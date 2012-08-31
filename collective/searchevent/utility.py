from collective.searchevent.interfaces import ISearchEventCollection
from five import grok
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements


class SearchEventCollection(grok.GlobalUtility):
    implements(ISearchEventCollection)

    def __call__(self, cid):
        registry = getUtility(IRegistry)
        tags = registry['collective.searchevent.collections.tags']
        paths = registry['collective.searchevent.collections.paths']
        limit = registry['collective.searchevent.collections.limit']
        if cid in tags:
            return {
                'tags': tags[cid],
                'paths': paths[cid],
                'limit': limit[cid],
            }
