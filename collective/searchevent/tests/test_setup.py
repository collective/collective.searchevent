from collective.searchevent.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_collective_searchevent_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('collective.searchevent'))

    def test_is_plone_formwidget_datetime_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.formwidget.datetime'))

    def test_browserlayer(self):
        from collective.searchevent.browser.interfaces import ISearchEventLayer
        from plone.browserlayer import utils
        self.failUnless(ISearchEventLayer in utils.registered_layers())

    def test_controlpanel(self):
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        action = [
            action for action in controlpanel.listActions() if action.id == 'searchevent_collection_registry'
        ][0]
        self.assertEqual(action.title, 'Search Event Collections')
        self.assertEqual(action.appId, 'collective.searchevent')
        self.assertEqual(action.action.text, 'string:${portal_url}/@@searchevent-controlpanel')
        self.assertEqual(action.icon_expr.text, 'string:${portal_url}/maintenance_icon.png')
        self.assertTrue(action.visible)
        self.assertEqual(action.permissions, ('Manage portal',))

    def test_registry__collections(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        self.assertEqual(len(registry['collective.searchevent.collections']), 0)

    def test_registry__collections__instance(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        field = getUtility(IRegistry).records[
            'collective.searchevent.collections'
        ].field
        from plone.registry.field import List
        self.assertTrue(isinstance(field, List))

    def test_registry__collections__title(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        field = getUtility(IRegistry).records[
            'collective.searchevent.collections'
        ].field
        self.assertEqual(field.title, u'Collections')

    def test_registry__collections__description(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        field = getUtility(IRegistry).records[
            'collective.searchevent.collections'
        ].field
        self.assertEqual(field.description, u'List of Collection Data.')

    def test_registry__collections__value_type(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        field = getUtility(IRegistry).records[
            'collective.searchevent.collections'
        ].field
        from plone.registry.field import Dict
        self.assertTrue(isinstance(field.value_type, Dict))

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        self.failIf(installer.isProductInstalled('collective.searchevent'))

    def test_uninstall__browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        from collective.searchevent.browser.interfaces import ISearchEventLayer
        from plone.browserlayer import utils
        self.failIf(ISearchEventLayer in utils.registered_layers())

    def test_uninstall__controlpanel(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        actions = [
            action.id for action in controlpanel.listActions()
        ]
        self.assertFalse('searchevent_collection_registry' in actions)

    def test_unintall__registry__collections(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        self.assertRaises(
            KeyError,
            lambda: registry['collective.searchevent.collections']
        )
