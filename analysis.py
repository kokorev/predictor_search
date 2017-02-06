#!/usr/bin/env python
# coding=utf-8
"""

"""
import numpy as np


def vector2array(dat, missing=-999):
    """
    converts xyz vector to 2d array
    :param dat:  xyz array
    :param missing:
    :return: 2d array, x_axis values, y_axis values
    """
    x = dat[:, 0]
    y = dat[:, 1]
    x_axis = np.unique(x)
    x_axis.sort()
    x_dict = {k: v for v, k in enumerate(x_axis)}
    y_axis = np.unique(y)
    y_axis.sort()
    y_dict = {k: v for v, k in enumerate(y_axis)}
    grid = np.empty((len(x_axis), len(y_axis)))  # (max(x)-min(x)+1,max(y)-min(x)+1)
    grid.fill(missing)
    x_nums = [x_dict[v] for v in x]
    y_nums = [y_dict[v] for v in y]
    grid[x_nums, y_nums] = dat[:, 2]
    return grid, x_axis, y_axis


def clusters(b):
    """
    Islands search on binary array
    Search for True values
    :param b:
    :return: dictionary with {clusterNumber: list of indexes, }
    """

    def get_point_neighors(xind, yind, i):
        m1 = (xind == xind[i]) & np.logical_or((yind == yind[i] + 1), (yind == yind[i] - 1))
        m2 = (yind == yind[i]) & np.logical_or((xind == xind[i] + 1), (xind == xind[i] - 1))
        m = m1 | m2
        return np.nonzero(m)[0]

    inds = np.nonzero(b)
    xind, yind = inds
    clst = np.arange(len(xind))
    for i in range(len(xind)):
        nbrs_inds = get_point_neighors(xind, yind, i)
        neighbors = clst[nbrs_inds]
        for n in neighbors:
            clst[clst == n] = clst[i]
    res = {}
    for k, ci in enumerate(np.unique(clst)):
        res[k] = [xind[clst == ci], yind[clst == ci]]
    return res


def localMaxima(grid, threshold):
    """
    Search for local maximums above threshold. First search for islands of values above threshold
    then return coordinate of maximum value for each island
    :param grid: 2d array
    :param threshold:
    :return: list of [[x,y],] coordinates
    """
    res = []
    clst = clusters(grid > threshold)
    for c in clst:
        mp = np.argmax(grid[clst[c]])
        p = [clst[c][0][mp], clst[c][1][mp]]
        res.append(p)
    return res


if __name__ == '__main__':
    res_path = r'..\saca_grid_explore\results\predictor_search'
    for month in range(3, 13):
        r = np.genfromtxt(res_path + r'\Java_mean_corrs_7655_m%02i_lag2.csv' % month, delimiter=',', skip_header=1)
        d = r[:, [1, 2, 3]]
        g, x, y = vector2array(d)
        indsGrid = vector2array(r[:, [1, 2, 0]])[0]
        grid = np.ma.masked_less(g, -900)
        result = localMaxima(grid, 0.40)
        for v in result:
            print(month, indsGrid[v[0], v[1]], x[v[0]], y[v[1]], round(grid[v[0], v[1]], 2))
