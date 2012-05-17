from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

EXTENSION_PROFILE = ('profile-collective.searchevent:uninstall',)


def uninstall(self):
    out = StringIO()
    print >> out, "Removing collective.searchevent."

    setup = getToolByName(self, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        profile,
        purge_old=False,
    )

    print >> out, "Removed collective.searchevent."

    return out.getvalue()