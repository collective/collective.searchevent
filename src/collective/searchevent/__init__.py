from zope.i18nmessageid import MessageFactory


_ = MessageFactory("collective.searchevent")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
