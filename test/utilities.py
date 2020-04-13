"""Common functionality used by regression tests."""

import os
import pathlib
import tempfile

from pb_tool import pb_tool
from processing.core.Processing import Processing
from qgis.core import QgsApplication
import qgis.utils


def _debug_log_message(message, tag, level):
    """Print the given log message to STDOUT."""
    print('{}({}): {}'.format(tag, level, message))


def _init_qgis_app():
    """Initialize a QGIS application and set signals to print debug messages."""
    QgsApplication.initQgis()
    QgsApplication.instance().messageLog().messageReceived.connect(_debug_log_message)


class singleton:
    """Class decorator ensuring that only one instance of the given class is ever created.

    This instance is accessed through the ``.instance()`` method of the given class.
    """

    def __init__(self, cls):
        self._cls = cls

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through the `instance()` method.')


@singleton
class QgisAppMgr:
    """Start and stop a QGIS application for testing."""

    def __init__(self):
        self._init_attrs()

    def _init_attrs(self):
        self.app = None
        self.profile_folder = None

    def start_qgis(self):
        """Start a QgsApplication without any arguments and with *GUI mode turned off*. Also call
        its initialization method.

        It will not load any plugins.

        The initialization will only happen once, so it is safe to call this method repeatedly.
        """
        if isinstance(self.app, QgsApplication):
            return
        self.profile_folder = tempfile.TemporaryDirectory(prefix='QGIS-PythonTestConfigPath')
        os.environ['QGIS_CUSTOM_CONFIG_PATH'] = self.profile_folder.name
        self.app = QgsApplication([b''], False)
        _init_qgis_app()
        print(QgsApplication.showSettings())
        Processing.initialize()
        sys_plugin_path = pathlib.Path(QgsApplication.pkgDataPath()) / 'python' / 'plugins'
        home_plugin_path = pathlib.Path(QgsApplication.qgisSettingsDirPath()) / 'python' / 'plugins'
        qgis.utils.plugin_paths.append(sys_plugin_path.as_posix())
        qgis.utils.plugin_paths.append(home_plugin_path.as_posix())
        pb_tool.deploy_files(
            config_file=(pathlib.Path(__file__).parents[1] / 'pb_tool.cfg').as_posix(),
            plugin_path='{}/'.format(home_plugin_path.as_posix()),
            user_profile=None,
            confirm=False,
        )
        qgis.utils.updateAvailablePlugins()

    def stop_qgis(self):
        """Stop the started QGIS application properly."""
        if self.app is None:
            return
        QgsApplication.exitQgis()
        self.profile_folder.cleanup()
        self._init_attrs()
