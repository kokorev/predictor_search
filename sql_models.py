#!/usr/bin/env python
# coding=utf-8
"""
this file defines sql models used in db
x_point, y_point tables contain lists of predictors their indexes and coordinates
spearman table contain calculated spearman correlations between x-y pairs
"""
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class x_point(Base):
    __tablename__ = 'x_point'
    ind = Column(Integer, primary_key=True)
    lat_ind = Column(Integer)
    lon_ind = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    results = relationship("result", back_populates="x_point")


class y_point(Base):
    __tablename__ = 'y_point'
    ind = Column(Integer, primary_key=True)
    lat_ind = Column(Integer)
    lon_ind = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    results = relationship("result", back_populates="y_point")


class result(Base):
    __tablename__ = 'spearman'
    x_ind = Column(Integer, ForeignKey("x_point.ind"), nullable=False, primary_key=True)
    x_point = relationship("x_point", back_populates="results")
    y_ind = Column(Integer, ForeignKey("y_point.ind"), nullable=False, primary_key=True)
    y_point = relationship("y_point", back_populates="results")
    month = Column(Integer, primary_key=True)
    val = Column(Float)
    p = Column(Float)


if __name__ == '__main__':
    pass