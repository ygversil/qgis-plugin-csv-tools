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

from processing import run as run_alg
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProcessingException,
    QgsVectorLayer
)
import qgis.testing
import qgis.utils

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
             'subsetIndex=no&watchFile=no&delimiter=;&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Semicolon delimiter with spaces',
             {'delimiter': ' ; '},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=;&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Tab delimiter',
             {'delimiter': 'tab'},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=\\t&geomType=none&'
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
             'subsetIndex=no&watchFile=no&delimiter=;&quote=%27&geomType=none&'
             'spatialIndex=no'.format(csv_path)),
            ('Semicolon delimiter, WKT geometry',
             {'delimiter': ';', 'geometry_data': 0, 'wkt_field': 'wkt', 'crs': 2154},
             'file://{}?type=csv&useHeader=Yes&decimalPoint=.&trimFields=Yes&detectTypes=yes&'
             'subsetIndex=no&watchFile=no&delimiter=;&wktField=wkt&crs=2154&'
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


class LoadCSVAlgorithmTest(qgis.testing.TestCase):
    """Test for the ``loadcsvfile`` processing algorithm."""

    @classmethod
    def setUpClass(cls):
        qgis.utils.loadPlugin(PLUGIN_NAME)
        qgis.utils.startPlugin(PLUGIN_NAME)

    @classmethod
    def tearDownClass(cls):
        qgis.utils.unloadPlugin(PLUGIN_NAME)

    def test_layer_from_csv(self):
        """Check that ``loadcsvfile`` algorithm produces correct layer."""
        params = {
            'INPUT': (pathlib.Path(__file__).parent / 'load_comma_header_geometry.csv').as_posix(),
            'CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'DECIMAL_POINT': 0,
            'DELIMITER': 0,
            'GEOMETRY_DATA': 0,
            'QUOTE_CHAR': '\"',
            'USE_HEADER': True,
            'WKT_FIELD': 'wkt',
            'X_FIELD': '',
            'Y_FIELD': '',
            'OUTPUT': 'memory:',
        }
        r = run_alg('csvtools:loadcsvfile', params)
        expected_layer = QgsVectorLayer('{gpkg_path}|layername={layername}'.format(
            gpkg_path=(pathlib.Path(__file__).parent / 'expected_after_load_csv.gpkg').as_posix(),
            layername='expected_after_load_csv'
        ), 'expected_after_load_csv', 'ogr')
        self.assertLayersEqual(layer_result=r['OUTPUT'], layer_expected=expected_layer, pk='fid')


class LoadCSVAlgorithmErrorTest(unittest.TestCase):
    """Test for errors when running the ``loadcsvfile`` processing algorithm."""

    @classmethod
    def setUpClass(cls):
        qgis.utils.loadPlugin(PLUGIN_NAME)
        qgis.utils.startPlugin(PLUGIN_NAME)

    @classmethod
    def tearDownClass(cls):
        qgis.utils.unloadPlugin(PLUGIN_NAME)

    def test_cannot_load_layer_from_inexistant_file(self):
        """Check that ``loadcsvfile`` algorithm raises an error if called with non existent file."""
        with self.assertRaises(QgsProcessingException):
            params = {
                'INPUT': '/file_that_do_no_exists.csv',
                'CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
                'DECIMAL_POINT': 0,
                'DELIMITER': 0,
                'GEOMETRY_DATA': 0,
                'QUOTE_CHAR': '\"',
                'USE_HEADER': True,
                'WKT_FIELD': 'wkt',
                'X_FIELD': '',
                'Y_FIELD': '',
                'OUTPUT': 'memory:',
            }
            run_alg('csvtools:loadcsvfile', params)


if __name__ == '__main__':
    unittest.main()
