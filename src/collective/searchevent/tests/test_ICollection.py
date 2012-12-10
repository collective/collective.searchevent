import unittest


class TestICollection(unittest.TestCase):

    def test_subclass(self):
        from collective.searchevent.schema import ICollection
        from zope.interface import Interface
        self.assertTrue(issubclass(ICollection, Interface))

    def createField(self, name):
        from collective.searchevent.schema import ICollection
        return ICollection.get(name)

    def test_id__instance(self):
        from zope.schema import ASCIILine
        field = self.createField('id')
        self.assertTrue(isinstance(field, ASCIILine))

    def test_id__title(self):
        field = self.createField('id')
        self.assertEqual(field.title, u'ID')

    def test_id__description(self):
        field = self.createField('id')
        self.assertEqual(field.description, u'Shown when managing search event portlet.')

    def test_tags__instance(self):
        from zope.schema import Set
        field = self.createField('tags')
        self.assertTrue(isinstance(field, Set))

    def test_tags_title(self):
        field = self.createField('tags')
        self.assertEqual(field.title, u'Tags')

    def test_tags_description(self):
        field = self.createField('tags')
        self.assertEqual(field.description, u'Select tags to be filtered when searching events.')

    def test_tags_required(self):
        field = self.createField('tags')
        self.assertFalse(field.required)

    def test_tags__value_type(self):
        field = self.createField('tags')
        from zope.schema import Choice
        self.assertTrue(isinstance(field.value_type, Choice))

    def test_tags__value_type__vocabularyName(self):
        field = self.createField('tags')
        self.assertEqual(
            field.value_type.vocabularyName,
            u'plone.app.vocabularies.Keywords')

    def test_paths__instance(self):
        from zope.schema import Text
        field = self.createField('paths')
        self.assertTrue(isinstance(field, Text))

    def test_paths__title(self):
        field = self.createField('paths')
        self.assertEqual(field.title, u'Paths')

    def test_paths__description(self):
        field = self.createField('paths')
        self.assertEqual(field.description, u"Input path starting form '/', excluding plone root path, line by line.")

    def test_paths__required(self):
        field = self.createField('paths')
        self.assertFalse(field.required)
