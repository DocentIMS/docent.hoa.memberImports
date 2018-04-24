# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from docent.hoa.memberImport.interfaces import IMember
from docent.hoa.memberImport.testing import DOCENT_HOA_MEMBERIMPORT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class MemberIntegrationTest(unittest.TestCase):

    layer = DOCENT_HOA_MEMBERIMPORT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Member')
        schema = fti.lookupSchema()
        self.assertEqual(IMember, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Member')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Member')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IMember.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Member',
            id='Member',
        )
        self.assertTrue(IMember.providedBy(obj))
