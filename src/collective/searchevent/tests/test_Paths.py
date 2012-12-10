import mock
import unittest


class TestPaths(unittest.TestCase):

    def createInstance(self):
        from collective.searchevent.portlets.search import Paths
        path = mock.Mock()
        path.id = 'PID'
        paths = [path]
        return Paths(paths)

    def test__call__(self):
        instance = self.createInstance()
        context = mock.Mock()
        context.portal_url.getPortalPath.return_value = 'PORTAL_PATH'
        brain = mock.Mock()
        context.portal_catalog.return_value = [brain]
        instance(context)
