from Acquisition import aq_inner
from DateTime import DateTime
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.memoize.instance import memoize
from zope.interface import Interface
import csv
import tempfile
from StringIO import StringIO


grok.templatedir('viewlets')


class SearchEventResultsViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager to list search results."""
    grok.context(Interface)
    grok.name('collective.searchevent.results.manager')


class BaseSearchEventViewlet(grok.Viewlet):
    """Base class for viewlet."""
    grok.baseclass()
    grok.context(Interface)
    grok.viewletmanager(SearchEventResultsViewletManager)

    def date(self, year, month, day):
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

    def results(self, paths=None, limit=0, b_start=0, b_size=10, b_orphan=1):
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
        after_date = self.date(after_year, after_month, after_day)
        before_year = form.get('form.widgets.before_date-year', None)
        before_month = form.get('form.widgets.before_date-month', None)
        before_day = form.get('form.widgets.before_date-day', None)
        before_date = self.date(before_year, before_month, before_day)
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


class SearchEventResultsViewlet(BaseSearchEventViewlet):
    """Search event results Viewlet Class."""
    grok.require('zope2.View')
    grok.template('results')
    grok.name('collective.searchevent.results')

    def batch(self):
        form = self.request.form
        b_start = int(form.get('b_start', '0'))
        b_size = int(form.get('b_size', '10'))
        b_orphan = 1
        return Batch(
            self.results(b_start=b_start, b_size=b_size),
            b_size,
            start=b_start,
            orphan=b_orphan)

    @memoize
    def _ulocalized_time(self):
        """Return ulocalized_time method.

        :rtype: method
        """
        translation_service = getToolByName(self.context, 'translation_service')
        return translation_service.ulocalized_time

    def datetime(self, item):
        start = item.start
        end = item.end
        ulocalized_time = self._ulocalized_time()
        start_dt = ulocalized_time(start, long_format=True, context=self.context)
        if start.Date() == end.Date():
            if start == end:
                dt = start_dt
            else:
                end_time = ulocalized_time(end, time_only=True)
                dt = u'{} - {}'.format(start_dt, end_time)
        else:
            end_dt = ulocalized_time(end, long_format=True, context=self.context)
            dt = u'{} - {}'.format(start_dt, end_dt)

        return dt


class ExportSearchEventResultsViewlet(BaseSearchEventViewlet):
    """Viewlet Class for exporting search event results in csv mode."""
    grok.require('cmf.ModifyPortalContent')
    grok.template('export')
    grok.name('collective.searchevent.export')

    def events(self):
        return self.results(b_size=None)

    def update(self):
        if self.request.form.get('form.export', None) is not None:
            out = StringIO()
            writer = csv.writer(out)
            writer.writerow(('Email address', 'Subject'))
            filename = 'test.csv'
            cd = 'attachment; filename="{}"'.format(filename)
            self.request.response.setHeader('Content-Type', 'text/csv')
            self.request.response.setHeader("Content-Disposition", cd)
            return out.getvalue()
            # for item in self.results(b_size=None):

