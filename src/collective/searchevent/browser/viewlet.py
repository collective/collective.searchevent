from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.base.interfaces import IAdapter
from collective.searchevent import _
from collective.searchevent.browser.interfaces import ISearchEventResultsViewlet
from collective.searchevent.interfaces import ISearchEventResults
from plone.app.layout.viewlets.common import ViewletBase
from plone.batching.batch import Batch
from zope.component import getMultiAdapter
from zope.interface import implements


class BaseSearchEventViewlet(ViewletBase):
    """Base class for viewlet."""

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
    implements(ISearchEventResultsViewlet)
    index = ViewPageTemplateFile('viewlets/search-event-results.pt')

    def batch(self):
        form = self.request.form
        b_start = int(form.get('b_start', '0'))
        b_size = int(form.get('b_size', '10'))
        b_orphan = 1
        try:
            return Batch(self.results(b_start=b_start, b_size=b_size), b_size, start=b_start, orphan=b_orphan)
        except:
            message = _(u'input_date_format', default=u'Input date format: YEAR-MONTH-DAY like 2013-01-01.')
            IStatusMessage(self.request).addStatusMessage(message, type="info")
            url = self.context.restrictedTraverse('@@plone_context_state').current_base_url()
            self.request.response.redirect(url)

    def datetime(self, item):
        return IAdapter(self.context).event_datetime(item)
