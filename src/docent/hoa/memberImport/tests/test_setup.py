# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from docent.hoa.memberImport.testing import DOCENT_HOA_MEMBERIMPORT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that docent.hoa.memberImport is properly installed."""

    layer = DOCENT_HOA_MEMBERIMPORT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if docent.hoa.memberImport is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'docent.hoa.memberImport'))

    def test_browserlayer(self):
        """Test that IDocentHoaMemberimportLayer is registered."""
        from docent.hoa.memberImport.interfaces import (
            IDocentHoaMemberimportLayer)
        from plone.browserlayer import utils
        self.assertIn(IDocentHoaMemberimportLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCENT_HOA_MEMBERIMPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['docent.hoa.memberImport'])

    def test_product_uninstalled(self):
        """Test if docent.hoa.memberImport is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'docent.hoa.memberImport'))

    def test_browserlayer_removed(self):
        """Test that IDocentHoaMemberimportLayer is removed."""
        from docent.hoa.memberImport.interfaces import \
            IDocentHoaMemberimportLayer
        from plone.browserlayer import utils
        self.assertNotIn(IDocentHoaMemberimportLayer, utils.registered_layers())
