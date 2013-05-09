from Products.CMFCore.utils import getToolByName
from collective.searchevent.interfaces import IItemText
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.memoize.instance import memoize
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import implements


class ItemText(object):
    adapts(IContentListingObject)
    implements(IItemText)

    def __call__(self):
        obj = self.context.getObject()
        html = obj.getField('text').get(obj)
        return self._html_to_text(html)

    def __init__(self, context):
        self.context = context

    @memoize
    def _html_to_text(self, html):
        transforms = getToolByName(getSite(), 'portal_transforms')
        return transforms.convert('html_to_text', html).getData()
