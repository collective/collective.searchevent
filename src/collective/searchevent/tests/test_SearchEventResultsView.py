from collective.searchevent.browser.interfaces import ISearchEventResultsView
from collective.searchevent.browser.template import SearchEventResultsView
from collective.searchevent.tests.base import IntegrationTestCase


class SearchEventResultsViewTestCase(IntegrationTestCase):
    """TestCase for SearchEventResultsView"""

    def test_subclass(self):
        from collective.base.view import BaseFormView
        self.assertTrue(SearchEventResultsView, BaseFormView)
        from collective.base.interfaces import IBaseFormView
        self.assertTrue(ISearchEventResultsView, IBaseFormView)

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(SearchEventResultsView)
        self.assertTrue(verifyObject(ISearchEventResultsView, instance))
