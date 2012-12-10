from collective.searchevent import _
from plone.directives import form
from zope import schema


class IAddCollection(form.Schema):

    id = schema.ASCIILine(
        title=_(u'ID'),
        description=_(u'Shown when managing search event portlet.'))

    tags = schema.Set(
        title=_(u'Tags'),
        description=_(u'Select tags to be filtered when searching events.'),
        required=False,
        value_type=schema.Choice(vocabulary=u"plone.app.vocabularies.Keywords"))

    paths = schema.Text(
        title=_(u"Paths"),
        description=_(u"Input path starting form '/', excluding plone root path, line by line."),
        required=False,
        default=u'',
        missing_value=u'')

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Number of results with which search results will be batched."),
        required=True,
        default=10,
        min=1)


class ICollection(IAddCollection):

    id = schema.ASCIILine(
        title=_(u'ID'),
        description=_(u'Shown when managing search event portlet.'),
        readonly=True)
