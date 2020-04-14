"""Tests for the ``loadcsvfile`` algorithm.


.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'ygversil@lilo.org'
__date__ = '13/04/2020'
__copyright__ = ('Copyright 2020, Yann Voté')


import importlib
import pathlib
import unittest

from . import PLUGIN_NAME


class QgisCsvUriTest(unittest.TestCase):
    """Test for the ``_qgis_csv_uri`` function."""

    @classmethod
    def setUpClass(cls):
        cls.alg_module = importlib.import_module(
            '{plugin_name}.{module_name}'.format(
                plugin_name=PLUGIN_NAME,
                module_name='import_from_csv_algorithms'
            )
        )

    def test_correct_uri(self):
        """Check that correct CSV URI is build for QGIS when loading CSV file."""
        self.maxDiff = None  # Show long line differences in test output
        csv_path = pathlib.Path('/tmp/data.csv').as_posix()
        for msg, params, expected_uri in (
            ('No params given, all default values',
             {},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&geomType=none&spatialIndex=no'.format(csv_path)),
            ('Default delimiter and quote char',
             {'delimiter': ',', 'quotechar': '"'},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&geomType=none&spatialIndex=no'.format(csv_path)),
            ('Semicolon delimiter',
             {'delimiter': ';'},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=%3B&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Semicolon delimiter with spaces',
             {'delimiter': ' ; '},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=%3B&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Pipe delimiter',
             {'delimiter': '|'},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=%7C&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Comma decimal point',
             {'decimal_point': ','},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=%2C&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&geomType=none&spatialIndex=no'.format(csv_path)),
            ('No header',
             {'use_header': False},
             'file://{}?type=csv&useHeader=No&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&geomType=none&spatialIndex=no'.format(csv_path)),
            ('Caution: only empty string or False or None for use_header is False',
             {'use_header': 'no'},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&geomType=none&spatialIndex=no'.format(csv_path)),
            ('Semicolon delimiter, single quote char',
             {'delimiter': ';', 'quotechar': "'"},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=%3B&quote=%27&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Semicolon delimiter, WKT geometry',
             {'delimiter': ';', 'geometry_data': 0, 'wkt_field': 'wkt', 'crs': 2154},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=%3B&wktField=wkt&crs=2154&'
             'spatialIndex=yes'.format(csv_path)),
            ('XY geometry',
             {'geometry_data': 1, 'x_field': 'lon', 'y_field': 'lat', 'crs': 4326},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&xField=lon&yField=lat&crs=4326&'
             'spatialIndex=yes'.format(csv_path)),
        ):
            with self.subTest(msg=msg):
                self.assertEqual(
                    self.alg_module._qgis_csv_uri(csv_path, **params),
                    expected_uri
                )

    def test_error_on_inconsistent_parameters(self):
        """Check error is raised when inconsistent parameters are given to ``_qgis_csv_uri``."""
        csv_path = pathlib.Path('/tmp/data.csv').as_posix()
        for msg, params in (
            ('WKT geometry but no WKT field',
             {'geometry_data': 0, 'crs': 2154}),
            ('WKT geometry but empty WKT field',
             {'geometry_data': 0, 'wktField': '', 'crs': 2154}),
            ('WKT geometry but empty WKT field (only spaces)',
             {'geometry_data': 0, 'wktField': '', 'crs': 2154}),
            ('WKT geometry but no CRS',
             {'geometry_data': 0, 'wktField': 'wkt'}),
            ('XY geometry but no X field',
             {'geometry_data': 1, 'y_field': 'lat', 'crs': 4326}),
            ('XY geometry but no Y field',
             {'geometry_data': 1, 'x_field': 'lon', 'crs': 4326}),
            ('XY geometry but no CRS',
             {'geometry_data': 1, 'x_field': 'lon', 'y_field': 'lat'}),
        ):
            with self.subTest(msg=msg), \
                    self.assertRaises(ValueError):
                self.alg_module._qgis_csv_uri(csv_path, **params),

    def test_error_invalid_parameters(self):
        """Check that an error is raised when invalid parameters are given to ``_qgis_csv_uri``."""
        csv_path = pathlib.Path('/tmp/data.csv').as_posix()
        for msg, params, error in (
            ('Invalid delimiter',
             {'delimiter': 0},
             AttributeError),
            ('Invalid quotechar',
             {'quotechar': 0},
             AttributeError),
            ('Invalid decimal_point',
             {'decimal_point': 0},
             AttributeError),
            ('Invalid geometry_data',
             {'geometry_data': 'a'},
             ValueError),
        ):
            with self.subTest(msg=msg), \
                    self.assertRaises(error):
                self.alg_module._qgis_csv_uri(csv_path, **params),


if __name__ == '__main__':
    unittest.main()
