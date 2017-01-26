#!/usr/bin/env python
# coding=utf-8
"""
contain settings, db connection, and other common resources
"""
from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base
from readers import netcdfReader, hdf5Reader
Base = declarative_base()   # we should create Base before we could import sql models
from sql_models import x_point, y_point


x_config = {
    'fn': r'C:\data\noaa.ersst.v4\sst.mnmean.v4.nc',    # path to input file
    'reader': hdf5Reader,   # reader class to read the data. Do not forget to import it from readers.py
    'p_obj': x_point,       # sql model to save point coordinates and other information.
    'var_name': 'sst',  # name of a main variable for netCDF, hdf formats
    # the parameters below are optional. Technically, 'var_name' is also optional but it needed for all existing readers
    'lat_name': 'lat',      # name of a latitude axis for netCDF files. 'lat' is default value
    'lon_name': 'lon',      # name of a longitude axis for netCDF files. 'lon' is default value
    'lat_bnd': [-30, 30],   # use only points inside lat/lon box
    'lon_bnd': [80, 180]    # if not provided the whole dataset is used
}

y_config = {
    'fn': r'C:\data\SACA&D\grid\rr_0.5deg_regular_mon_anoms.nc',
    'var_name': 'rr',
    'lat_name': 'latitude',
    'lon_name': 'longitude',
    'reader': netcdfReader,
    'p_obj': y_point
}

home = os.getcwd()

engine = create_engine('sqlite:///%s' % (os.path.join(home, 'db', 'main.sqlite')))