from collective.searchevent.interfaces import ISearchEventCollection
from five import grok
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements


class SearchEventCollection(grok.GlobalUtility):
    implements(ISearchEventCollection)

    def __call__(self, cid):
        registry = getUtility(IRegistry)
        collections = [
            col for col in registry[
                'collective.searchevent.collections'
            ] if col['id'] == cid]
        if collections:
            return collections[0]
