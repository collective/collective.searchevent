from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import logging


PROFILE_ID = 'profile-collective.searchevent:default'


def convert_old_data_to_new_data(old_data):
    tags = {}
    paths = {}
    limit = {}

    for item in old_data:
        did = item['id']
        tags[did] = set(item['tags'])
        paths[did] = sorted(list(item['paths']))
        limit[did] = item['limit']
    return {
        'tags': tags,
        'paths': paths,
        'limit': limit,
    }


def upgrade_1_to_2(context, logger=None):
    """Update registry record."""
    if logger is None:
        logger = logging.getLogger(__name__)
    registry = getUtility(IRegistry)
    setup = getToolByName(context, 'portal_setup')

    logger.info('Updating collective.searchevent.collections.*.')

    data = convert_old_data_to_new_data(registry['collective.searchevent.collections'])

    setup.runImportStepFromProfile(
        PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)

    registry['collective.searchevent.collections.tags'] = data['tags']
    registry['collective.searchevent.collections.paths'] = data['paths']
    registry['collective.searchevent.collections.limit'] = data['limit']

    logger.info('Updated collective.searchevent.collections.*.')
