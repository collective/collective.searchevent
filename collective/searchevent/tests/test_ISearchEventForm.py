import unittest


class TestISearchEventForm(unittest.TestCase):

    def test_subclass(self):
        from collective.searchevent.portlets.search import ISearchEventForm
        from zope.interface import Interface
        self.assertTrue(issubclass(ISearchEventForm, Interface))

    def test_after_date(self):
        from zope.schema import Date as schema
        from collective.searchevent.portlets.search import ISearchEventForm as interface
        field = interface.get('after_date')
        self.assertTrue(isinstance(field, schema))
        self.assertEqual(field.title, u'From')
        self.assertFalse(field.required)

    def test_before_date(self):
        from zope.schema import Date as schema
        from collective.searchevent.portlets.search import ISearchEventForm as interface
        field = interface.get('before_date')
        self.assertTrue(isinstance(field, schema))
        self.assertEqual(field.title, u'To')
        self.assertFalse(field.required)

    def test_words(self):
        from zope.schema import TextLine as schema
        from collective.searchevent.portlets.search import ISearchEventForm as interface
        field = interface.get('words')
        self.assertTrue(isinstance(field, schema))
        self.assertEqual(field.title, u'Search Words')
        self.assertFalse(field.required)
