from Products.CMFCore.utils import getToolByName
from collective.searchevent.interfaces import IItemDateTime
from collective.searchevent.interfaces import IItemText
from five import grok
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.memoize.instance import memoize
from zope.component.hooks import getSite


class ItemDateTime(grok.Adapter):
    grok.context(IContentListingObject)
    grok.provides(IItemDateTime)

    def __call__(self):
        start = self.context.start
        end = self.context.end
        ulocalized_time = self._ulocalized_time()
        site = getSite()
        start_dt = ulocalized_time(start, long_format=True, context=site)
        if start.Date() == end.Date():
            if start == end:
                dt = start_dt
            else:
                end_time = ulocalized_time(end, time_only=True)
                dt = u'{} - {}'.format(start_dt, end_time)
        else:
            end_dt = ulocalized_time(end, long_format=True, context=site)
            dt = u'{} - {}'.format(start_dt, end_dt)

        return dt

    @memoize
    def _ulocalized_time(self):
        """Return ulocalized_time method.

        :rtype: method
        """
        translation_service = getToolByName(getSite(), 'translation_service')
        return translation_service.ulocalized_time


class ItemText(grok.Adapter):
    grok.context(IContentListingObject)
    grok.provides(IItemText)

    def __call__(self):
        obj = self.context.getObject()
        html = obj.getField('text').get(obj)
        return self._html_to_text(html)

    @memoize
    def _html_to_text(self, html):
        transforms = getToolByName(getSite(), 'portal_transforms')
        return transforms.convert('html_to_text', html).getData()
