"""Tests for the ``csvtools`` algorithm provider.


.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'ygversil@lilo.org'
__date__ = '12/04/2020'
__copyright__ = ('Copyright 2020, Yann Voté')


import unittest

from qgis.core import QgsApplication
import qgis.utils

from . import PLUGIN_NAME, PROVIDER_ID


class NoCSVToolsProviderByDefaultTest(unittest.TestCase):
    """Test for processing when plugin has not been activated."""

    @classmethod
    def setUpClass(cls):
        cls.provider_ids = set(provider.id()
                               for provider in QgsApplication.processingRegistry().providers())

    def test_default_providers_exists(self):
        """Check that processing plugin has default providers."""
        for expected_provider_id in ('qgis', 'gdal'):
            with self.subTest(msg=expected_provider_id):
                self.assertIn(expected_provider_id, self.provider_ids)

    def test_no_csvtools_provider_by_default(self):
        """Check that processing plugin has no csvtools provider by default."""
        self.assertNotIn(PROVIDER_ID, self.provider_ids)


class CSVToolsProviderTest(unittest.TestCase):
    """Test for the ``csvtools`` processing provider."""

    @classmethod
    def setUpClass(cls):
        cls.alg_reg = QgsApplication.processingRegistry()
        qgis.utils.loadPlugin(PLUGIN_NAME)
        qgis.utils.startPlugin(PLUGIN_NAME)

    @classmethod
    def tearDownClass(cls):
        qgis.utils.unloadPlugin(PLUGIN_NAME)

    def test_provider_registered(self):
        """Check that ``csvtools`` provider is registered with Processing plugin."""
        self.assertIn(PROVIDER_ID,
                      set(provider.id() for provider in self.alg_reg.providers()))

    def test_algorithms_registered(self):
        """Check that algorithms in ``csvtools`` provider are registered in Processing plugin."""
        provider = self.alg_reg.providerById(PROVIDER_ID)
        self.assertEqual(set(alg.name() for alg in provider.algorithms()),
                         set((
                             'exportpostgresqlquerytocsv',
                             'exportsqlitequerytocsv',
                             'loadcsvfile',
                             'exportlayertocsv'
                             'attributediffbetweenlayers'
                             'attributediffwithpg'
                         )))


if __name__ == '__main__':
    unittest.main()
