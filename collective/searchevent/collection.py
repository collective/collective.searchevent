from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFPlone.utils import getToolByName
from collective.searchevent import _
from plone.directives.form import Schema
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import implements
from zope.schema import ASCIILine
from zope.schema import Choice
from zope.schema import Int
from zope.schema import Set
from zope.site.hooks import getSite


class IAddCollection(Schema):

    id = ASCIILine(
        title=_(u'ID'),
        description=_(u'Shown when managing search event portlet.'))

    tags = Set(
        title=_(u'Tags'),
        description=_(u'Select tags to be filtered when searching events.'),
        required=False,
        value_type=Choice(vocabulary=u"plone.app.vocabularies.Keywords"))

    paths = RelationList(
        title=_(u"Paths"),
        description=_(u"Select paths to be filtered when searching events. Only top level folders can be used."),
        required=False,
        missing_value=[],
        value_type=RelationChoice(
            source=ObjPathSourceBinder(object_provides=IATFolder.__identifier__)))

    limit = Int(
        title=_(u"Limit"),
        description=_(u"Number of results with which search results will be batched."),
        required=True,
        default=10,
        min=1)


class ICollection(IAddCollection):

        id = ASCIILine(
        title=_(u'ID'),
        description=_(u'Shown when managing search event portlet.'),
        readonly=True)


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
