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
    @mock.patch('collective.searchevent.vocabulary.aq_parent')
    @mock.patch('collective.searchevent.vocabulary.aq_inner')
    def test__call(self, aq_inner, aq_parent, getToolByName, SimpleVocabulary):
        getToolByName().Indexes = {'Subject': {'Category01': None, 'Category01': None}}
        instance = self.createInstance()
        context = mock.Mock()
        instance(context)
        self.assertTrue(SimpleVocabulary.called)
