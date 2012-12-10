from Products.CMFCore.utils import getToolByName
from collective.searchevent.tests.base import IntegrationTestCase

import logging
import mock

OLD_DATA = [{
    'id': 'ID',
    'limit': 3,
    'paths': set(['portal/path1', 'portal/path2']),
    'tags': ['tag1', 'tag2'],
}]

DATA = {
    'tags': {'ID': set(['tag1', 'tag2'])},
    'paths': {'ID': [u'/path1', u'/path2']},
    'limit': {'ID': 3},
}


class TestUpgrades(IntegrationTestCase):
    """Upgrades Test Case."""

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = getToolByName(self.portal, 'portal_setup')
        self.logger = logging.getLogger(__name__)

    def test_convert_old_data_to_new_data(self):
        from collective.searchevent.upgrades import convert_old_data_to_new_data
        self.assertEqual(convert_old_data_to_new_data(OLD_DATA), DATA)

    @mock.patch('collective.searchevent.upgrades.getUtility')
    def test_upgrade_1_to_2(self, getUtility):
        getUtility.return_value = {'collective.searchevent.collections': OLD_DATA}

        from collective.searchevent.upgrades import upgrade_1_to_2
        upgrade_1_to_2(self.portal)

        self.assertEqual(
            getUtility()['collective.searchevent.collections.tags'], {'ID': set(['tag1', 'tag2'])})
        self.assertEqual(
            getUtility()['collective.searchevent.collections.paths'], {'ID': [u'/path1', u'/path2']})
        self.assertEqual(
            getUtility()['collective.searchevent.collections.limit'], {'ID': 3})
