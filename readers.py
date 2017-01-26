#!/usr/bin/env python
# coding=utf-8
"""
Classes to read data from source files. Each class have an get_predictor() method that takes lat_ind, lon_ind, month
and return data for preset period.
"""
import numpy as np
import netCDF4
import h5py


class netcdfReader:
    def __init__(self, fn, var_name, lat_name='lat', lon_name='lon', time_name='time', in_memory=True, **p):
        self.nc = netCDF4.Dataset(fn)
        self.lat = self.nc.variables[lat_name]
        self.lon = self.nc.variables[lon_name]
        self.time = self.nc.variables[time_name]
        if in_memory:
            self.dat = np.ma.array(self.nc.variables[var_name][:, :, :])
        else:
            self.dat = self.nc.variables[var_name]
        self.dates_lst = netCDF4.num2date(self.time[:], self.time.units)
        self.period_set = False

    def set_time_masks(self, y_min, y_max):
        mon_time_masks = dict()
        for m in range(1, 13):
            mask_lst = [True if (y_min <= d.year <= y_max) and (d.month == m) else False for d in self.dates_lst]
            mon_time_masks[m] = np.array(mask_lst)
        self.y_min = y_min
        self.y_max = y_max
        self.mon_time_masks = mon_time_masks
        self.period_set = True
        return mon_time_masks

    def get_predictor(self, lat_ind, lon_ind, month):
        if not self.period_set:
            raise AttributeError("set the time bounds first, netcdfReader.set_time_masks(y_min, y_max)")
        vals = self.dat[self.mon_time_masks[month], lat_ind, lon_ind]
        return vals


class hdf5Reader(netcdfReader):
    def __init__(self, fn, var_name, lat_name='lat', lon_name='lon', time_name='time', in_memory=True, **p):
        self.f = h5py.File(fn, "r")
        # self.fillValue = self.f[var_name].attrs['missing_value']
        if in_memory:
            self.dat = np.array(self.f[var_name])
        else:
            self.dat = self.f[var_name]
        self.lat = np.array(self.f[lat_name])
        self.lon = np.array(self.f[lon_name])
        self.time = np.array(self.f[time_name])
        self.dates_lst = netCDF4.num2date(self.time[:], self.f[time_name].attrs['units'].decode('ascii'))
        self.period_set = False


if __name__ == '__main__':
    pass
