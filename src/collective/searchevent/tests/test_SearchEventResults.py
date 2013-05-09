from collective.searchevent.adapter.interface import SearchEventResults
from collective.searchevent.interfaces import ISearchEventResults
from collective.searchevent.tests.base import IntegrationTestCase
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

import mock


class SearchEventResultsTestCase(IntegrationTestCase):
    """TestCase for SearchEventResults"""

    def test_subclass(self):
        self.assertTrue(issubclass(SearchEventResults, object))
        from zope.interface import Interface
        self.assertTrue(issubclass(ISearchEventResults, Interface))

    @mock.patch('collective.searchevent.adapter.interface.IAdapter')
    def test___call__(self, IAdapter):
        from DateTime import DateTime
        from Products.ATContentTypes.interfaces.event import IATEvent
        request = TestRequest()
        adapter = getMultiAdapter((self.portal, request), ISearchEventResults)
        request.form = {'start': '2013-05-09'}
        IAdapter().portal_path.return_value = 'PORTAL_PATH'
        adapter(limit=2)
        IAdapter().get_content_listing.assert_called_with(IATEvent,
            end={'query': [DateTime('2013-05-09')], 'range': 'min'},
            b_size=10, sort_on='start', SearchableText='',
            start={'query': [None], 'range': 'max'}, sort_limit=2, b_start=0, path='PORTAL_PATH')
