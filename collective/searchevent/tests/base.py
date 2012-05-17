from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import unittest2 as unittest


class CollectiveEvent_Search_PortletLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import collective.searchevent
        self.loadZCML(package=collective.searchevent)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.searchevent:default')

    def tearDownZope(self, app):
        """Tear down Zope."""


FIXTURE = CollectiveEvent_Search_PortletLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="CollectiveEvent_Search_PortletLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="CollectiveEvent_Search_PortletLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
