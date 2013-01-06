import mock
import unittest


class TestPaths(unittest.TestCase):

    def createInstance(self):
        from collective.searchevent.portlets.search import Paths
        path = mock.Mock()
        path.id = 'PID'
        paths = [path]
        return Paths(paths)

    @mock.patch('collective.searchevent.portlets.search.getToolByName')
    def test__call__(self, getToolByName):
        instance = self.createInstance()
        context = mock.Mock()
        getToolByName().getPortalPath.return_value = 'PORTAL_PATH'
        brain = mock.Mock()
        getToolByName().return_value = [brain]
        instance(context)
