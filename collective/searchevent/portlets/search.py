from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.searchevent import _
from collective.searchevent.interfaces import ISearchEventCollection
from five import grok
from plone import directives
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


class ISearchEventPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet."),
        required=True)

    show_header = schema.Bool(
        title=_(u"Show header"),
        description=_(u"If enabled, header title will be shown."),
        required=True,
        default=True)

    collections = schema.Choice(
        title=_(u"Collections"),
        description=_(u"Select the collections for filtering search."),
        required=False,
        source="collective.searchevent.RegistryCollections")

    tags = schema.TextLine(
        title=_(u"Tags"),
        description=_(u"Label of tags field."),
        required=False,
        default=_(u'Tags'))

    folders = schema.TextLine(
        title=_(u"Folders"),
        description=_(u"Label of folders field."),
        required=False,
        default=_(u'Folders'))


class Assignment(base.Assignment):

    implements(ISearchEventPortlet)

    collections = None
    header = None
    show_header = True
    tags = _(u'Tags')
    folders = _(u'Folders')

    def __init__(self, header=None, show_header=True, collections=None,
        tags=_(u'Tags'), folders=_(u'Folders')):
        self.collections = collections
        self.header = header
        self.show_header = show_header
        self.tags = tags
        self.folders = folders

    @property
    def title(self):
        return self.header


class PortletFormView(FormWrapper):
    """ Form view which renders z3c.forms embedded in a portlet."""

    index = ViewPageTemplateFile("formwrapper.pt")


class Tags(object):
    grok.implements(IContextSourceBinder)

    def __init__(self, tags):
        self.tags = tags

    def __call__(self, context):
        terms = [
            SimpleVocabulary.createTerm(tag, str(tag), tag) for tag in list(self.tags)]
        return SimpleVocabulary(terms)


class Paths(object):

    grok.implements(IContextSourceBinder)

    def __init__(self, paths):
        self.paths = paths

    def __call__(self, context):
        portal_path = getToolByName(context, 'portal_url').getPortalPath()
        res = []
        for path in self.paths:
            if not isinstance(path, str):
                path = '{}/{}'.format(portal_path, path.id)
            res.append(path)
        self.paths = res
        catalog = getToolByName(context, 'portal_catalog')
        terms = []
        for path in self.paths:
            query = {
                'path': {
                    'query': path,
                    'depth': 0,
                }
            }
            brain = catalog(query)[0]
            title_or_id = brain.Title or brain.id
            terms.append(
                SimpleVocabulary.createTerm(
                    path, str(path), title_or_id))
        return SimpleVocabulary(terms)


class ISearchEventForm(directives.form.Schema):

    after_date = schema.Date(
        title=_(u'From'),
        required=False)

    before_date = schema.Date(
        title=_(u'To'),
        required=False)

    words = schema.TextLine(
        title=_(u"Search Words"),
        required=False)

    directives.form.order_before(words='*')
    directives.form.order_before(before_date='words')
    directives.form.order_before(after_date='before_date')


class SearchEventForm(directives.form.SchemaForm):
    grok.context(Interface)
    grok.require('zope2.View')
    directives.form.wrap(True)

    schema = ISearchEventForm
    ignoreContext = True

    def __init__(self, context, request, data=None):
        super(SearchEventForm, self).__init__(context, request)
        self.data = data
        cid = self.data.collections
        if cid:
            collection = getUtility(ISearchEventCollection)(cid)
            if collection:
                tags = collection.get('tags')
                if tags:
                    field = schema.Set(
                        title=self.data.tags,
                        required=False,
                        value_type=schema.Choice(source=Tags(tags)))
                    field.__name__ = 'tags'
                    self.fields += Fields(field)
                    self.fields['tags'].widgetFactory = CheckBoxFieldWidget
                paths = collection.get('paths')
                if paths:
                    field = schema.Set(
                        title=self.data.folders,
                        required=False,
                        value_type=schema.Choice(source=Paths(paths)))
                    field.__name__ = 'paths'
                    self.fields += Fields(field)
                    self.fields['paths'].widgetFactory = CheckBoxFieldWidget

    def updateWidgets(self):
        super(self.__class__, self).updateWidgets()
        self.widgets['words'].size = 20

    @property
    def action(self):
        """ Rewrite HTTP POST action.

        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        url = '{}/@@search-results'.format(self.context.absolute_url())
        cid = self.data.collections
        if cid:
            collection = getUtility(ISearchEventCollection)(cid)
            if collection:
                limit = collection['limit'] or 10
                url = '{}?b_size={}'.format(url, limit)
        return url

    @button.buttonAndHandler(_('Search Events'), name='search')
    def search(self, action):
        """ Form button hander. """
        data, errors = self.extractData()
        if not errors:
            pass

    @property
    def has_permission(self):
        return getSecurityManager().checkPermission(permissions.ModifyPortalContent, self.context)

    @button.buttonAndHandler(_('Export'), name='export', condition=lambda form: form.has_permission)
    def handleApply(self, action):
        """Export search event results to csv file."""


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('search.pt')

    def __init__(self, *args):
        self.assignment = args[-1]
        base.Renderer.__init__(self, *args)

    def form(self):
        form = SearchEventForm(self.context, self.request, data=self.data)
        view = PortletFormView(self.context, self.request)
        view = view.__of__(self.context)
        view.form_instance = form
        return view()

    @property
    def title(self):
        return self.assignment.show_header and self.assignment.header

    @property
    def search_results_url(self):
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        return '{}/@@search-results'.format(context_state.object_url())


class AddForm(base.AddForm):

    form_fields = form.Fields(ISearchEventPortlet)

    label = _(u"Add Event Search Portlet")
    description = _(u"This portlet displays a form to search events.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(ISearchEventPortlet)

    label = _(u"Edit Event Search Portlet")
    description = _(u"This portlet displays a form to search events.")
