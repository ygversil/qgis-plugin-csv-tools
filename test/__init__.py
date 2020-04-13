# import qgis libs so that ve set the correct sip api version
import qgis   # pylint: disable=W0611  # NOQA

import atexit

from .utilities import QgisAppMgr

PLUGIN_NAME = 'csv_tools'
PROVIDER_ID = 'csvtools'


def setUpModule():
    qgis_mgr = QgisAppMgr.instance()
    qgis_mgr.start_qgis()
    atexit.register(qgis_mgr.stop_qgis)


def tearDownModule():
    qgis_mgr = QgisAppMgr.instance()
    qgis_mgr.stop_qgis()
