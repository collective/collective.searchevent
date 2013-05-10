from collective.base.interfaces import IBaseFormView
from collective.base.interfaces import IViewlet
from zope.interface import Interface


# Browser layer

class ISearchEventLayer(Interface):
    """Marker interface for browserlayer."""


# View

class ISearchEventResultsView(IBaseFormView):
    """View interface for SearchEventResultsView"""


# Viewlet

class ISearchEventResultsViewlet(IViewlet):
    """Viewlet interface for SearchEventResultsViewlet"""


    def batch():
        """Returns batch"""

    def datetime(item):
        """Returns localized date time for event"""
