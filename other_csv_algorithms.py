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

from itertools import starmap
import difflib
import io
import os
import tempfile

from PyQt5.QtGui import QIcon
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import DiffLexer
from processing import run as run_algorithm
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterExpression,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFileDestination,
    QgsSettings,
)

from .context_managers import QgisStepManager
from .qgis_version import HAS_DB_PROCESSING_PARAMETER


if not HAS_DB_PROCESSING_PARAMETER:
    from processing.tools.postgis import uri_from_name as uri_from_db_conn_name


# TODO: write tests
class AttributeDiffBetweenLayersAlgorithm(QgisAlgorithm):
    """QGIS algorithm that takes two vector layers with identical columns
    and show differences between features of these two layers."""

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    ORIG_INPUT = 'ORIG_INPUT'
    NEW_INPUT = 'NEW_INPUT'
    FIELDS_TO_COMPARE = 'FIELDS_TO_COMPARE'
    SORT_EXPRESSION = 'SORT_EXPRESSION'
    OUTPUT_HTML_FILE = 'OUTPUT_HTML_FILE'

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.ORIG_INPUT,
            self.tr('Original layer'),
            types=[QgsProcessing.TypeVector],
        ))
        self.addParameter(QgsProcessingParameterFeatureSource(
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
        self.addParameter(QgsProcessingParameterExpression(
            self.SORT_EXPRESSION,
            self.tr('Sort expression'),
            parentLayerParameterName=self.ORIG_INPUT,
            defaultValue='',
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT_HTML_FILE,
            self.tr('HTML report'),
            self.tr('HTML files (*.html)'),
            None, True
        ))

    def name(self):
        """Algorithm identifier."""
        return 'attributediffbetweenlayers'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Attribute difference between layers')

    def group(self):
        """Algorithm group human name."""
        return self.tr('Other CSV tools')

    def groupId(self):
        """Algorithm group identifier."""
        return 'othercsvtools'

    def icon(self):
        """Algorithm's icon (SVG)."""
        return QIcon(':/plugins/csv_tools/diff_files.png')

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        multi_feedback = QgsProcessingMultiStepFeedback(9, feedback)
        run_next_step = QgisStepManager(multi_feedback)
        orig_layer = self.parameterAsVectorLayer(parameters,
                                                 self.ORIG_INPUT,
                                                 context)
        sort_expression = self.parameterAsExpression(parameters, self.SORT_EXPRESSION, context)
        new_layer = self.parameterAsVectorLayer(parameters,
                                                self.NEW_INPUT,
                                                context)
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
        outputs = dict()
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as orig_csvf, \
                tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as new_csvf:
            for layer, csvf in ((orig_layer, orig_csvf), (new_layer, new_csvf)):
                with run_next_step:
                    outputs['droppedgeometries'] = run_algorithm('native:dropgeometries', {
                        'INPUT': layer,
                        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
                    }, context=context, feedback=multi_feedback, is_child_algorithm=True)
                with run_next_step:
                    outputs['refactored'] = run_algorithm('native:refactorfields', {
                        'INPUT': outputs['droppedgeometries']['OUTPUT'],
                        'FIELDS_MAPPING': [{
                            'expression': field_name,
                            'name': field_name,
                            'type': 10,
                            'length': 0,
                            'precision': 0,
                        } for field_name in fields_to_compare],
                        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
                    }, context=context, feedback=multi_feedback, is_child_algorithm=True)
                with run_next_step:
                    outputs['ordered'] = run_algorithm('native:orderbyexpression', {
                        'INPUT': outputs['refactored']['OUTPUT'],
                        'EXPRESSION': sort_expression,
                        'ASCENDING': True,
                        'NULLS_FIRST': True,
                        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
                    }, context=context, feedback=multi_feedback, is_child_algorithm=True)
                with run_next_step:
                    run_algorithm('csvtools:exportlayertocsv', {
                        'INPUT': outputs['ordered']['OUTPUT'],
                        'OUTPUT': csvf.name
                    }, context=context, feedback=multi_feedback, is_child_algorithm=True)
        with open(orig_csvf.name) as orig_csvf, \
                open(new_csvf.name) as new_csvf, \
                run_next_step:
            diff_output = difflib.unified_diff(
                orig_csvf.readlines(),
                new_csvf.readlines(),
                fromfile=orig_layer.name(),
                tofile=new_layer.name(),
            )
        results = dict()
        output_file = self.parameterAsFileOutput(parameters,
                                                 self.OUTPUT_HTML_FILE,
                                                 context)
        if output_file:
            with open(output_file, 'w') as f, io.StringIO() as diff_f:
                diff_f.writelines(diff_output)
                f.write(highlight(diff_f.getvalue(), DiffLexer(),
                                  HtmlFormatter(full=True)))
            results[self.OUTPUT_HTML_FILE] = output_file
        os.unlink(orig_csvf.name)
        os.unlink(new_csvf.name)
        return results

    def shortHelpString(self):
        return self.tr(
            "This algorithm takes two vector layers (SQLite or PostgreSQL) "
            "with common fields (those common fields being in the same order) "
            "and shows differences between features attributes in an HTML "
            "report.\n\n"
            "This can be useful to compare two versions of the same layer.\n\n"
            "Under the hood, each attribute table is converted to CSV and the "
            "two CSV files are diffed."
        )


def _connection_name_from_info(conn_info):
    settings = QgsSettings()
    settings.beginGroup('/PostgreSQL/connections/')
    for group in settings.childGroups():
        if all(starmap(
                lambda x, y: x == y,
                zip(
                    filter(
                        lambda v: not v.startswith('sslrootcert'),
                        conn_info.split()
                    ),
                    filter(
                        lambda v: not v.startswith('sslrootcert'),
                        uri_from_db_conn_name(group).connectionInfo().split()
                    )
                )
        )):
            return group
    return None
