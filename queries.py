#!/usr/bin/env python
# coding=utf-8
"""
In this file functions that extract some parameters from the dataset for further analysis
"""
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from settings import engine, x_config
from sql_models import result


def mean_x_influence(month=None, f=np.mean, lag=0):
    """
    Estimate how influential x_point is
    get the list of all the correlations from each x_point and apply provided function to this list (mean by default)
    :param month: use correlation for this month only. If None use the whole year
    :param f: function that take a list of correlations as input and return the measure of influence
    :return: return numpy array of [ind, lat, lon, val]
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    x_points_lst = ses.query(x_config['p_obj']).all()
    q = ses.query(result)
    res = []
    for pnt in x_points_lst:
        qr = q.filter(and_(result.x_ind == pnt.ind, result.lag == lag))
        if month is not None:
            qr = qr.filter(result.month == month)
        rho_lst = [abs(v.val) for v in qr if v.val is not None]
        rval = f(rho_lst)
        res.append([pnt.ind, pnt.lat, pnt.lon, rval])
    ses.close()
    return np.array(res)


def get_y_point_correlations(point_ind, month, lag=0):
    """
    Return ind, x, y, z array of correlations for each x point and given y point
    :param point_ind: index of x point, if not exist res will return empty array
    :param month: month
    :return:
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    q = ses.query(result).filter(and_(result.y_ind == point_ind, result.month == month, result.lag == lag))
    res = np.array([[r.x_ind, r.x_point.lat, r.x_point.lon, r.val] for r in q])
    return res


def get_y_group_mean_correlations(y_ind_lst, month, lag=0):
    """
    Return ind, x, y, z array of correlations. For each x point and given set y points mean correlation calculated.
    :param y_ind_lst: list of x point indexes
    :param month: month
    :return:
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    q = ses.query(result).filter(and_(result.y_ind.in_(y_ind_lst), result.month == month, result.lag == lag))
    dat = np.array([[r.x_ind, r.y_ind, r.x_point.lat, r.x_point.lon, r.val] for r in q])
    x_ind_lst = np.unique(dat[:, 0])
    res = []
    for x_ind in x_ind_lst:
        this_dat = dat[dat[:, 0] == x_ind]
        res.append([x_ind, this_dat[0, 2], this_dat[0, 3], this_dat[:, 4].mean()])
    return np.array(res)


if __name__ == '__main__':
    import os

    res_path = r'..\saca_grid_explore\results\predictor_search'
    m = 10
    ind = 7655

    # r = get_y_point_correlations(ind, m)
    # np.savetxt(os.path.join(res_path, 'point_corrs_%i_m%02i.csv' % (ind,m)), r, delimiter=',', header='ind,lat,lon,rho',
    #                         comments='')

    r = mean_x_influence(month=m, lag=2)
    np.savetxt(os.path.join(res_path, 'mean_influence_lag2_m%02i.csv' % m), r, delimiter=',', header='ind,lat,lon,rho',
               comments='')
