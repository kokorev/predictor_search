#!/usr/bin/env python
# coding=utf-8
"""
In this file functions that extract some parameters from the dataset for further analysis
"""
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from sql_models import result, x_point, y_point
from settings import engine


def mean_x_influence(month=None, f=np.mean):
    """
    Estimate how influential x_point is
    get the list of all the correlations from each x_point and apply provided function to this list (mean by default)
    :param month: use correlation for this month only. If None use the whole year
    :param f: function that take a list of correlations as input and return the measure of influence
    :return: return numpy array of [ind, lat, lon, val]
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    x_points_lst = ses.query(x_point).all()
    q = ses.query(result)
    res = []
    for pnt in x_points_lst:
        qr = q.filter(result.x_ind == pnt.ind)
        if month is not None:
            qr = qr.filter(result.month == month)
        rho_lst = [abs(v.val) for v in qr if v.val is not None]
        rval = f(rho_lst)
        res.append([pnt.ind, pnt.lat, pnt.lon, rval])
    ses.close()
    return np.array(res)


def get_y_point_correlations(point_ind, month):
    """
    Return ind, x, y, z array of correlations for each x point and given y point
    :param point_ind: index of x point, if not exist res will return empty array
    :param month: month
    :return:
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    q = ses.query(result).filter(and_(result.y_ind == point_ind, result.month == month))
    res = np.array([[r.x_ind, r.x_point.lat, r.x_point.lon, r.val] for r in q])
    return res


def get_y_group_mean_correlations(y_ind_lst, month):
    """
    Return ind, x, y, z array of correlations. For each x point and given set y points mean correlation calculated.
    :param y_ind_lst: list of x point indexes
    :param month: month
    :return:
    """
    Session = sessionmaker(bind=engine)
    ses = Session()
    q = ses.query(result).filter(and_(result.y_ind.in_(y_ind_lst), result.month == month))
    dat = np.array([[r.x_ind, r.y_ind, r.x_point.lat, r.x_point.lon, r.val] for r in q])
    x_ind_lst = np.unique(dat[:, 0])
    res = []
    for x_ind in x_ind_lst:
        this_dat = dat[dat[:, 0] == x_ind]
        res.append([x_ind, this_dat[0, 2], this_dat[0, 3], this_dat[:, 4].mean()])
    return np.array(res)


if __name__ == '__main__':
    v = get_y_group_mean_correlations([730, 731, 732], 10)
    print(v)
    # np.savetxt('res.csv', mean_x_influence(), delimiter=',', header='ind,lat,lon,rho', comments='')
