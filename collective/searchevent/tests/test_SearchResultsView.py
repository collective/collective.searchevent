import mock
import unittest


class TestSearchResultsView(unittest.TestCase):

    def createInstance(self):
        from collective.searchevent.browser.template import SearchResultsView
        context = mock.Mock()
        request = mock.Mock()
        return SearchResultsView(context, request)

    def test_subclass(self):
        from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
        from collective.searchevent.browser.template import SearchResultsView
        self.assertTrue(SearchResultsView, ViewPageTemplateFile)

    def test_instance(self):
        instance = self.createInstance()
        from collective.searchevent.browser.template import SearchResultsView
        self.assertTrue(isinstance(instance, SearchResultsView))

    def test_index(self):
        instance = self.createInstance()
        self.assertEqual(
            instance.index.filename.split('/')[-1],
            'search_results.pt'
        )

    # def test___call__(self):
    #     instance = self.createInstance()
    #     instance.index = mock.Mock()
    #     instance()
    #     instance.request.set.assert_called_with('disable_border', True)
    #     self.assertTrue(instance.index.called)
