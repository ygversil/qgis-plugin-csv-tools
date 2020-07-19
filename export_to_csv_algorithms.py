# -*- coding: utf-8 -*-

"""
/***************************************************************************
 CSVTools
                                 A QGIS plugin
 Adds new processing algorithms and models that deal with CSV files
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-02-19
        copyright            : (C) 2019 by Yann Voté
        email                : ygversil@lilo.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Yann Voté'
__date__ = '2019-02-19'
__copyright__ = '(C) 2019 by Yann Voté'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


import csv
import io
import re
import sqlite3
import tempfile
import sys

from PyQt5.QtGui import QIcon
from processing import run as run_alg
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
)
from .qgis_version import HAS_DB_PROCESSING_PARAMETER
from .utils import pg_conn, pg_copy


csv.field_size_limit(int(sys.maxsize / 1000))


_DATETIME_REGEXP = re.compile(r'(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)'
                              r'[T\s]+'
                              r'(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)'
                              r'(?P<microseconds>.\d+)?Z?')


if HAS_DB_PROCESSING_PARAMETER:
    from qgis.core import QgsProcessingParameterProviderConnection
else:
    from processing.tools.postgis import GeoDB


class _AbstractExportQueryToCsv(QgisAlgorithm):
    """Abstract algorithm that takes a ``SELECT`` SQL query, run it against a
    database, and export the results into a CSV file."""

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    DATABASE = 'DATABASE'
    SELECT_SQL = 'SELECT_SQL'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(QgsProcessingParameterString(
            self.SELECT_SQL,
            self.tr('SELECT SQL query'),
            multiLine=True,
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT,
            self.tr('CSV file'),
            'CSV files (*.csv)',
        ))

    def groupId(self):
        """Algorithm group identifier."""
        return 'exporttocsv'

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        select_sql = self.parameterAsString(parameters, self.SELECT_SQL,
                                            context)
        select_sql = str(select_sql).strip().replace('\n', ' ')
        # XXX: check if this a SELECT query
        qgis_conn = self._get_connection(parameters, self.DATABASE, context)
        csv_fpath = self.parameterAsFileOutput(parameters, self.OUTPUT,
                                               context)
        if csv_fpath:
            with open(csv_fpath, 'w') as csvf:
                writer = csv.writer(csvf, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                for row in self._db_rows(qgis_conn, select_sql):
                    writer.writerow(_normalize_row(row))
        return {self.OUTPUT: csv_fpath}


# TODO: write tests
class ExportPostgreSQLQueryToCsv(_AbstractExportQueryToCsv):
    """QGIS algorithm that takes a ``SELECT`` SQL query, run it against a
    PostgreSQL database, and ``COPY`` the results into a CSV file."""

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        if HAS_DB_PROCESSING_PARAMETER:
            db_param = QgsProcessingParameterProviderConnection(
                self.DATABASE,
                self.tr('Database (connection name)'),
                'postgres',
            )
        else:
            db_param = QgsProcessingParameterString(
                self.DATABASE,
                self.tr('Database (connection name)'),
            )
            db_param.setMetadata({
                'widget_wrapper': {
                    'class': ('processing.gui.wrappers_postgis'
                              '.ConnectionWidgetWrapper')
                }
            })
        self.addParameter(db_param)
        super().initAlgorithm(config)

    def name(self):
        """Algorithm identifier."""
        return 'exportpostgresqlquerytocsv'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Export PostgreSQL query to CSV (COPY)')

    def group(self):  # Cannot be factored in abstract class because of i18n
        """Algorithm group human name."""
        return self.tr('Export to CSV')

    def shortHelpString(self):
        """Algorithm help message displayed in the right panel."""
        return self.tr(
            "This algorithm creates a CSV file from an SQL SELECT query. The "
            "query is ran against a PostgreSQL/Postgis database, then the "
            "result table is exported as CSV using the PostgreSQL COPY "
            "command."
        )

    def icon(self):
        """Algorithm's icon."""
        return QIcon(':/plugins/csv_tools/pg2csv.png')

    def _get_connection(self, parameters, param, context):
        if HAS_DB_PROCESSING_PARAMETER:
            return self.parameterAsConnectionName(parameters, self.DATABASE, context)
        else:
            return self.parameterAsString(parameters, self.DATABASE, context)

    def _db_rows(self, qgis_conn, select_sql):
        with tempfile.TemporaryFile() as fb, \
                io.TextIOWrapper(fb, encoding='utf-8', newline='') as f:
            if HAS_DB_PROCESSING_PARAMETER:
                with pg_conn(qgis_conn) as conn, \
                        conn.cursor() as cur:
                    pg_copy(cur, select_sql, f)
            else:
                db = GeoDB.from_name(qgis_conn)
                cur = db.con.cursor()
                pg_copy(cur, select_sql, f)
            f.seek(0)
            reader = csv.reader(f, delimiter='|', quotechar='"')
            yield from reader


