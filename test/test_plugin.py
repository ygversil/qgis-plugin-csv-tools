"""Tests to check if the ``csv_tools`` plugin is correctly loaded.


.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'ygversil@lilo.org'
__date__ = '13/04/2020'
__copyright__ = ('Copyright 2020, Yann Voté')


from contextlib import contextmanager
import unittest

import qgis.utils

from . import PLUGIN_NAME


@contextmanager
def _activate_plugin(plugin_name):
    """Context manager that starts a plugin on enter and ensure that it is deactivated on exit."""
    qgis.utils.loadPlugin(plugin_name)
    qgis.utils.startPlugin(plugin_name)
    yield
    qgis.utils.unloadPlugin(plugin_name)


class CSVToolsPluginTest(unittest.TestCase):
    """Test if the ``csv_tools`` plugin can be loaded."""

    def test_available_plugin(self):
        """Check that ``csv_tools`` plugin is in available plugins."""
        self.assertIn(PLUGIN_NAME, qgis.utils.available_plugins)

    def test_active_plugin_on_start(self):
        """Check that ``csv_tools`` plugin is in active plugins when activated."""
        with _activate_plugin(PLUGIN_NAME):
            self.assertIn(PLUGIN_NAME, qgis.utils.active_plugins)
        self.assertNotIn(PLUGIN_NAME, qgis.utils.active_plugins)


if __name__ == '__main__':
    unittest.main()
