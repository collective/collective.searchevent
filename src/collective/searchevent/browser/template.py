from Products.ATContentTypes import ATCTMessageFactory
from Products.ATContentTypes.content.event import ATEvent
from Products.CMFPlone import PloneMessageFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from StringIO import StringIO
from collective.base.interfaces import IAdapter
from collective.base.view import BaseFormView
from collective.searchevent import _
from collective.searchevent.browser.interfaces import ISearchEventResultsView
from collective.searchevent.collection import Collection
from collective.searchevent.interfaces import IItemText
from collective.searchevent.interfaces import ISearchEventCollection
from collective.searchevent.interfaces import ISearchEventResults
from collective.searchevent.schema import IAddCollection
from collective.searchevent.schema import ICollection
from datetime import datetime
from plone.app.z3cform.layout import wrap_form
from plone.registry.interfaces import IRegistry
from plone.z3cform.crud import crud
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements

import csv


class SearchEventControlPanelForm(crud.CrudForm):

    ignoreContext = True
    label = _(u'Event Search Collections')
    add_schema = IAddCollection
    update_schema = ICollection

    def _normalize(self, value):
        """Normalize and make it list."""
        if value:
            return [l.strip() for l in value.strip().splitlines() if l.strip()]
        else:
            return []

    def update(self):
        super(self.__class__, self).update()
        edit_forms = self.subforms[0]
        forms = edit_forms.subforms
        for form in forms:
            form.widgets['tags'].size = 5
            form.widgets['paths'].rows = 10
            form.widgets['limit'].size = 3
            registry = getUtility(IRegistry)
            paths = registry['collective.searchevent.collections.paths'][str(form.widgets['id'].value)]
            form.widgets['paths'].value = u'\n'.join(paths)
        add_form = self.subforms[1]
        add_form.widgets['id'].size = 10
        add_form.widgets['limit'].size = 3

    def update_data(self, data):
        """Add new collection data to egistry.

        :param data: Collection data.
        :type data: dict
        """
        registry = getUtility(IRegistry)
        tags = registry['collective.searchevent.collections.tags']
        paths = registry['collective.searchevent.collections.paths']
        limit = registry['collective.searchevent.collections.limit']
        did = data['id']
        tags[did] = data['tags']
        paths[did] = self._normalize(data['paths'])
        limit[did] = data['limit']
        registry['collective.searchevent.collections.tags'] = tags
        registry['collective.searchevent.collections.paths'] = paths
        registry['collective.searchevent.collections.limit'] = limit

    def add(self, data):
        """Add new collection data to collective.searchevent.collections registry.

        :param data: Collection data.
        :type data: dict
        """
        self.update_data(data)

    def get_items(self):
        """Get items to show on the form."""
        registry = getUtility(IRegistry)
        tags = registry['collective.searchevent.collections.tags']
        return [(key, Collection(key, **getUtility(ISearchEventCollection)(key))) for key in tags]

    def remove(self, (id, item)):
        """Delete collection data from collective.searchevent.collections registry.

        :param id: Unique collection id.
        :type id: str

        :param item: collective.searchevent.collection.Collection instance.
        :type id: object
        """
        registry = getUtility(IRegistry)
        del registry['collective.searchevent.collections.tags'][id]
        del registry['collective.searchevent.collections.paths'][id]
        del registry['collective.searchevent.collections.limit'][id]

    def before_update(self, item, data):
        data['id'] = item.id
        self.update_data(data)


SearchEventControlPanelView = wrap_form(
    SearchEventControlPanelForm,
    index=ViewPageTemplateFile('templates/controlpanel.pt'))


class SearchEventResultsView(BaseFormView):
    implements(ISearchEventResultsView)

    title = _(u'Search Results')

    def __call__(self):
        super(SearchEventResultsView, self).__call__()
        if self.request.form.get('form.buttons.Export', None) is not None:
            defaults_name = [
                self.context.translate(PloneMessageFactory(u'Title')),
                self.context.translate(_(u'Date')),
                self.context.translate(PloneMessageFactory(u'Description')),
                self.context.translate(PloneMessageFactory(u'Text')),
                self.context.translate(PloneMessageFactory(u'URL'))]
            extras = ['location', 'attendees', 'eventUrl', 'contactName', 'contactEmail', 'contactPhone', 'subject']
            extras_name = [self.context.translate(ATCTMessageFactory(ATEvent.schema.get(extra).widget.label)) for extra in extras]

            plone = getMultiAdapter((self.context, self.request), name="plone")
            encoding = plone.site_encoding()

            headers = tuple([header.encode(encoding) for header in (defaults_name + extras_name)])
            out = StringIO()
            writer = csv.writer(out, delimiter='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)

            adapter = IAdapter(self.context)
            for item in getMultiAdapter((self.context, self.request), ISearchEventResults)(b_size=None):
                values = [
                    item.Title(),
                    adapter.event_datetime(item).encode(encoding),
                    item.Description(),
                    IItemText(item)(),
                    item.getURL()]
                obj = item.getObject()
                for extra in extras:
                    if extra == 'attendees' or extra == 'subject':
                        value = u', '.join(getattr(obj, extra)).encode(encoding)
                    else:
                        value = getattr(obj, extra).encode(encoding)

                    values.append(value)

                writer.writerow(tuple(values))

            filename = 'search-event-results-{}.csv'.format(datetime.now().isoformat())
            cd = 'attachment; filename="{}"'.format(filename)
            self.request.response.setHeader('Content-Type', 'text/csv')
            self.request.response.setHeader("Content-Disposition", cd)
            return out.getvalue()
        else:
            return self.template()
