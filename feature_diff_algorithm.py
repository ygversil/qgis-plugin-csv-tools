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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterField,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterVectorLayer,
)


# TODO: write tests
class FeatureDiffAlgorithm(QgsProcessingAlgorithm):
    """QGIS algorithm that takes two vector layers with identical columns
    and show differences between features of these two layers."""

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    ORIG_INPUT = 'ORIG_INPUT'
    NEW_INPUT = 'NEW_INPUT'
    FIELDS_TO_COMPARE = 'FIELDS_TO_COMPARE'
    OUTPUT_HTML_FILE = 'OUTPUT_HTML_FILE'

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.ORIG_INPUT,
            self.tr('Original layer'),
            types=[QgsProcessing.TypeVector],
        ))
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.NEW_INPUT,
            self.tr('New layer'),
            types=[QgsProcessing.TypeVector],
        ))
        self.addParameter(QgsProcessingParameterField(
            self.FIELDS_TO_COMPARE,
            self.tr('Fields to compare'),
            None,
            self.ORIG_INPUT,
            allowMultiple=True,
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT_HTML_FILE,
            self.tr('HTML report'),
            self.tr('HTML files (*.html)'),
            None, True
        ))

    def name(self):
        """Algorithm identifier."""
        return 'featurediff'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Differences between features')

    def group(self):
        """Algorithm group human name."""
        return self.tr('Vector general')

    def groupId(self):
        """Algorithm group identifier."""
        return 'vectorgeneral'

    def tr(self, string):
        """Helper method to mark strings for translation."""
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        """Create an instance of the algorithm."""
        return FeatureDiffAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        orig_layer = self.parameterAsVectorLayer(parameters,
                                                 self.ORIG_INPUT,
                                                 context)
        new_layer = self.parameterAsVectorLayer(parameters,
                                                self.NEW_INPUT,
                                                context)
        # Check for SQLite or PostgreSQL or CSV type
        orig_layer_type = orig_layer.storageType()
        new_layer_type = new_layer.storageType()
        if not all(
                any(substr in type for substr in ('GPKG',
                                                  'SQLite',
                                                  'PostgreSQL'))
                for type in (orig_layer_type, new_layer_type)
        ):
            raise QgsProcessingException(self.tr(
                'Can only compare SQLite (GeoPackage, Spatialite) or '
                'PostgreSQL layers.'
            ))
        # Check that fields are the same
        fields_to_compare = self.parameterAsFields(parameters,
                                                   self.FIELDS_TO_COMPARE,
                                                   context)
        new_layer_fields = [field.name() for field in new_layer.fields()
                            if field.name() in fields_to_compare]
        if new_layer_fields != fields_to_compare:
            raise QgsProcessingException(self.tr(
                'Unable to compare layers with different fields or field order'
            ))
        results = dict()
        output_file = self.parameterAsFileOutput(parameters,
                                                 self.OUTPUT_HTML_FILE,
                                                 context)
        results[self.OUTPUT_HTML_FILE] = output_file
        return results