# TODO: write tests
class ExportSQLiteQueryToCsv(_AbstractExportQueryToCsv):
    """QGIS algorithm that takes a ``SELECT`` SQL query, run it against a
    SQLite database, and export the results into a CSV file."""

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(QgsProcessingParameterFile(
            self.DATABASE,
            self.tr('GeoPackage or Spatialite database')
        ))
        super().initAlgorithm(config)

    def name(self):
        """Algorithm identifier."""
        return 'exportsqlitequerytocsv'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Export SQLite query to CSV')

    def group(self):  # Cannot be factored in abstract class because of i18n
        """Algorithm group human name."""
        return self.tr('Export to CSV')

    def shortHelpString(self):
        """Algorithm help message displayed in the right panel."""
        return self.tr(
            "This algorithm creates a CSV file from an SQL SELECT query. The "
            "query is ran against an SQLite database (Geopackage or "
            "Spatialite), then the result table is exported as CSV."
        )

    def icon(self):
        """Algorithm's icon."""
        return QIcon(':/plugins/csv_tools/gpkg2csv.png')

    def _get_connection(self, parameters, param, context):
        return self.parameterAsString(parameters, self.DATABASE, context)

    def _db_rows(self, qgis_conn, select_sql):
        with sqlite3.connect(qgis_conn) as conn:
            cur = conn.cursor()
            cur.execute(select_sql)
            yield tuple(item[0] for item in cur.description)
            yield from cur


# TODO: write tests
class ExportLayerToCsv(QgisAlgorithm):
    """QGIS algorithm that takes a vector layer and converts it to a CSV file with WKT Geometry."""

    INPUT = 'INPUT'
    OPTIONS = 'OPTIONS'
    OUTPUT = 'OUTPUT'

    def name(self):
        """Algorithm identifier."""
        return 'exportlayertocsv'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Export layer to CSV')

    def groupId(self):
        """Algorithm group identifier."""
        return 'exporttocsv'

    def group(self):
        """Algorithm group human name."""
        return self.tr('Export to CSV')

    def icon(self):
        """Algorithm's icon."""
        return QIcon(':/plugins/csv_tools/layer2csv.png')

    def shortHelpString(self):
        """Algorithm help message displayed in the right panel."""
        return self.tr(
            "This algorithm creates a CSV file from a vector layer. Geometries are converted to "
            "WKT strings."
        )

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT,
            self.tr('Input vector layer'),
            types=[QgsProcessing.TypeVector],
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT,
            self.tr('CSV file'),
            'CSV files (*.csv)',
        ))

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        csv_fpath = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        options_dict = {
            'GEOMETRY': 'AS_WKT',
            'SEPARATOR': 'COMMA',
            'STRING_QUOTING': 'IF_AMBIGUOUS',
        }
        alg_params = {
            'INPUT': input_layer,
            'OPTIONS': ' '.join('-lco {k}={v}'.format(k=k, v=v) for k, v in options_dict.items()),
            'OUTPUT': csv_fpath,
        }
        return run_alg('gdal:convertformat', alg_params, context=context, feedback=feedback)


def _normalize_boolean(v):
    return {'t': '1', 'f': '0'}.get(v, v)


def _normalize_datetime(v):
    m = _DATETIME_REGEXP.match(v)
    if not m:
        return v
    else:
        return ('{year}-{month}-{day}'
                'T'
                '{hour}:{minute}:{second}'
                'Z'.format(**m.groupdict()))


def _normalize_row(row):
    """Return a new row from the given one with normalized values."""
    row = map(lambda v: str(v).strip() if v is not None else '', row)
    row = map(_normalize_boolean, row)
    row = map(_normalize_datetime, row)
    return row
