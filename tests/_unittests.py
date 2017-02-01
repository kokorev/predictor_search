#!/usr/bin/env python
# coding=utf-8
"""
here be unittests
"""
import unittest
import os.path

class test_netCDFReader(unittest.TestCase):

    def setUp(self):
        from readers import netcdfReader
        y_config = {
            'fn': os.path.join('test_data', 'test.nc'),
            'var_name': 'rr',
            'lat_name': 'latitude',
            'lon_name': 'longitude',
            'reader': netcdfReader,
        }
        self.reader = netcdfReader(**y_config)
        self.reader.set_time_masks(1991, 1993)

    def test_get_predictor(self):
        self.assertAlmostEqual(self.reader.get_predictor(9, 75, 1)[0], -22.3, places=2) # -105.9, -58.3, np.nan, -64.1
        self.assertAlmostEqual(self.reader.get_predictor(9, 75, 1)[1], -105.9, places=2)
        self.assertAlmostEqual(self.reader.get_predictor(9, 75, 1)[2], -58.3, places=2)

    def tearDown(self):
        self.reader.nc.close()