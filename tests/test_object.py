# encoding: utf-8

from unittest import TestCase

from marrow.util.bunch import Bunch
from marrow.util.object import flatten, load_object, Cache




class TestOOUtils(TestCase):
    def test_flatten(self):
        self.assertEqual(
                [i for i in flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])],
                [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
            )
    
    def test_load_object(self):
        self.assertTrue(load_object('marrow.util.bunch:Bunch') is Bunch)
        self.assertRaises(AttributeError, lambda: load_object('marrow.util.bunch:Foo'))
        self.assertRaises(ImportError, lambda: load_object('marrow.foo:Bar'))

    def test_load_object_entry_point(self):
        from marrow.util import object as object_module

        expected = object()

        class EntryPoint:
            name = 'sample'

            def load(self):
                return expected

        class EntryPoints(list):
            def select(self, **filters):
                self.filters = filters
                return self

        points = EntryPoints([EntryPoint()])
        original = object_module.entry_points
        object_module.entry_points = lambda: points
        try:
            self.assertIs(load_object('sample', 'example.plugins'), expected)
            self.assertEqual(points.filters, {'group': 'example.plugins'})
        finally:
            object_module.entry_points = original

    def test_load_object_missing_entry_point(self):
        from marrow.util import object as object_module

        class EntryPoints(list):
            def select(self, **filters):
                return self

        original = object_module.entry_points
        object_module.entry_points = EntryPoints
        try:
            with self.assertRaisesRegex(ValueError, 'Unknown plugin'):
                load_object('missing', 'example.plugins')
        finally:
            object_module.entry_points = original


class TestOOCache(TestCase):
    def setUp(self):
        self.cache = Cache(3)

        self.cache['A'] = 0
        self.cache['B'] = 1
        self.cache['C'] = 2

    def test_basic(self):
        self.assertEqual(repr(self.cache), "{'A': 0, 'B': 1, 'C': 2}")
        self.assertEqual(len(self.cache), 3)
        self.assertEqual(self.cache['A'], 0)

    def test_overflow(self):
        self.cache['D'] = 3

        self.assertEqual(len(self.cache), 3)
        self.assertFalse('A' in self.cache)

    def test_sort(self):
        self.cache['E'] = 4
        self.cache['B']

        self.assertEqual([i for i in self.cache], ['B', 'E', 'C'])

    def test_reassignment(self):
        self.cache['A'] = 5
        self.assertEqual(self.cache['A'], 5)
        self.assertEqual([i for i in self.cache], ['A', 'C', 'B'])

        self.cache['C'] = 6
        self.assertEqual(self.cache['C'], 6)
        self.assertEqual([i for i in self.cache], ['C', 'A', 'B'])

    def test_capacity(self):
        self.cache.capacity = 1
        self.cache._restrict()

        self.assertEqual(len(self.cache), 1)
        self.assertFalse('A' in self.cache)
        self.assertTrue('C' in self.cache)

        self.cache['A'] = 0
        self.assertEqual(len(self.cache), 1)
        self.assertTrue('A' in self.cache)
        self.assertFalse('C' in self.cache)

        self.cache.capacity = 0
        self.cache._restrict()

        self.assertEqual(len(self.cache), 0)
