from DateTime import DateTime
from Products.ATContentTypes.interfaces.event import IATEvent
from collective.base.interfaces import IAdapter
from collective.searchevent.interfaces import ISearchEventResults
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserRequest


class SearchEventResults(object):
    adapts(Interface, IBrowserRequest)
    implements(ISearchEventResults)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, paths=None, limit=0, b_start=0, b_size=10, b_orphan=1):
        """Returns limited number of brains.

        :param limit: Integer number.
        :type limit: int

        :param b_start: batching start.
        :type b_start: int

        :param b_size: batch size.
        :type b_size: int

        :param b_orphan: batch orphan.
        :type b_orphan: int

        :rtype: plone.app.contentlisting.contentlisting.ContentListing
        """
        form = self.request.form

        start = form.get('start')
        if start:
            start = DateTime(start)

        end = form.get('end')
        if end:
            end = DateTime(end) + 1

        if not (start or end):
            start = DateTime()

        adapter = IAdapter(self.context)

        query = dict(
            SearchableText=form.get('words', ''),
            sort_on='start',
            start={
                'query': [end, ],
                'range': 'max',
            },
            end={
                'query': [start, ],
                'range': 'min',
            },
            path=adapter.portal_path(),
        )
        Subject = form.get('tags', None)
        if Subject:
            query.update({'Subject': Subject})
        paths = form.get('paths', paths)
        if paths:
            query.update({'path': paths})
        if limit:
            query.update({'sort_limit': limit})
        # Add b_start and b_size to the query.
        if b_size:
            query['b_start'] = b_start
            query['b_size'] = b_size

        return adapter.get_content_listing(IATEvent, **query)
