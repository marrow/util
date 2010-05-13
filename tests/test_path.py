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

def test_path_path():
    assert Path(Path('/foo')) == ['', 'foo']

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

def test_path_slicing():
    class MockOb(object):
        path = Path()
    
    instance = MockOb()
    
    instance.path = '/foo/bar/baz'
    
    assert str(instance.path[1:]) == 'foo/bar/baz'
    assert str(instance.path[2:]) == 'bar/baz'
    assert str(instance.path[0:2]) == '/foo'
    assert str(instance.path[::2]) == '/bar'

def test_path_comparison():
    assert Path('/foo') == ('', 'foo'), 'tuple comparison'
    assert Path('/foo') == ['', 'foo'], 'list comparison'
    assert Path('/foo') == '/foo', 'string comparison'

def test_path_join():
    assert Path('/foo') + Path('/bar') == Path('/foo/bar'), 'path concatenation'

def test_path_abs():
    assert abs(Path('foo')) == Path('/foo')
