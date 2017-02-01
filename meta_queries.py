#!/usr/bin/env python
# coding=utf-8
"""
this file contain functions for selecting points from db
"""
from settings import session, Session
import shapefile
from shapely.geometry import Polygon, Point
from sqlalchemy import and_


def cLon(lon):
    """ Convert longitude to 181+ format """
    if lon < 0:
        lon = 360 + lon
    return lon


@session
def select_points_in_shp(model, shp_fn):
    """
    Select points inside given polygon
    :param model: sql model to query from, normally x_point or y_point
    :param shp_fn: path to .shp file
    :return: points inside given shape as a list indexes
    """
    # todo: test if works
    ses = Session()
    q = ses.query(model)
    sf = shapefile.Reader(shp_fn)
    res = []
    for sp in sf.shapes():
        res_tmp = []
        lonmin, latmin, lonmax, latmax = sp.bbox
        lonmin, lonmax = cLon(lonmin), cLon(lonmax)
        points_lst = q.filter(and_(model.lat >= latmin, model.lat <= latmin, model.lon <= lonmax, model.lon >= lonmin))
        if lonmin < 0 or lonmax < 0:
            polygonPoints = [[cLon(cors[0]), cors[1]] for cors in sp.points]
        else:
            polygonPoints = sp.points
        poly = Polygon(polygonPoints)
        for pnt in points_lst:
            lat, lon = pnt.lat, cLon(pnt.lon)
            pnt_shp = Point(lon, lat)
            if poly.contains(pnt_shp): res_tmp.append(pnt.ind)
        res += res_tmp
    return list(set(res))
