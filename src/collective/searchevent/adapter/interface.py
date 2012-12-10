from Acquisition import aq_inner
from DateTime import DateTime
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.CMFCore.utils import getToolByName
from collective.searchevent.interfaces import ISearchEventResults
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest


class SearchEventResults(grok.MultiAdapter):
    grok.provides(ISearchEventResults)
    grok.adapts(Interface, IBrowserRequest)

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
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        form = self.request.form
        after_year = form.get('form.widgets.after_date-year', None)
        after_month = form.get('form.widgets.after_date-month', None)
        after_day = form.get('form.widgets.after_date-day', None)
        after_date = self._date(after_year, after_month, after_day)
        before_year = form.get('form.widgets.before_date-year', None)
        before_month = form.get('form.widgets.before_date-month', None)
        before_day = form.get('form.widgets.before_date-day', None)
        before_date = self._date(before_year, before_month, before_day)
        if before_date:
            before_date += 1
        if not (before_date or after_date):
            after_date = DateTime()
        query = dict(
            object_provides=IATEvent.__identifier__,
            SearchableText=form.get('form.widgets.words', ''),
            sort_on='start',
            start={
                'query': [before_date, ],
                'range': 'max',
            },
            end={
                'query': [after_date, ],
                'range': 'min',
            }
        )
        Subject = form.get('form.widgets.tags', None)
        if Subject:
            query.update({'Subject': Subject})
        paths = form.get('form.widgets.paths', paths)
        if paths:
            query.update({'path': paths})
        if limit:
            query.update({'sort_limit': limit})
        # Add b_start and b_size to the query.
        if b_size:
            query['b_start'] = b_start
            query['b_size'] = b_size + b_orphan
        brains = catalog(query)
        if limit:
            brains = brains[:limit]
        return IContentListing(brains)

    def _date(self, year, month, day):
        date = None
        if year:
            if day:
                date = '{}/{}/{}'.format(
                    year,
                    month,
                    day,
                )
            else:
                date = '{}/{}/01'.format(
                    year,
                    month,
                )
            date = DateTime(date)
        return date
