from zope.interface import Interface


class ISearchEventCollection(Interface):

    def __call__(cid):
        """Returns collection of ID cid."""
