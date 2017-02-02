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


@session
def select_neighbors(model, ind, n_lon, radius=None, connected=True):
    """
    Select neighboring grid points
    :param model: y_point or x_point
    :param ind: point index
    :param n_lon: number of gridpoints on lon axis
    :param radius: radius of neigbor search
    :param connected: select only directly connected points, if false then radius must be set
    :return: list of neighbor indexes including original index
    """

    def get_all_neighbors(i, n_lon):
        return {i - n_lon - 1, i - n_lon, i - n_lon + 1, i - 1, i + 1, i + n_lon - 1, i + n_lon,
                i + n_lon + 1}

    def get_linear_neighbors(i, n_lon):
        return {i - n_lon, i - 1, i + 1, i + n_lon}

    if not connected:
        assert radius is not None, "if connected is false then radius must be set"
    ses = Session()
    all_existing_inds = set([v[0] for v in ses.query(model.ind).all()])
    if radius is None:
        f = get_linear_neighbors
    else:
        f = get_all_neighbors
    get_existing = lambda i: [i for i in f(i, n_lon) if i in all_existing_inds]
    neighbors = set(get_existing(ind))
    search = True
    while search:
        addition = set()
        for nind in neighbors:
            addition = addition.union(get_existing(nind))
        addition = addition.difference(neighbors)
        if len(addition) == 0:
            if connected:
                search = False
        else:
            neighbors = neighbors.union(addition)
        if radius is not None:
            radius -= 1
        if radius == 0:
            search = False
    return list(neighbors)


if __name__ == '__main__':
    from settings import y_point, cfg
    ind = 7655
    y_conn = cfg['y']['reader'](**cfg['y'])
    r = select_neighbors(y_point, ind, 200)
    print(r)