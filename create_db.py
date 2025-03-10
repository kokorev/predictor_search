#!/usr/bin/env python
# coding=utf-8
"""
this file contains user function for creating and filling the db
"""
import netCDF4
import numpy as np
from scipy import stats
from sqlalchemy import and_
from settings import engine
from sql_models import Base, result
from settings import Session, session


def points_list_from_netcdf(fn, p_obj, var_name=None, lat_name='lat', lon_name='lon', lat_bnd=None, lon_bnd=None, **p):
    """
    Extract gridpoints indexes and coordinates information from netCDF file
    :param fn: path to source netcdf file
    :param p_obj: sql model to use (x_point or y_point)
    :param var_name: name of the primnary variable in the netCDF file. It used to calculate mask for the
            points with missing data
    :param lat_name: name of the latitude axis in the netCDF file
    :param lon_name: name of the longitude axis in the netCDF file
    :param lat_bnd: [min_lat, max_lat] use only points inside the set boundaries
    :param lon_bnd: [min_lon, max_lon] use only points inside the set boundaries
    :return:
    """
    nc = netCDF4.Dataset(fn)
    lat = nc.variables[lat_name]
    n_lat = lat.shape[0]
    lon = nc.variables[lon_name]
    n_lon = lon.shape[0]
    get_ind = lambda lati, loni: lati * n_lon + loni
    isinbounds = lambda v, bnd: bnd[0] <= v <= bnd[1] if bnd is not None else True
    if var_name is not None:
        dat = nc.variables[var_name]
        missing_mask = dat[:, :, :].mask
        miss_data_mask = np.all(missing_mask, axis=0)
    else:
        miss_data_mask = np.zeros((n_lat, n_lon), dtype=bool)
    points_list = []
    for lat_ind in range(n_lat):
        latv = lat[lat_ind]
        if not isinbounds(latv, lat_bnd): continue
        for lon_ind in range(n_lon):
            lonv = lon[lon_ind]
            if miss_data_mask[lat_ind, lon_ind]: continue
            if not isinbounds(lonv, lon_bnd): continue
            pt = p_obj(ind=get_ind(lat_ind, lon_ind), lat_ind=lat_ind, lon_ind=lon_ind, lat=latv, lon=lonv)
            points_list.append(pt)
    return points_list


def create_db():
    """
    create in the db tables described in sql_models.py
    db connection described in settings.py
    """
    Base.metadata.create_all(engine)


@session
def add_meta(cfg):
    """
    Adds a information about x and y points to the database
    :return:
    """
    ses = Session()
    plst = points_list_from_netcdf(**cfg['y'])
    ses.add_all(plst)
    plst = points_list_from_netcdf(**cfg['x'])
    ses.add_all(plst)


@session
def add_data(yMin, yMax, month, cfg, lag=0, corr_func=stats.spearmanr, check_if_exist=False):
    """
    Calculate correlations between all possible point pairs for particular month.
    Correlation calculated for set interval, the interval is not saved in the database
    and assumed to be the same for all values
    :param yMin: first year (inclusive)
    :param yMax: flast year (inclusive)
    :param month: value of this month selected from each year
    :param check_if_exist: if True the function will check if the record already exist in the database before
    attempting to write results. This slowdown the process significantly since sql query performed for each points pair.
    However, an attempt to write to db result for a pair that alredy exist in db will rise an error.
    :return:
    """
    ses = Session()
    x_points_lst = ses.query(cfg['x']['p_obj']).all()
    y_points_lst = ses.query(cfg['y']['p_obj']).all()
    y_conn = cfg['y']['reader'](**cfg['y'])
    y_conn.set_time_masks(yMin, yMax)
    x_conn = cfg['x']['reader'](**cfg['x'])
    x_conn.set_time_masks(yMin, yMax)
    if check_if_exist:
        resq = ses.query(result).filter(result.month == month)
    r_obj_lst = list()
    icount = 0
    for x_pnt in x_points_lst:
        for y_pnt in y_points_lst:
            if check_if_exist:
                tq = resq.filter(and_(result.x_ind == x_pnt.ind, result.y_ind == y_pnt.ind))
                if ses.query(tq.exists()).scalar():
                    continue
            y_vals = y_conn.get_predictor(y_pnt.lat_ind, y_pnt.lon_ind, month)
            x_vals = x_conn.get_predictor(x_pnt.lat_ind, x_pnt.lon_ind, month - lag)
            mask = y_vals.mask.__invert__()
            if sum(mask) > 10:
                r, pval = corr_func(y_vals[mask], x_vals[mask])
                r_obj = result(x_ind=x_pnt.ind, y_ind=y_pnt.ind, month=month, lag=lag, val=r, p=pval)
                r_obj_lst.append(r_obj)
                icount += 1
            if icount >= 10000:
                ses.add_all(r_obj_lst)
                r_obj_lst = list()
                ses.commit()
                icount = 0


if __name__ == '__main__':
    from settings import cfg
    # create_db()
    # add_meta(cfg)
    yMin, yMax = 1981, 2010
    # add_data(yMin, yMax, 10, lag=2, check_if_exist=False)
    for month in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        add_data(yMin, yMax, month, cfg, lag=2, check_if_exist=False)
        print(month)
    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        add_data(yMin, yMax, month, cfg, lag=0, check_if_exist=False)
        print(month)
