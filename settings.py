#!/usr/bin/env python
# coding=utf-8
"""
contain settings, db connection, and other common resources
"""
from sqlalchemy import create_engine
import os
from readers import netcdfReader, hdf5Reader
from sql_models import x_point, y_point
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

cfg = {
    'x': {
        'fn': r'C:\data\noaa.ersst.v4\sst.mnmean.v4.nc',  # path to input file
        'reader': hdf5Reader,  # reader class to read the data. Do not forget to import it from readers.py
        'p_obj': x_point,  # sql model to save point coordinates and other information.
        'var_name': 'sst',  # name of a main variable for netCDF, hdf formats
        # the parameters below are optional. Technically, 'var_name' is also optional but it needed for all existing readers
        'lat_name': 'lat',  # name of a latitude axis for netCDF files. 'lat' is default value
        'lon_name': 'lon',  # name of a longitude axis for netCDF files. 'lon' is default value
        'lat_bnd': [-40, 40],  # use only points inside lat/lon box
        'lon_bnd': [50, 180]  # if not provided the whole dataset is used
    },
    'y': {
        'fn': r'C:\data\SACA&D\grid\rr_0.5deg_regular_mon_anoms.nc',
        'var_name': 'rr',
        'lat_name': 'latitude',
        'lon_name': 'longitude',
        'reader': netcdfReader,
        'p_obj': y_point
    }
}


home = os.getcwd()

engine = create_engine('sqlite:///%s' % (os.path.join(home, 'db', 'main_lags_new.sqlite')))
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def session(func):
    """
    this is the decorator providing thread-safe session for functions that need it
    in case of error in function session is rolled back before raising the exception
    session is closed automatically after
    the decorated function should use >>> ses = Session(), it will refer to the same session as in the decorator
    :param func:
    :return:
    """

    def wrapped(*args, **kw):
        ses = Session()
        try:
            result = func(*args, **kw)
            ses.commit()
        except:
            ses.rollback()
            raise
        finally:
            ses.close()
        return result

    return wrapped
