import mock
import unittest


class TestSearchEventCollection(unittest.TestCase):

    def test_subclass(self):
        from collective.searchevent.utility import SearchEventCollection
        from five.grok import GlobalUtility
        self.assertTrue(SearchEventCollection, GlobalUtility)

    def createInstance(self):
        from collective.searchevent.utility import SearchEventCollection
        return SearchEventCollection()

    @mock.patch('collective.searchevent.utility.getUtility')
    def test_instance(self, getUtility):
        getUtility.return_value = {
            'collective.searchevent.collections.tags': [],
            'collective.searchevent.collections.paths': [],
            'collective.searchevent.collections.limit': [],
            }
        instance = self.createInstance()
        self.failIf(instance('cid'))
