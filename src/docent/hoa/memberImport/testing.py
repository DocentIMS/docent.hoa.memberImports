# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import docent.hoa.memberImport


class DocentHoaMemberimportLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=docent.hoa.memberImport)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'docent.hoa.memberImport:default')


DOCENT_HOA_MEMBERIMPORT_FIXTURE = DocentHoaMemberimportLayer()


DOCENT_HOA_MEMBERIMPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCENT_HOA_MEMBERIMPORT_FIXTURE,),
    name='DocentHoaMemberimportLayer:IntegrationTesting'
)


DOCENT_HOA_MEMBERIMPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCENT_HOA_MEMBERIMPORT_FIXTURE,),
    name='DocentHoaMemberimportLayer:FunctionalTesting'
)


DOCENT_HOA_MEMBERIMPORT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCENT_HOA_MEMBERIMPORT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='DocentHoaMemberimportLayer:AcceptanceTesting'
)
