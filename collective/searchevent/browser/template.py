from Acquisition import aq_inner
from DateTime import DateTime
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.searchevent import _
from collective.searchevent.collection import Collection
from collective.searchevent.collection import ICollection
from plone.app.z3cform.layout import wrap_form
from plone.registry.interfaces import IRegistry
from plone.z3cform.crud import crud
from zope.component import getUtility
from Products.statusmessages.interfaces import IStatusMessage


class SearchEventControlPanelForm(crud.CrudForm):

    update_schema = ICollection

    label = _(u'Event Search Collections')

    def update(self):
        super(self.__class__, self).update()
        edit_forms = self.subforms[0]
        forms = edit_forms.subforms
        for form in forms:
            form.widgets['id'].size = 10
            form.widgets['limit'].size = 5
        add_form = self.subforms[1]
        add_form.widgets['id'].size = 10
        add_form.widgets['limit'].size = 5

    def get_items(self):
        registry = getUtility(IRegistry)
        collections = registry['collective.searchevent.collections']
        data = []
        for collection in collections:
            data.append(
                (
                    str(collection['id']),
                    Collection(
                        collection['id'],
                        collection['tags'],
                        collection['paths'],
                        collection['limit'],
                    )
                )
            )
        return data

    def add(self, data):
        """Add new collection data to collective.searchevent.collections registry.

        :param data: Collection data.
        :type data: dict
        """
        registry = getUtility(IRegistry)
        collections = registry['collective.searchevent.collections']
        ids = [item['id'] for item in collections]
        if data['id'] not in ids:
            data.update({'paths': self.request.form.get('crud-add.form.widgets.paths')})
            collections.append(data)
            registry['collective.searchevent.collections'] = collections
        else:
            message = _(u"You cannot add another collection with the same ID.")
            IStatusMessage(self.request).addStatusMessage(message, type='warn')

    def remove(self, (id, item)):
        """Delete collection data from collective.searchevent.collections registry.

        :param id: Unique collection id.
        :type id: str

        :param item: collective.searchevent.collection.Collection instance.
        :type id: object
        """
        registry = getUtility(IRegistry)
        collections = registry['collective.searchevent.collections']
        collections = [collection for collection in collections if collection['id'] != id]
        registry['collective.searchevent.collections'] = collections

    def before_update(self, item, data):
        registry = getUtility(IRegistry)
        collections = registry['collective.searchevent.collections']
        collections = [collection for collection in collections if collection['id'] != data['id']]
        collections.append(data)
        registry['collective.searchevent.collections'] = collections


SearchEventControlPanelView = wrap_form(
    SearchEventControlPanelForm,
    index=ViewPageTemplateFile('templates/controlpanel.pt')
)


class SearchResultsView(BrowserView):

    index = ViewPageTemplateFile('templates/search_results.pt')

    def __call__(self):
        self.request.set('disable_border', True)
        return self.index()

    def date(self, year, month, day):
        date = None
        if year:
            if day:
                date = '{0}/{1}/{2}'.format(
                    year,
                    month,
                    day,
                )
            else:
                date = '{0}/{1}/01'.format(
                    year,
                    month,
                )
            date = DateTime(date)
        return date

    def results(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        form = self.request.form
        after_year = form.get('form.widgets.after_date-year', None)
        after_month = form.get('form.widgets.after_date-month', None)
        after_day = form.get('form.widgets.after_date-day', None)
        after_date = self.date(after_year, after_month, after_day)
        before_year = form.get('form.widgets.before_date-year', None)
        before_month = form.get('form.widgets.before_date-month', None)
        before_day = form.get('form.widgets.before_date-day', None)
        before_date = self.date(before_year, before_month, before_day)
        if before_date:
            before_date += 1
        if not (before_date or after_date):
            after_date = DateTime()
        query = dict(
            object_provides=IATEvent.__identifier__,
            SearchableText=form.get('form.widgets.words', ''),
            sort_on='start',
            start={
                'query': [before_date, ],
                'range': 'max',
            },
            end={
                'query': [after_date, ],
                'range': 'min',
            }
        )
        Subject = form.get('form.widgets.tags', None)
        if Subject:
            query.update({'Subject': Subject})
        paths = form.get('form.widgets.paths', None)
        if paths:
            query.update({'path': paths})
        return catalog(query)

    def batch(self):
        form = self.request.form
        b_start = form.get('b_start', 0)
        b_size = int(form.get('b_size', '10'))
        return Batch(
            self.results(),
            b_size,
            start=b_start,
            orphan=1,
        )

    def update(self):
        """We need this method for plone.app.z3cform.kss.validation.validate_input"""
        pass
