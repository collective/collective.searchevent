from collective.searchevent.tests.base import IntegrationTestCase

# import mock


class TestSearchEventResultsViewlet(IntegrationTestCase):
    """TestCase for SearchEventResultsViewlet class."""

    def setUp(self):
        self.portal = self.layer['portal']

    def createViewlet(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        from zope.publisher.browser import TestRequest
        return SearchEventResultsViewlet(self.portal, TestRequest(), None, None)

    def test_templatedir(self):
        from collective.searchevent.browser import viewlet
        self.assertEqual(
            getattr(viewlet, 'grokcore.view.directive.templatedir'),
            'viewlets')

    def test_viewlet__subclass(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        from five.grok import Viewlet
        self.assertTrue(issubclass(SearchEventResultsViewlet, Viewlet))

    def test_viewlet__instance(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        viewlet = self.createViewlet()
        self.assertTrue(isinstance(viewlet, SearchEventResultsViewlet))

    def test_viewlet__context(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        from zope.interface import Interface
        self.assertEqual(
            getattr(SearchEventResultsViewlet, 'grokcore.component.directive.context'),
            Interface)

    def test_viewlet__name(self):
        viewlet = self.createViewlet()
        self.assertEqual(
            getattr(viewlet, 'grokcore.component.directive.name'),
            'collective.searchevent.results')

    def test_viewlet__require(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        self.assertEqual(
            getattr(SearchEventResultsViewlet, 'grokcore.security.directive.require'),
            ['zope2.View'])

    def test_viewlet__tempalate(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        self.assertEqual(
            getattr(SearchEventResultsViewlet, 'grokcore.view.directive.template'),
            'results')

    def test_viewlet__viewletmanager(self):
        from collective.searchevent.browser.viewlet import SearchEventResultsViewlet
        from collective.searchevent.browser.viewlet import SearchEventResultsViewletManager
        self.assertEqual(
            getattr(SearchEventResultsViewlet, 'grokcore.viewlet.directive.viewletmanager'),
            SearchEventResultsViewletManager)

    # def test_viewlet__date(self):
    #     """With year, month and day values."""
    #     viewlet = self.createViewlet()
    #     from DateTime import DateTime
    #     self.assertEqual(viewlet.date(2012, 01, 02), DateTime('2012/01/02'))

    # def test_viewlet__date__no_day(self):
    #     """Without day value, the day is the first day."""
    #     viewlet = self.createViewlet()
    #     from DateTime import DateTime
    #     self.assertEqual(viewlet.date(2012, 01, None), DateTime('2012/01/01'))

    # @mock.patch('collective.searchevent.browser.viewlet.DateTime')
    # @mock.patch('collective.searchevent.browser.viewlet.getToolByName')
    # def test_viewlet__results__with_limit(self, getToolByName, DateTime):
    #     """Limiting number for results."""
    #     catalog = getToolByName()
    #     catalog.return_value = [mock.Mock(), mock.Mock(), mock.Mock()]
    #     viewlet = self.createViewlet()
    #     viewlet.results(limit=2)
    #     getToolByName().assert_called_with({
    #         'SearchableText': '',
    #         'end': {'query': [DateTime()], 'range': 'min'},
    #         'object_provides': 'Products.ATContentTypes.interfaces.event.IATEvent',
    #         'sort_limit': 2,
    #         'sort_on': 'start',
    #         'start': {'query': [None], 'range': 'max'},
    #         'b_start': 0,
    #         'b_size': 11,
    #     })
