from Products.CMFCore.utils import getToolByName
from collective.searchevent.tests.base import IntegrationTestCase


def get_css_resource(obj, name):
    return getToolByName(obj, 'portal_css').getResource(name)


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_package_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('collective.searchevent'))

    def test_browserlayer(self):
        from collective.searchevent.browser.interfaces import ISearchEventLayer
        from plone.browserlayer import utils
        self.failUnless(ISearchEventLayer in utils.registered_layers())

    def test_cssregistry__main__applyPrefix(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertTrue(resource.getApplyPrefix())

    def test_cssregistry__main__authenticated(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertFalse(resource.getAuthenticated())

    def test_cssregistry__main__compression(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertEqual(resource.getCompression(), 'safe')

    def test_cssregistry__main__conditionalcomment(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertEqual(resource.getConditionalcomment(), '')

    def test_cssregistry__main__cookable(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertTrue(resource.getCookable())

    def test_cssregistry__main__enabled(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertTrue(resource.getEnabled())

    def test_cssregistry__main__expression(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertEqual(resource.getExpression(), '')

    def test_cssregistry__main__media(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertEqual(resource.getMedia(), 'screen')

    def test_cssregistry__main__rel(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertEqual(resource.getRel(), 'stylesheet')

    def test_cssregistry__main__rendering(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertEqual(resource.getRendering(), 'link')

    def test_cssregistry__main__title(self):
        resource = get_css_resource(self.portal, '++resource++collective.searchevent/css/main.css')
        self.assertIsNone(resource.getTitle())

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

    def test_metadata__dependency__plone_formwidget_datetime(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.formwidget.datetime'))

    def test_metadata__dependency__plone_app_relatedfield(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('plone.app.relationfield'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-collective.searchevent:default'),
            u'3')

    def get_record(self, name):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        return getUtility(IRegistry).records.get(name)

    def test_registry__tags(self):
        from plone.registry.field import Dict
        record = self.get_record('collective.searchevent.collections.tags')
        self.assertIsInstance(record.field, Dict)

    def test_registry__tags__key_type(self):
        from plone.registry.field import ASCIILine
        record = self.get_record('collective.searchevent.collections.tags')
        self.assertIsInstance(record.field.key_type, ASCIILine)

    def test_registry__tags__value_type(self):
        from plone.registry.field import Set
        record = self.get_record('collective.searchevent.collections.tags')
        self.assertIsInstance(record.field.value_type, Set)

    def test_registry__paths(self):
        from plone.registry.field import Dict
        record = self.get_record('collective.searchevent.collections.paths')
        self.assertIsInstance(record.field, Dict)

    def test_registry__paths__key_type(self):
        from plone.registry.field import ASCIILine
        record = self.get_record('collective.searchevent.collections.paths')
        self.assertIsInstance(record.field.key_type, ASCIILine)

    def test_registry__paths__value_type(self):
        from plone.registry.field import List
        record = self.get_record('collective.searchevent.collections.paths')
        self.assertIsInstance(record.field.value_type, List)

    def test_registry__limit(self):
        from plone.registry.field import Dict
        record = self.get_record('collective.searchevent.collections.limit')
        self.assertIsInstance(record.field, Dict)

    def test_registry__limit__key_type(self):
        from plone.registry.field import ASCIILine
        record = self.get_record('collective.searchevent.collections.limit')
        self.assertIsInstance(record.field.key_type, ASCIILine)

    def test_registry__limit__value_type(self):
        from plone.registry.field import Int
        record = self.get_record('collective.searchevent.collections.limit')
        self.assertIsInstance(record.field.value_type, Int)

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

    def test_unintall__registry__tags(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        self.assertIsNone(self.get_record('collective.searchevent.collections.tags'))

    def test_unintall__registry__paths(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        self.assertIsNone(self.get_record('collective.searchevent.collections.paths'))

    def test_unintall__registry__limit(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['collective.searchevent'])
        self.assertIsNone(self.get_record('collective.searchevent.collections.limit'))
