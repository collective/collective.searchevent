import mock
import unittest2 as unittest


class TestFoldersVocabulary(unittest.TestCase):

    def createInstance(self):
        from collective.searchevent.vocabulary import FoldersVocabulary
        return FoldersVocabulary()

    def test_instance(self):
        instance = self.createInstance()
        from collective.searchevent.vocabulary import FoldersVocabulary
        self.assertTrue(isinstance(instance, FoldersVocabulary))

    @mock.patch('collective.searchevent.vocabulary.SimpleVocabulary')
    @mock.patch('collective.searchevent.vocabulary.getToolByName')
    @mock.patch('collective.searchevent.vocabulary.aq_parent')
    @mock.patch('collective.searchevent.vocabulary.aq_inner')
    def test__call(self, aq_inner, aq_parent, getToolByName, SimpleVocabulary):
        instance = self.createInstance()
        context = mock.Mock()
        aq_parent().getPhysicalPath.return_value = ['physical', 'path']
        brain01 = mock.Mock()
        brain02 = mock.Mock()
        getToolByName().return_value = [brain01, brain02]
        instance(context)
        self.assertTrue(SimpleVocabulary.called)
