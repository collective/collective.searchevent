import mock
import unittest2 as unittest


class TestTagsVocabulary(unittest.TestCase):

    def createInstance(self):
        from collective.searchevent.vocabulary import TagsVocabulary
        return TagsVocabulary()

    def test_instance(self):
        instance = self.createInstance()
        from collective.searchevent.vocabulary import TagsVocabulary
        self.assertTrue(isinstance(instance, TagsVocabulary))

    @mock.patch('collective.searchevent.vocabulary.SimpleVocabulary')
    @mock.patch('collective.searchevent.vocabulary.getToolByName')
    def test__call(self, getToolByName, SimpleVocabulary):
        getToolByName().Indexes = {'Subject': {'Category01': None, 'Category01': None}}
        instance = self.createInstance()
        context = mock.Mock()
        instance(context)
        self.assertTrue(SimpleVocabulary.called)
