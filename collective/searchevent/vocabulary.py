from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from collective.searchevent import _
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite
from five import grok


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
                    value=items.index(item),
                    title=safe_unicode(item),
                ) for item in items
            ]
        return SimpleVocabulary(terms)


grok.global_utility(TagsVocabulary, name=u"collective.searchevent.Tags")

class FoldersVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):
        context = aq_parent(aq_parent(aq_inner(context)))
        if not IFolderish.providedBy(context):
            context = aq_parent(context)
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        query = dict(
            object_provides=IATFolder.__identifier__,
            path={'query': path, 'depth': 1},
        )
        brains = catalog(query)
        items = []
        if len(brains):
            items = [
                SimpleTerm(
                    brain.UID,
                    brain.UID,
                    brain.Title,
                ) for brain in brains
            ]
        return SimpleVocabulary(items)


FoldersVocabularyFactory = FoldersVocabulary()


# class SelectedCategoriesVocabulary(object):

#     implements(IVocabularyFactory)

#     def __call__(self, context):
#         context = aq_inner(context)
#         catalog = getToolByName(context, 'portal_catalog')
#         subjects = [item[0] for item in catalog.Indexes.get('Subject').items()]
#         items = [subjects[i] for i in context.data.categories]
#         terms = [
#             SimpleTerm(
#                 value=item,
#                 title=safe_unicode(item),
#             ) for item in items
#         ]
#         return SimpleVocabulary(terms)


# SelectedCategoriesVocabularyFactory = SelectedCategoriesVocabulary()


# class SelectedFoldersVocabulary(object):

#     implements(IVocabularyFactory)

#     def __call__(self, context):
#         context = aq_inner(context)
#         catalog = getToolByName(context, 'portal_catalog')
#         brains = catalog(UID=list(context.data.folders))
#         terms = [
#              SimpleTerm(
#                 value=brain.UID,
#                 title=safe_unicode(brain.Title),
#             ) for brain in brains
#         ]
#         terms = SimpleVocabulary(terms)

#         return SimpleVocabulary(terms)


# SelectedFoldersVocabularyFactory = SelectedFoldersVocabulary()


# class CriteriaVocabulary(object):

#     implements(IVocabularyFactory)

#     def __call__(self, context):
#         items = ['Location', 'Tags']
#         terms = [
#             SimpleTerm(
#                 value=item,
#                 title=_(item),
#             ) for item in items
#         ]
#         return SimpleVocabulary(terms)

# CriteriaVocabularyFactory = CriteriaVocabulary()


# class CollectionsVocabulary(object):

#     implements(IVocabularyFactory)

#     def __call__(self, context):
#         # context = aq_inner(context)
#         # import pdb; pdb.set_trace()
#         # context = context.context
#         portal = getSite()
#         catalog = getToolByName(portal, 'portal_catalog')
#         query = {
#             'object_provides': IATTopic.__identifier__,
#         }
#         terms = catalog(query)
#         items = terms
#         if items:
#             terms = [
#                 SimpleTerm(
#                     value=item.UID,
#                     title=item.Title,
#                 ) for item in items
#             ]
#         return SimpleVocabulary(terms)

# CollectionsVocabularyFactory = CollectionsVocabulary()


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

# RegistryCollectionsVocabularyFactory = RegistryCollectionsVocabulary()