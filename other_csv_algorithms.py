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

from datetime import datetime
from itertools import starmap
import abc
import difflib
import io
import os
import pathlib
import tempfile

from PyQt5.QtGui import QIcon
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import DiffLexer
from processing import run as run_algorithm
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    QgsApplication,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterExpression,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
    QgsSettings,
)

from .context_managers import QgisStepManager
from .qgis_version import HAS_DB_PROCESSING_PARAMETER


if HAS_DB_PROCESSING_PARAMETER:
    from qgis.core import (
        QgsProcessingParameterDatabaseSchema,
        QgsProcessingParameterDatabaseTable,
        QgsProcessingParameterProviderConnection,
    )
else:
    from processing.tools.postgis import uri_from_name as uri_from_db_conn_name


# TODO: write tests
class _AbstractAttributeDiffAlgorithm(QgisAlgorithm):
    """Abstract QGIS algorithm that factors in a single class code to compute attribute difference
    between two layers."""

    NEW_INPUT = 'NEW_INPUT'
    FIELDS_TO_COMPARE = 'FIELDS_TO_COMPARE'
    HIGHLIGHT_METHOD = 'HIGHLIGHT_METHOD'
    SORT_EXPRESSION = 'SORT_EXPRESSION'
    OUTPUT_HTML_FILE = 'OUTPUT_HTML_FILE'

    @abc.abstractproperty
    def step_count(self):
        return None

    @abc.abstractmethod
    def _check_fields(self):
        """Check that fields are the same."""

    @abc.abstractmethod
    def _generate_csv_files(self, orig_csvf, new_csvf):
        """Generate CSV files that are to be diffed."""

    @abc.abstractmethod
    def _orig_name(self):
        """Return the name to be used as original file in output."""

    @abc.abstractmethod
    def _read_parameters(self, parameters, context):
        """Read parameters specific to this algorithm."""

    def groupId(self):
        """Algorithm group identifier."""
        return 'othercsvtools'

    def icon(self):
        """Algorithm's icon (SVG)."""
        return QIcon(':/plugins/csv_tools/diff_files.png')

    def processAlgorithm(self, parameters, context, feedback):
        """Actual processing steps."""
        self.context = context
        self._prepare_progress_bar(feedback)
        self._read_common_parameters(parameters, context)
        self._read_parameters(parameters, context)
        self._check_fields()
        self.outputs = dict()
        self.results = dict()
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as orig_csvf, \
                tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as new_csvf:
            self._generate_csv_files(orig_csvf, new_csvf)
        with self.run_next_step:
            diff_output = _diff_csv_files(
                orig_csvf, new_csvf, self._orig_name(), self.new_layer.name(),
                method='udiff' if self.highlight_method_idx == 0 else 'ndiff'
            )
        if self.output_file:
            diff_html = _html_version(
                diff_output, method='udiff' if self.highlight_method_idx == 0 else 'ndiff'
            )
            self._create_download_report(self.output_file, diff_html)
            self.results[self.OUTPUT_HTML_FILE] = self.output_file
        os.unlink(orig_csvf.name)
        os.unlink(new_csvf.name)
        return self.results

    def _create_download_report(self, output_html_path, diff_html):
        """Create the given HTML file which is a report of found attribute differences."""
        now = datetime.now()
        tmpl_content = diff_html if diff_html else self.tr('<p>No differences found</p>')
        tmpl_path = pathlib.Path(__file__).parent / 'report_tmpl.html'
        output_html_path = pathlib.Path(output_html_path)
        with tmpl_path.open(encoding='utf-8') as tmpl, \
                output_html_path.open('w', encoding='utf-8') as f:
            f.write(tmpl.read().format(
                report_title=self.tr('Attribute difference report'),
                report_subtitle=self.tr('CSV Tools QGIS Extension'),
                now=now,
                section_title=self.tr('Differences found'),
                content=tmpl_content,
            ))

    def _layer_to_csv(self, layer, csvf):
        """Export the given layer to the given CSV file."""
        with self.run_next_step:
            self.outputs['droppedgeometries'] = run_algorithm('native:dropgeometries', {
                'INPUT': layer,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            }, context=self.context, feedback=self.multi_feedback, is_child_algorithm=True)
        with self.run_next_step:
            refactor_alg_ids = (list(filter(lambda alg: alg.id() == 'native:refactorfields',
                                            QgsApplication.processingRegistry().algorithms()))
                                or list(filter(lambda alg: alg.id() == 'qgis:refactorfields',
                                               QgsApplication.processingRegistry().algorithms())))
            refactor_alg_id = refactor_alg_ids[0]
            self.outputs['refactored'] = run_algorithm(refactor_alg_id, {
                'INPUT': self.outputs['droppedgeometries']['OUTPUT'],
                'FIELDS_MAPPING': [{
                    'expression': field_name,
                    'name': field_name,
                    'type': 10,
                    'length': 0,
                    'precision': 0,
                } for field_name in self.fields_to_compare],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            }, context=self.context, feedback=self.multi_feedback, is_child_algorithm=True)
        with self.run_next_step:
            self.outputs['ordered'] = run_algorithm('native:orderbyexpression', {
                'INPUT': self.outputs['refactored']['OUTPUT'],
                'EXPRESSION': self.sort_expression,
                'ASCENDING': True,
                'NULLS_FIRST': True,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            }, context=self.context, feedback=self.multi_feedback, is_child_algorithm=True)
        with self.run_next_step:
            run_algorithm('csvtools:exportlayertocsv', {
                'INPUT': self.outputs['ordered']['OUTPUT'],
                'OUTPUT': csvf.name
            }, context=self.context, feedback=self.multi_feedback, is_child_algorithm=True)

    def _prepare_progress_bar(self, feedback):
        """Prepare number of steps for progress bar."""
        self.multi_feedback = QgsProcessingMultiStepFeedback(self.step_count, feedback)
        self.run_next_step = QgisStepManager(self.multi_feedback)

    def _read_common_parameters(self, parameters, context):
        """Set value of parameters common to all concrete algorithms."""
        self.new_layer = self.parameterAsVectorLayer(parameters, self.NEW_INPUT, context)
        self.fields_to_compare = self.parameterAsFields(parameters, self.FIELDS_TO_COMPARE, context)
        self.sort_expression = self.parameterAsExpression(parameters, self.SORT_EXPRESSION, context)
        self.output_file = self.parameterAsFileOutput(parameters, self.OUTPUT_HTML_FILE, context)
        self.highlight_method_idx = self.parameterAsEnum(parameters, self.HIGHLIGHT_METHOD, context)


