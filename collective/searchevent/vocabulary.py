from five import grok
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class RegistryCollectionsVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        items = registry['collective.searchevent.collections']
        terms = items
        if items:
            terms = [
                SimpleTerm(
                    value=item['id'],
                    title=item['id'],
                ) for item in items]
        return SimpleVocabulary(terms)


grok.global_utility(RegistryCollectionsVocabulary, name=u"collective.searchevent.RegistryCollections")
