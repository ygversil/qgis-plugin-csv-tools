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
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
    QgsVectorLayer,
)


class LoadCSVAlgorithm(QgsProcessingAlgorithm):
    """QGIS algorithm that takes a CSV file and loads it as a vector layer."""

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    DELIMITER = 'DELIMITER'
    QUOTECHAR = 'QUOTE_CHAR'
    USE_HEADER = 'USE_HEADER'

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('Input CSV file'),
                extension='csv',
            )
        )
        self.delimiters = [
            ',',
            ';',
            '|',
            't',
        ]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.DELIMITER,
                self.tr('Column delimiter'),
                options=self.delimiters,
                defaultValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.QUOTECHAR,
                self.tr('Character used to quote columns'),
                defaultValue='"',
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.USE_HEADER,
                self.tr('Is the first line headers ?'),
                defaultValue=True,
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr('Output layer'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )

    def name(self):
        """Algorithm identifier."""
        return 'loadcsvfile'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Create vector layer from CSV file')

    def group(self):
        """Algorithm group human name."""
        return self.tr('Vector creation')

    def groupId(self):
        """Algorithm group identifier."""
        return 'vectorcreation'

    def tr(self, string):
        """Helper method to mark strings for translation."""
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        """Create an instance of the algorithm."""
        return LoadCSVAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        csv_path = self.parameterAsFile(parameters, self.INPUT, context)
        delimiter = self.parameterAsEnum(parameters, self.DELIMITER, context)
        delimiter = self.delimiters[delimiter]
        quotechar = self.parameterAsString(parameters, self.QUOTECHAR, context)
        use_header = self.parameterAsBool(parameters, self.USE_HEADER,
                                          context)
        uri = ('file://{path}?delimiter={delimiter}&'
               'quote={quotechar}&'
               'useHeader={use_header}').format(
                   path=csv_path,
                   delimiter=delimiter,
                   quotechar=quotechar,
                   use_header='yes' if use_header else 'no',
               )
        vlayer = QgsVectorLayer(uri, "layername", "delimitedtext")
        return {self.OUTPUT: vlayer.id()}
