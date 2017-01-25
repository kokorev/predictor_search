#!/usr/bin/env python
# coding=utf-8
"""
contain settings, db connection, and other common resources
"""
from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base

fns = {'y': r'C:\data\SACA&D\grid\rr_0.5deg_regular_mon_anoms.nc',
       'x': r'C:\data\noaa.ersst.v4\sst.mnmean.v4.nc'
       }
Base = declarative_base()

home = os.getcwd()

engine = create_engine('sqlite:///%s' % (os.path.join(home, 'db', 'main.sqlite')))