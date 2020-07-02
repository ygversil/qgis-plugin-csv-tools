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


from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .resources import *  # noqa
from .import_from_csv_algorithms import LoadCSVAlgorithm
from .export_to_csv_algorithms import (
    ExportLayerToCsv,
    ExportPostgreSQLQueryToCsv,
    ExportSQLiteQueryToCsv,
)
from .other_csv_algorithms import FeatureDiffAlgorithm


class CSVToolsProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(ExportLayerToCsv())
        self.addAlgorithm(ExportPostgreSQLQueryToCsv())
        self.addAlgorithm(ExportSQLiteQueryToCsv())
        self.addAlgorithm(FeatureDiffAlgorithm())
        self.addAlgorithm(LoadCSVAlgorithm())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'csvtools'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('CSV Tools')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()

    def icon(self):
        """The provider's icon."""
        return QIcon(':/plugins/csv_tools/csv.svg')

    def svgIconPath(self):
        """The provider's icon."""
        return QIcon(':/plugins/csv_tools/csv.svg')
