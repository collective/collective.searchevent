# -*- coding: utf-8 -*-
import unittest2 as unittest


class TestCollection(unittest.TestCase):

    def createInstance(self, id="ID", tags=["TAG01", "TAG02"], paths=['PATH01', 'PATH02'], limit=10):
        from collective.searchevent.collection import Collection
        return Collection(id, tags, paths, limit)

    def test_instance(self):
        item = self.createInstance()
        from collective.searchevent.collection import Collection
        self.assertTrue(isinstance(item, Collection))

    def test_verifyObject(self):
        instance = self.createInstance()
        from collective.searchevent.collection import ICollection
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(ICollection, instance))

    def test__repr__(self):
        item = self.createInstance()
        self.assertEqual(
            item.__repr__(),
            "<Collection with id='ID', tags=['TAG01', 'TAG02'], paths=['PATH01', 'PATH02'], limit=10>"
        )
