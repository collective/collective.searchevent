import unittest


class TestISearchEventPortlet(unittest.TestCase):

    def test_subclass(self):
        from collective.searchevent.portlets.search import ISearchEventPortlet
        from plone.portlets.interfaces import IPortletDataProvider
        self.assertTrue(issubclass(ISearchEventPortlet, IPortletDataProvider))

    def getField(self, name):
        from collective.searchevent.portlets.search import ISearchEventPortlet
        return ISearchEventPortlet.get(name)

    def test_header__instance(self):
        from zope.schema import TextLine
        field = self.getField('header')
        self.assertTrue(isinstance(field, TextLine))

    def test_header__title(self):
        field = self.getField('header')
        self.assertEqual(field.title, u'Portlet header')

    def test_header__description(self):
        field = self.getField('header')
        self.assertEqual(
            field.description,
            u"Title of the rendered portlet."
        )

    def test_header__required(self):
        field = self.getField('header')
        self.assertTrue(field.required)

    def test_show_header__instance(self):
        from zope.schema import Bool
        field = self.getField('show_header')
        self.assertTrue(isinstance(field, Bool))

    def test_show_header__title(self):
        field = self.getField('show_header')
        self.assertEqual(field.title, u'Show header')

    def test_show_header__description(self):
        field = self.getField('show_header')
        self.assertEqual(
            field.description,
            u"If enabled, header title will be shown."
        )

    def test_show_header__required(self):
        field = self.getField('show_header')
        self.assertTrue(field.required)

    def test_collections__instance(self):
        from zope.schema import Choice
        field = self.getField('collections')
        self.assertTrue(isinstance(field, Choice))

    def test_collections__title(self):
        field = self.getField('collections')
        self.assertEqual(field.title, u'Collections')

    def test_collections__description(self):
        field = self.getField('collections')
        self.assertEqual(
            field.description,
            u"Select the collections for filtering search."
        )

    def test_collections__required(self):
        field = self.getField('collections')
        self.assertFalse(field.required)

    def test_collections__vocabularyName(self):
        field = self.getField('collections')
        self.assertEqual(
            field.vocabularyName,
            "collective.searchevent.RegistryCollections"
        )
