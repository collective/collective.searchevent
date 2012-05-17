import mock
import unittest2 as unittest


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
            'event_results.pt'
        )

    def test___call__(self):
        instance = self.createInstance()
        instance.index = mock.Mock()
        instance()
        instance.request.set.assert_called_with('disable_border', True)
        self.assertTrue(instance.index.called)

    def test_date__year_none(self):
        instance = self.createInstance()
        self.assertFalse(instance.date(None, None, None))

    @mock.patch('collective.searchevent.browser.template.DateTime')
    def test_date__day_none(self, DateTime):
        instance = self.createInstance()
        instance.date(2011, 10, None)
        DateTime.assert_called_with('2011/10/01')

    @mock.patch('collective.searchevent.browser.template.DateTime')
    def test_date__day_not_none(self, DateTime):
        instance = self.createInstance()
        instance.date(2011, 10, 20)
        DateTime.assert_called_with('2011/10/20')

    @mock.patch('collective.searchevent.browser.template.IATEvent')
    @mock.patch('collective.searchevent.browser.template.getToolByName')
    @mock.patch('collective.searchevent.browser.template.aq_inner')
    def test_results(self, aq_inner, getToolByName, IATEvent):
        instance = self.createInstance()
        instance.request.form = mock.MagicMock()
        instance.request.form = {
            'form.widgets.words': 'words',
            'form.widgets.categories': 'Subject',
            'form.widgets.folders': ['folder']
        }
        from DateTime import DateTime
        date = DateTime()
        instance.date = mock.Mock(return_value=date)
        IATEvent.__identifier__ = 'identifier'
        getToolByName().lookupObject().getPhysicalPath = mock.Mock(return_value=['path'])
        instance.results()
        getToolByName().assert_called_with(
            {
                'object_provides': 'identifier',
                'SearchableText': 'words',
                'sort_on': 'start',
                'sort_order': 'reverse',
                'start': {
                    'query': [date + 1, ],
                    'range': 'max',
                },
                'end': {
                    'query': [date, ],
                    'range': 'min',
                },
                'Subject': 'Subject',
                'path': ['path'],
            }
        )

    @mock.patch('collective.searchevent.browser.template.IATEvent')
    @mock.patch('collective.searchevent.browser.template.getToolByName')
    @mock.patch('collective.searchevent.browser.template.aq_inner')
    def test_results__without_subject(self, aq_inner, getToolByName, IATEvent):
        instance = self.createInstance()
        instance.request.form = mock.MagicMock()
        instance.request.form = {
            'form.widgets.words': 'words',
            'form.widgets.categories': None,
            'form.widgets.folders': ['folder']
        }
        from DateTime import DateTime
        date = DateTime()
        instance.date = mock.Mock(return_value=date)
        IATEvent.__identifier__ = 'identifier'
        getToolByName().lookupObject().getPhysicalPath = mock.Mock(return_value=['path'])
        instance.results()
        getToolByName().assert_called_with(
            {
                'object_provides': 'identifier',
                'SearchableText': 'words',
                'sort_on': 'start',
                'sort_order': 'reverse',
                'start': {
                    'query': [date + 1, ],
                    'range': 'max',
                },
                'end': {
                    'query': [date, ],
                    'range': 'min',
                },
                'path': ['path'],
            }
        )

    @mock.patch('collective.searchevent.browser.template.IATEvent')
    @mock.patch('collective.searchevent.browser.template.getToolByName')
    @mock.patch('collective.searchevent.browser.template.aq_inner')
    def test_results_without_folders(self, aq_inner, getToolByName, IATEvent):
        instance = self.createInstance()
        instance.request.form = mock.MagicMock()
        instance.request.form = {
            'form.widgets.words': 'words',
            'form.widgets.categories': 'Subject',
            'form.widgets.folders': None
        }
        from DateTime import DateTime
        date = DateTime()
        instance.date = mock.Mock(return_value=date)
        IATEvent.__identifier__ = 'identifier'
        instance.results()
        getToolByName().assert_called_with(
            {
                'object_provides': 'identifier',
                'SearchableText': 'words',
                'sort_on': 'start',
                'sort_order': 'reverse',
                'start': {
                    'query': [date + 1, ],
                    'range': 'max',
                },
                'end': {
                    'query': [date, ],
                    'range': 'min',
                },
                'Subject': 'Subject',
            }
        )

    def test_update(self):
        instance = self.createInstance()
        self.assertFalse(instance.update())
