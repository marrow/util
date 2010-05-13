# encoding: utf-8

import sys
from unittest import TestCase

from pulp.util.compat import binary, unicode
from pulp.util.path import Path


if sys.version_info >= (3, 0):
    from uni_compat3 import path_cases

else:
    from uni_compat2 import path_cases



def assert_path(instance, expected, kind=list):
    assert kind(instance.path) == expected, (kind(instance.path), expected)

def test_path_list():
    class MockOb(object):
        path = Path()
    
    cases = [
            ('/', ['', '']),
            ('/foo', ['', 'foo']),
            ('/foo/bar', ['', 'foo', 'bar']),
            ('/foo/bar/', ['', 'foo', 'bar', '']),
            ('/foo//bar/', ['', 'foo', '', 'bar', '']),
            (('foo', ), ['foo']),
            (('foo', 'bar'), ['foo', 'bar'])
        ]
    
    for case, expected in cases:
        instance = MockOb()
        instance.path = case
        
        yield assert_path, instance, expected

def test_path_str():
    class MockOb(object):
        path = Path()
    
    cases = [
            ('/', "/"),
            ('/foo', '/foo'),
            ('/foo/bar', '/foo/bar'),
            ('/foo/bar/', '/foo/bar/'),
            ('/foo//bar/', '/foo//bar/'),
            (('foo', ), 'foo'),
            (('foo', 'bar'), 'foo/bar')
        ]
    
    for case, expected in cases:
        instance = MockOb()
        instance.path = case
        
        yield assert_path, instance, expected, str
    
    instance = MockOb()
    instance.path = '/foo/bar'
    
    if sys.version_info >= (3, 0):
        yield assert_path, instance, """<Path "deque([\'\', \'foo\', \'bar\'])">""", repr
    
    else:
        yield assert_path, instance, """<Path "deque([u\'\', u\'foo\', u\'bar\'])">""", repr

def test_path_unicode():
    class MockOb(object):
        path = Path()
    
    for case, expected in path_cases:
        instance = MockOb()
        instance.path = case
        
        yield assert_path, instance, expected, unicode

class TestPaths(TestCase):
    def test_path_path(self):
        assert Path(Path('/foo')) == [unicode(''), unicode('foo')]

    def test_path_slicing(self):
        class MockOb(object):
            path = Path()
    
        instance = MockOb()
    
        instance.path = '/foo/bar/baz'
        
        self.assertEqual(instance.path[1:], unicode('foo/bar/baz'))
        self.assertEqual(instance.path[2:], unicode('bar/baz'))
        self.assertEqual(instance.path[0:2], unicode('/foo'))
        self.assertEqual(instance.path[::2], unicode('/bar'))

    def test_path_comparison(self):
        assert Path('/foo') == (unicode(''), unicode('foo')), 'tuple comparison'
        assert Path('/foo') == [unicode(''), unicode('foo')], 'list comparison'
        assert Path('/foo') == unicode('/foo'), 'string comparison'

    def test_path_join(self):
        assert Path('/foo') + Path('/bar') == Path('/foo/bar'), 'path concatenation'

    def test_path_abs(self):
        assert abs(Path('foo')) == Path('/foo')
