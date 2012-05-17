from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from five import grok
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite


class TagsVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getSite()
        catalog = getToolByName(context, 'portal_catalog')
        subjects = catalog.Indexes.get('Subject')
        terms = []
        if len(subjects):
            items = [item[0] for item in subjects.items()]
            terms = [
                SimpleTerm(
                    # value=items.index(item),
                    value=item,
                    title=safe_unicode(item),
                ) for item in items
            ]
        return SimpleVocabulary(terms)


grok.global_utility(TagsVocabulary, name=u"collective.searchevent.Tags")


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
                ) for item in items
            ]
        return SimpleVocabulary(terms)


grok.global_utility(RegistryCollectionsVocabulary, name=u"collective.searchevent.RegistryCollections")