# TODO: write tests
class AttributeDiffBetweenLayersAlgorithm(_AbstractAttributeDiffAlgorithm):
    """QGIS algorithm that takes two vector layers with identical columns
    and show differences between features of these two layers."""

    ORIG_INPUT = 'ORIG_INPUT'

    @property
    def step_count(self):
        return 9

    def name(self):
        """Algorithm identifier."""
        return 'attributediffbetweenlayers'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Attribute difference between layers')

    def group(self):
        """Algorithm group human name."""
        return self.tr('Other CSV tools')

    def shortHelpString(self):
        return self.tr(
            "This algorithm takes two vector layers  with common fields (those common fields "
            "being in the same order or the result will be unreadable) and shows differences "
            "between attributes in an HTML report.\n\n"
            "This can be useful to compare two versions of the same layer.\n\n"
            "Under the hood, each attribute table is converted to CSV and the "
            "two CSV files are diffed.\n\n"
            "For the output to be correct, all lines in each CSV file must be written in the same "
            "order. Thus, a sort expression must be given. For example, it can be a key field that "
            "identifies features in each layer."
        )

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
            self.NEW_INPUT,
            allowMultiple=True,
        ))
        self.addParameter(QgsProcessingParameterEnum(
            self.HIGHLIGHT_METHOD,
            self.tr('Highlight method'),
            options=[
                self.tr('Only highlight different lines'),
                self.tr('Highligt different lines and inta-line character changes (Slower on '
                        'large layers)'),
            ],
            defaultValue=0,
        ))
        self.addParameter(QgsProcessingParameterExpression(
            self.SORT_EXPRESSION,
            self.tr('Sort expression'),
            parentLayerParameterName=self.NEW_INPUT,
            defaultValue='',
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT_HTML_FILE,
            self.tr('HTML report'),
            self.tr('HTML files (*.html)'),
            None, True
        ))

    def _check_fields(self):
        """Check that fields are the same."""
        orig_layer_fields = [field.name() for field in self.orig_layer.fields()
                             if field.name() in self.fields_to_compare]
        if orig_layer_fields != self.fields_to_compare:
            raise QgsProcessingException(self.tr(
                'Unable to compare layers with different fields or field order'
            ))

    def _orig_name(self):
        """Return the name to be used as original file in output."""
        return self.orig_layer.name()

    def _generate_csv_files(self, orig_csvf, new_csvf):
        """Generate CSV files that are to be diffed."""
        for layer, csvf in ((self.orig_layer, orig_csvf), (self.new_layer, new_csvf)):
            self._layer_to_csv(layer, csvf)

    def _read_parameters(self, parameters, context):
        """Read parameters specific to this algorithm."""
        self.orig_layer = self.parameterAsVectorLayer(parameters, self.ORIG_INPUT, context)


