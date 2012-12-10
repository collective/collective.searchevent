from Products.CMFPlone.PloneBatch import Batch
from collective.searchevent.interfaces import IItemDateTime
from collective.searchevent.interfaces import ISearchEventResults
from five import grok
from plone.app.viewletmanager.manager import OrderedViewletManager
from zope.component import getMultiAdapter
from zope.interface import Interface


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
        return getMultiAdapter(
            (self.context, self.request), ISearchEventResults)(
                paths=paths, limit=limit, b_start=b_start, b_size=b_size, b_orphan=b_orphan)


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

    def datetime(self, item):
        return IItemDateTime(item)()
