from Products.ATContentTypes.interfaces.folder import IATFolder
from collective.searchevent import _
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import Interface
from zope.interface import implements
from zope.schema import ASCIILine
from zope.schema import Choice
from zope.schema import Int
from zope.schema import Set


class ICollection(Interface):

    id = ASCIILine(
        title=_(u'ID'),
    )
    tags = Set(
        title=_(u'Tags'),
        required=False,
        value_type=Choice(
            source="collective.searchevent.Tags",
        )
    )
    paths = RelationList(
        title=u"Paths",
        required=False,
        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                {'object_provides': IATFolder.__identifier__}
            ),
        ),
    )
    limit = Int(
        title=_(u"Limit"),
        description=_(u"Number of results with which search results will be batched."),
        required=True,
        default=10,
        min=1,
    )


class Collection(object):

    implements(ICollection)

    def __init__(
        self,
        id,
        tags=None,
        paths=None,
        limit=10,
    ):
        self.id = id
        self.tags = tags
        self.paths = paths
        self.limit = limit

    def __repr__(self):
        return '<Collection with id={id!r}, tags={tags!r}, paths={paths!r}, limit={limit!r}>'.format(
            id=self.id,
            tags=self.tags,
            paths=self.paths,
            limit=self.limit,
        )
