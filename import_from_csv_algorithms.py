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

import pathlib
import urllib

from PyQt5.QtGui import QIcon
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    Qgis,
    QgsFeatureSink,
    QgsMessageLog,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
    QgsVectorLayer,
)


def _qgis_csv_uri(csv_path, **kwargs):
    """Return a URI for QGIS to open given CSV file with given parameters.

    See https://qgis.org/pyqgis/master/core/QgsVectorLayer.html for reference on how to build
    such URIs and available parameters: look at section *delimietedText*.
    """
    base_uri = pathlib.Path(csv_path).as_uri()
    delimiter = kwargs.get('delimiter', ',').strip()
    quotechar = kwargs.get('quotechar', '"').strip()
    use_header = bool(kwargs.get('use_header', True))
    decimal_point = kwargs.get('decimal_point', '.').strip()
    geometry_data = int(kwargs.get('geometry_data', 2))
    wkt_field = kwargs.get('wkt_field')
    x_field = kwargs.get('x_field')
    y_field = kwargs.get('y_field')
    crs = kwargs.get('crs')
    params = (
        ('type', 'csv'),
        ('useHeader', 'Yes' if use_header else 'No'),
        ('decimalPoint', decimal_point),
        ('trimFields', 'Yes'),
        ('detectTypes', 'yes'),
        ('subsetIndex', 'no'),
        ('watchFile', 'no'),
    )
    if delimiter != ',':
        params += (('delimiter', delimiter if delimiter != 'tab' else '\\t'),)
    if quotechar != '"':
        params += (('quote', quotechar),)
    if geometry_data == 0:
        if not wkt_field:
            raise ValueError('while parsing parameters to load CSV file {}: geometry type is WKT '
                             'but wkt_field not provided'.format(csv_path))
        if not crs:
            raise ValueError('while parsing parameters to load CSV file {}: geometry type is WKT '
                             'but crs not provided'.format(csv_path))
        params += (
            ('wktField', wkt_field),
            ('crs', crs),
            ('spatialIndex', 'yes'),
        )
    elif geometry_data == 1:
        if not x_field or not y_field:
            raise ValueError('while parsing parameters to load CSV file {}: geometry type is XY '
                             'but x_field or y_field not provided'.format(csv_path))
        if not crs:
            raise ValueError('while parsing parameters to load CSV file {}: geometry type is XY '
                             'but crs not provided'.format(csv_path))
        params += (
            ('xField', x_field),
            ('yField', y_field),
            ('crs', crs),
            ('spatialIndex', 'yes'),
        )
    else:
        params += (
            ('geomType', 'none'),
            ('spatialIndex', 'no'),
        )
    return '{base_uri}?{params}'.format(
        base_uri=base_uri,
        params=urllib.parse.urlencode(params, safe=r'\:;')
    )


