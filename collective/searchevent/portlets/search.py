from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.searchevent import _
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields
from z3c.form.form import Form
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.site.hooks import getSite
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ISearchEventPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet."),
        required=True,
    )

    show_header = schema.Bool(
        title=_(u"Show header"),
        description=_(u"If enabled, header title will be shown."),
        required=True,
        default=True,
    )

    # collections = schema.Set(
    #     title=_(u"Collections"),
    #     description=_(u"Select the collections for filtering search."),
    #     required=False,
    #     value_type=schema.Choice(
    #         source="collective.searchevent.RegistryCollections",
    #     )
    # )

    collections = schema.Choice(
        title=_(u"Collections"),
        description=_(u"Select the collections for filtering search."),
        required=False,
        source="collective.searchevent.RegistryCollections",
    )



class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISearchEventPortlet)

    collections = None
    header = None
    show_header = True

    def __init__(
        self,
        header=None,
        show_header=True,
        collections = None,
    ):
        self.collections = collections
        self.header = header
        self.show_header = show_header

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class PortletFormView(FormWrapper):
    """ Form view which renders z3c.forms embedded in a portlet.

    Subclass FormWrapper so that we can use custom frame template. """

    index = ViewPageTemplateFile("formwrapper.pt")


class ISearchEventForm(Interface):

    after_date = schema.Date(
        title=_(u'From'),
        required=False,
    )

    before_date = schema.Date(
        title=_(u'To'),
        required=False,
    )

    # categories = schema.Set(
    #     title=_(u'Categories'),
    #     required=False,
    #     value_type=schema.Choice(
    #         source="collective.searchevent.SelectedCategories",
    #     ),
    # )

    # folders = schema.Set(
    #     title=_(u'Folders'),
    #     required=False,
    #     value_type=schema.Choice(
    #         source="collective.searchevent.SelectedFolders",
    #     ),
    # )

    words = schema.TextLine(
        title=_(u"Search Words"),
        required=False,
    )


class SearchEventForm(Form):

    fields = Fields(ISearchEventForm)
    ignoreContext = True
    label = _(u"Search Event")

    def __init__(self, context, request, returnURLHint=None, full=True, data=None):
        """

        @param returnURLHint: Should we enforce return URL for this form

        @param full: Show all available fields or just required ones.
        """
        Form.__init__(self, context, request)
        self.all_fields = full

        self.returnURLHint = returnURLHint

        self.data = data

        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        reference = getToolByName(portal, 'reference_catalog')
        registry = getUtility(IRegistry)
        collections = registry['collective.searchevent.collections']
        # for uid in self.data.collections:
        #     collection = [col for col in collections if col.get('collection') == uid][0]
        #     criteria = collection.get('criteria')
        #     if criteria:
        #         query = {
        #             'UID': uid,
        #         }
        #         obj = reference.lookupObject(uid)
        #         if criteria == 'Location':
        #             crit = obj['crit__path_ATPathCriterion']
        #             terms = [
        #                 SimpleTerm(
        #                     value='path:{0}'.format('/'.join(ob.getPhysicalPath())),
        #                     title=ob.Title(),
        #                 ) for ob in crit.Value()
        #             ]
        #         if criteria == 'Tags':
        #             crit = obj['crit__Subject_ATSelectionCriterion']
        #             terms = [
        #                 SimpleTerm(
        #                     value=tag,
        #                     title=tag,
        #                 ) for tag in crit.Value()
        #             ]
        #         vocabulary = SimpleVocabulary(terms)
        #         field = schema.Set(
        #             title=unicode(obj.Title()),
        #             required=False,
        #             value_type=schema.Choice(
        #                 vocabulary=vocabulary,
        #             ),
        #         )
        #         field.__name__ = obj.id
        #         self.fields += Fields(field)
        #         self.fields[obj.id].widgetFactory = CheckBoxFieldWidget

    def updateWidgets(self):
        super(self.__class__, self).updateWidgets()

        # for uid in self.data.collections:
        #     import pdb; pdb.set_trace() 
        #     self.widgets[uid] = self.widgets['words']

        # if not len(self.data.categories):
        #     del self.widgets['categories']
        # if not len(self.data.folders):
        #     del self.widgets['folders']

        # category_name = self.data.category_name
        # if self.widgets.get('categories') and category_name:
        #     self.widgets['categories'].label = category_name

        # folder_name = self.data.folder_name
        # if self.widgets.get('folders') and folder_name:
        #     self.widgets['folders'].label = folder_name

        self.widgets['words'].size = 20

    # def update(self):
    #     super(self.__class__, self).update()
    #     email = schema.TextLine(title=u'E-Mail')
    #     email.__name__ = 'email'
    #     import pdb; pdb.set_trace()
    #     self.fields += Fields(email)
        # fields['categories'].widgetFactory = CheckBoxFieldWidget
        # fields['folders'].widgetFactory = CheckBoxFieldWidget

    @property
    def action(self):
        """ Rewrite HTTP POST action.

        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        return self.context.portal_url() + "/@@search-results"

    @button.buttonAndHandler(_('Search Events'), name='search')
    def search(self, action):
        """ Form button hander. """

        data, errors = self.extractData()

        if not errors:
            pass


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('search.pt')
    render = _template

    def __init__(self, *args):
        self.assignment = args[-1]
        base.Renderer.__init__(self, *args)
        self.form_wrapper = self.createForm()

    def createForm(self):
        """ Create a form instance.

        @return: z3c.form wrapped for Plone 3 view
        """

        context = self.context.aq_inner

        returnURL = self.context.absolute_url()

        # Create a compact version of the contact form
        # (not all fields visible)
        form = SearchEventForm(context, self.request, returnURLHint=returnURL, full=False, data=self.data)

        # Wrap a form in Plone view
        view = PortletFormView(context, self.request)
        view = view.__of__(context)  # Make sure acquisition chain is respected
        view.form_instance = form
        return view

    @property
    def title(self):
        return self.assignment.show_header and self.assignment.header

    @property
    def search_results_url(self):
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        url = '{0}/@@event-results'.format(context_state.object_url())
        return url


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
