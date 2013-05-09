from AccessControl import getSecurityManager
from DateTime import DateTime
from Products.CMFCore import permissions
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.base.interfaces import IAdapter
from collective.searchevent import _
from collective.searchevent.interfaces import ISearchEventCollection
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements


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
        source="collective.searchevent.vocabulary.registry-collections")

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


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('search.pt')

    def __init__(self, *args):
        self.assignment = args[-1]
        base.Renderer.__init__(self, *args)

    def title(self):
        return self.assignment.show_header and self.assignment.header

    def search_results_url(self):
        url = '{}/@@search-event-results'.format(self.context.absolute_url())
        cid = self.data.collections
        if cid:
            collection = getUtility(ISearchEventCollection)(cid)
            if collection:
                limit = collection['limit'] or 10
                url = '{}?b_size={}'.format(url, limit)
        return url

    def start(self):
        form = self.request.form
        year = DateTime().year()
        return {'placeholder': '{}-01-01'.format(year), 'value': form.get('start', '')}

    def end(self):
        form = self.request.form
        year = DateTime().year()
        return {'placeholder': '{}-12-31'.format(year), 'value': form.get('end', '')}

    def words(self):
        return self.request.form.get('words', '')

    def _get_collection(self, name):
        cid = self.data.collections
        if cid:
            collection = getUtility(ISearchEventCollection)(cid)
            if collection.get(name):

                checked = self.request.form.get(name, [])
                names = []

                attr = name
                if name == 'paths':
                    attr = 'folders'
                    adapter = IAdapter(self.context)
                    portal_path = adapter.portal_path()
                    for nam in collection.get(name):
                        path = '{}{}'.format(portal_path, nam)
                        title = adapter.get_brain(path=path, depth=0).Title
                        names.append({
                            'checked': nam in checked,
                            'key': path,
                            'title': title,
                        })
                else:

                    for nam in collection.get(name):
                        names.append({'checked': nam in checked, 'key': nam})

                return {'names': names, 'title': getattr(self.data, attr)}

    def tags(self):
        return self._get_collection('tags')

    def paths(self):
        return self._get_collection('paths')

    def export_available(self):
        return getSecurityManager().checkPermission(permissions.ModifyPortalContent, self.context)


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
