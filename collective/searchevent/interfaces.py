from zope.interface import Interface


class ISearchEventCollection(Interface):

    def __call__(cid):  # pragma: no cover
        """Returns collection of ID cid."""