class LoadCSVAlgorithm(QgisAlgorithm):
    """QGIS algorithm that takes a CSV file and loads it as a vector layer."""

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    DELIMITER = 'DELIMITER'
    QUOTECHAR = 'QUOTE_CHAR'
    USE_HEADER = 'USE_HEADER'
    DECIMAL_POINT = 'DECIMAL_POINT'
    GEOMETRY_DATA = 'GEOMETRY_DATA'
    WKT_FIELD = 'WKT_FIELD'
    X_FIELD = 'X_FIELD'
    Y_FIELD = 'Y_FIELD'
    CRS = 'CRS'

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(QgsProcessingParameterFile(
            self.INPUT,
            self.tr('Input CSV file'),
            extension='csv',
        ))
        self.delimiters = [',', ';', 'tab']
        self.addParameter(QgsProcessingParameterEnum(
            self.DELIMITER,
            self.tr('Column delimiter'),
            options=self.delimiters,
            defaultValue=0,
        ))
        self.addParameter(QgsProcessingParameterString(
            self.QUOTECHAR,
            self.tr('Character used to quote columns'),
            defaultValue='"',
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            self.USE_HEADER,
            self.tr('Is the first line headers ?'),
            defaultValue=True,
        ))
        self.decimal_points = ['.', ',']
        self.addParameter(QgsProcessingParameterEnum(
            self.DECIMAL_POINT,
            self.tr('Decimal point'),
            options=self.decimal_points,
            defaultValue=0,
        ))
        self.geometry_data = [
            self.tr('WKT column'),
            self.tr('X/Y (or longitude/latitude) columns'),
            self.tr('No Geometry'),
        ]
        self.addParameter(QgsProcessingParameterEnum(
            self.GEOMETRY_DATA,
            self.tr('How geometry is given ?'),
            options=self.geometry_data,
            defaultValue=2,
        ))
        self.addParameter(QgsProcessingParameterString(
            self.WKT_FIELD,
            self.tr('Geometry column, as WKT (if WKT column selected)'),
            optional=True,
        ))
        self.addParameter(QgsProcessingParameterString(
            self.X_FIELD,
            self.tr('X/longitude column (if X/Y column selected)'),
            optional=True,
        ))
        self.addParameter(QgsProcessingParameterString(
            self.Y_FIELD,
            self.tr('Y/latitude column (if X/Y column selected)'),
            optional=True,
        ))
        self.addParameter(QgsProcessingParameterCrs(
            self.CRS,
            self.tr('CRS (if geometry given)'),
            optional=True,
        ))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT,
            self.tr('CSV layer'),
            QgsProcessing.TypeVector
        ))

    def name(self):
        """Algorithm identifier."""
        return 'loadcsvfile'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Create vector layer from CSV file')

    def groupId(self):
        """Algorithm group identifier."""
        return 'importfromcsv'

    def group(self):  # Cannot be factored in abstract class because of i18n
        """Algorithm group human name."""
        return self.tr('Import from CSV')

    def shortHelpString(self):
        """Algorithm help message displayed in the right panel."""
        return self.tr(
            "This algorithm loads a CSV file as a vector layer, with or "
            "without geometry. If present, geometry may be given as one WKT "
            "column or as two X/Y columns."
        )

    def icon(self):
        """Algorithm's icon."""
        return QIcon(':/plugins/csv_tools/load_csv.png')

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        uri = self._buildUri(parameters, context)
        vlayer = QgsVectorLayer(uri, "layername", "delimitedtext")
        if not vlayer.isValid():
            QgsMessageLog.logMessage(
                'CSV Tools: Cannot add layer with URI {}'.format(
                    vlayer.dataProvider().dataSourceUri()
                ),
                'Processing',
                Qgis.Critical
            )
            QgsMessageLog.logMessage(
                'CSV Tools: {}'.format(
                    vlayer.dataProvider().error().message()
                ),
                'Processing',
                Qgis.Critical
            )
            raise QgsProcessingException(
                '{}: {}'.format(
                    vlayer.dataProvider().dataSourceUri(),
                    vlayer.dataProvider().error().message()
                )
            )
        # We consider that having CSV data loaded is half the way
        feedback.setProgress(50)
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                                               context, vlayer.fields(),
                                               vlayer.wkbType(), vlayer.crs())
        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )
        count = vlayer.featureCount()
        total = 100.0 / count if count else 0
        features = vlayer.getFeatures()
        for i, feature in enumerate(features):
            if feedback.isCanceled():
                break
            sink.addFeature(feature, QgsFeatureSink.FastInsert)
            # Update the progress bar
            feedback.setProgress(50 + int(i * total))
        return {self.OUTPUT: dest_id}

    def _buildUri(self, parameters, context):
        """Build URI to pass to ``qgis.core.QgsVectorLayer`` from params."""
        csv_path = self.parameterAsFile(parameters, self.INPUT, context)
        delimiter = self.parameterAsEnum(parameters, self.DELIMITER, context)
        delimiter = self.delimiters[delimiter]
        quotechar = self.parameterAsString(parameters, self.QUOTECHAR, context)
        use_header = self.parameterAsBool(parameters, self.USE_HEADER,
                                          context)
        decimal_point = self.parameterAsEnum(parameters, self.DECIMAL_POINT,
                                             context)
        decimal_point = self.decimal_points[decimal_point]
        geometry_data = self.parameterAsEnum(parameters, self.GEOMETRY_DATA,
                                             context)
        wkt_field = self.parameterAsString(parameters, self.WKT_FIELD, context)
        x_field = self.parameterAsString(parameters, self.X_FIELD, context)
        y_field = self.parameterAsString(parameters, self.Y_FIELD, context)
        crs = self.parameterAsCrs(parameters, self.CRS, context)
        csv_uri_params = {
            'delimiter': delimiter,
            'quotechar': quotechar,
            'use_header': use_header,
            'decimal_point': decimal_point,
            'geometry_data': geometry_data,
            'wkt_field': wkt_field,
            'x_field': x_field,
            'y_field': y_field,
            'crs': crs.authid(),
        }
        return _qgis_csv_uri(csv_path, **csv_uri_params)
