from Products.CMFPlone.utils import getToolByName
from collective.searchevent.schema import ICollection
from zope.interface import implements
from zope.site.hooks import getSite


class Collection(object):

    implements(ICollection)

    def __init__(self, id, tags=None, paths=None, limit=10):
        self.id = id
        self.tags = tags
        self.paths = paths
        self.limit = limit
        self.portal_catalog = self._portal_catalog()

    def _portal_catalog(self):
        """Work around for Keywords vocabulary."""
        return getToolByName(getSite(), 'portal_catalog')
