from zope.interface import Interface


class ISearchEventCollection(Interface):

    def __call__(cid):  # pragma: no cover
        """Returns collection of ID cid."""


class ISearchEventResults(Interface):
    """Adapter interface to return search event results."""

    def __call__(paths=None, limit=0, b_start=0, b_size=10, b_orphan=1):  # pragma: no cover
        """Returns search event results."""


class IItemDateTime(Interface):

    def __call__():  # pragma: no cover
        """Returns localized datetime."""


class IItemText(Interface):

    def __call__():  # pragma: no cover
        """Returns item text converted from html."""