# TODO: write tests
class AttributeDiffWithPgAlgorithm(_AbstractAttributeDiffAlgorithm):
    """QGIS algorithm that takes a PostgreSQL/postgis table and a vector layer with identical
    columns and show differences between attributes tables."""

    DATABASE = 'DATABASE'
    SCHEMA = 'SCHEMA'
    TABLENAME = 'TABLENAME'

    @property
    def step_count(self):
        return 6

    def name(self):
        """Algorithm identifier."""
        return 'attributediffwithpg'

    def displayName(self):
        """Algorithm human name."""
        return self.tr('Attribute difference with a PostgreSQL/Postgis table')

    def group(self):
        """Algorithm group human name."""
        return self.tr('Other CSV tools')

    def shortHelpString(self):
        return self.tr(
            "This algorithm takes a vector layer and a PostgreSQL/Postgis table with common "
            "columns and shows differences between rows in an HTML report.\n\n"
            "This can be useful to compare the layer with its original version in database before "
            "submitting new or updated data to database.\n\n"
            "Under the hood, the table and attribute table are converted to CSV and the "
            "two CSV files are diffed.\n\n"
            "For the output to be correct, all lines in each CSV file must be written in the same "
            "order. Thus, a sort expression must be given. For example, it can be a key field that "
            "identifies features in each layer."
        )

    def initAlgorithm(self, config):
        """Initialize algorithm with inputs and output parameters."""
        if HAS_DB_PROCESSING_PARAMETER:
            db_param = QgsProcessingParameterProviderConnection(
                self.DATABASE,
                self.tr('PostgreSQL database (connection name)'),
                'postgres',
            )
            schema_param = QgsProcessingParameterDatabaseSchema(
                self.SCHEMA,
                self.tr('PostgreSQL schema name'),
                connectionParameterName=self.DATABASE,
                defaultValue='public',
            )
            table_param = QgsProcessingParameterDatabaseTable(
                self.TABLENAME,
                self.tr('PostgreSQL original table name'),
                connectionParameterName=self.DATABASE,
                schemaParameterName=self.SCHEMA
            )
        else:
            db_param = QgsProcessingParameterString(
                self.DATABASE,
                self.tr('PostgreSQL database (connection name)'),
            )
            db_param.setMetadata({
                'widget_wrapper': {
                    'class': 'processing.gui.wrappers_postgis.ConnectionWidgetWrapper'
                }
            })
            schema_param = QgsProcessingParameterString(
                self.SCHEMA,
                self.tr('PostgreSQL schema name'),
                'public',
                False,
                True,
            )
            schema_param.setMetadata({
                'widget_wrapper': {
                    'class': 'processing.gui.wrappers_postgis.SchemaWidgetWrapper',
                    'connection_param': self.DATABASE,
                }
            })
            table_param = QgsProcessingParameterString(
                self.TABLENAME,
                self.tr('PostgreSQL original table name'),
                '',
                False,
                True,
            )
            table_param.setMetadata({
                'widget_wrapper': {
                    'class': 'processing.gui.wrappers_postgis.TableWidgetWrapper',
                    'schema_param': self.SCHEMA,
                }
            })
        self.addParameter(db_param)
        self.addParameter(schema_param)
        self.addParameter(table_param)
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.NEW_INPUT,
            self.tr('New layer'),
            types=[QgsProcessing.TypeVector],
        ))
        self.addParameter(QgsProcessingParameterField(
            self.FIELDS_TO_COMPARE,
            self.tr('Fields to compare'),
            None,
            self.NEW_INPUT,
            allowMultiple=True,
        ))
        self.addParameter(QgsProcessingParameterEnum(
            self.HIGHLIGHT_METHOD,
            self.tr('Highlight method'),
            options=[
                self.tr('Only highlight different lines'),
                self.tr('Highligt different lines and inta-line character changes (Slower on '
                        'large layers)'),
            ],
            defaultValue=0,
        ))
        self.addParameter(QgsProcessingParameterExpression(
            self.SORT_EXPRESSION,
            self.tr('Sort expression (put in ORDER BY clause)'),
            parentLayerParameterName=self.NEW_INPUT,
            defaultValue='',
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT_HTML_FILE,
            self.tr('HTML report'),
            self.tr('HTML files (*.html)'),
            None, True
        ))

    def _check_fields(self):
        """Check that fields are the same."""
        # Not doing anything to avoid multiple requests to database.
        # If fields are not the same, SELECT request will fail.

    def _generate_csv_files(self, orig_csvf, new_csvf):
        """Generate CSV files that are to be diffed."""
        select_sql = 'select {cols} from {schema}.{table} order by {sort_exp}'.format(
            cols=', '.join(self.fields_to_compare), schema=self.schema, table=self.tablename,
            sort_exp=self.sort_expression
        )
        with self.run_next_step:
            run_algorithm('csvtools:exportpostgresqlquerytocsv', {
                'DATABASE': self.connection,
                'SELECT_SQL': select_sql,
                'OUTPUT': orig_csvf.name,
            }, context=self.context, feedback=self.multi_feedback, is_child_algorithm=True)
        self._layer_to_csv(self.new_layer, new_csvf)

    def _orig_name(self):
        """Return the name to be used as original file in output."""
        return self.tr('Table in PostgreSQL database')

    def _read_parameters(self, parameters, context):
        """Read parameters specific to this algorithm."""
        if HAS_DB_PROCESSING_PARAMETER:
            self.connection = self.parameterAsConnectionName(parameters, self.DATABASE, context)
            self.schema = self.parameterAsSchema(parameters, self.SCHEMA, context)
            self.tablename = self.parameterAsDatabaseTableName(parameters, self.TABLENAME, context)
        else:
            self.connection = self.parameterAsString(parameters, self.DATABASE, context)
            self.schema = self.parameterAsString(parameters, self.SCHEMA, context)
            self.tablename = self.parameterAsString(parameters, self.TABLENAME, context)


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


def _diff_csv_files(orig_csvf, new_csvf, orig_name, new_name, method='udiff'):
    """Compute difference between the two CSV files and return the output."""
    with open(orig_csvf.name) as orig_csvf, \
            open(new_csvf.name) as new_csvf:
        if method == 'udiff':
            diff_output = difflib.unified_diff(
                orig_csvf.readlines(),
                new_csvf.readlines(),
                fromfile=orig_name,
                tofile=new_name,
            )
        else:
            differ = difflib.HtmlDiff(tabsize=2)
            diff_output = differ.make_table(
                orig_csvf.readlines(),
                new_csvf.readlines(),
                fromdesc=orig_name,
                todesc=new_name,
                context=True,
                numlines=3,
            )
    return diff_output


def _html_version(diff_output, method='udiff'):
    """Convert the given diff output to HTML if needed."""
    with io.StringIO() as diff_f:
        diff_f.writelines(diff_output)
        diff_output = diff_f.getvalue()
    if diff_output:
        diff_html = (highlight(diff_output, DiffLexer(), HtmlFormatter(full=True))
                     if method == 'udiff'
                     else diff_output)
    else:
        diff_html = None
    return diff_html
