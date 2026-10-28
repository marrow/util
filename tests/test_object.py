# encoding: utf-8

from unittest import TestCase

from marrow.util.bunch import Bunch
from marrow.util.object import flatten, load_object, Cache, getargspec




class TestOOUtils(TestCase):
    def test_flatten(self):
        self.assertEqual(
                [i for i in flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])],
                [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
            )
    
    def test_load_object(self):
        self.failUnless(load_object('marrow.util.bunch:Bunch') is Bunch)
        self.assertRaises(AttributeError, lambda: load_object('marrow.util.bunch:Foo'))
        self.assertRaises(ImportError, lambda: load_object('marrow.foo:Bar'))


class TestGetArgSpec(TestCase):
    def test_function(self):
        def fn(a, b, c=1, *args, **kw):
            pass

        self.assertEqual(getargspec(fn), (['a', 'b', 'c'], {'c': 1}, True, True))

    def test_method(self):
        class Foo(object):
            def bar(self, a, b=2):
                pass

        self.assertEqual(getargspec(Foo().bar), (['a', 'b'], {'b': 2}, False, False))

    def test_class(self):
        class Foo(object):
            def __init__(self, a, b=2, **kw):
                pass

        class Bar(object):
            pass

        self.assertEqual(getargspec(Foo), (['a', 'b'], {'b': 2}, False, True))
        self.assertEqual(getargspec(Bar), ([], {}, False, False))

    def test_callable(self):
        class Foo(object):
            def __call__(self, a, *args):
                pass

        self.assertEqual(getargspec(Foo()), (['a'], {}, True, False))
        self.assertRaises(TypeError, getargspec, 42)


class TestOOCache(TestCase):
    def setUp(self):
        self.cache = Cache(3)

        self.cache['A'] = 0
        self.cache['B'] = 1
        self.cache['C'] = 2

    def test_basic(self):
        self.assertEqual(repr(self.cache), "{'A': 0, 'C': 2, 'B': 1}")
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
