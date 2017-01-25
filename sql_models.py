#!/usr/bin/env python
# coding=utf-8
"""
this file defines sql models used in db
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from settings import Base
from sqlalchemy.orm import relationship


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


# class calculated(Base):
#     __tablename__ = 'calc_logs'
#     x_ind = Column(Integer, ForeignKey("x_point.ind"), nullable=False, primary_key=True)
#     y_ind = Column(Integer, ForeignKey("y_point.ind"), nullable=False, primary_key=True)
#     added = Column(DateTime)


if __name__ == '__main__':
    pass