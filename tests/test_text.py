# encoding: utf-8

from unittest import TestCase

from marrow.util.text import *



NORMALIZE_BASIC_EXISTING = ["test", "test-1", "foo-2"]
NORMALIZE_BASIC_PAIRS = [
        ('Foo!', 'foo'),
        ('Hello world', 'hello-world'),
        ('Bad  String', 'bad-string'),
        ('Test', 'test-2'),
        ('foo', 'foo')
    ]


def assert_normalized(testing, expected):
    assert normalize(testing, NORMALIZE_BASIC_EXISTING) == expected, "Expected '%s', returned '%s'." % (expected, normalize(testing, NORMALIZE_BASIC_EXISTING))

def test_normalize_basic():
    for i, o in NORMALIZE_BASIC_PAIRS:
        yield assert_normalized, i, o



ELLIPSIS_BASIC_PAIRS = [
        ('This is a test.', 'This is a test.'),
        ('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod.', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do...'),
        ('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do. eiusmod', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do...'),
        ('Loremipsumdolorsitamet,consecteturadipisicingelit,seddoeiusmodtemporincididunt', 'Loremipsumdolorsitamet,consecteturadipisicingelit,seddoeiusmodtemporinci...')
    ]


def assert_truncated(testing, expected):
    assert ellipsis(testing, 72) == expected, "Expected '%s', returned '%s'." % (expected, ellipsis(testing, 72))

def test_truncated_basic():
    for i, o in ELLIPSIS_BASIC_PAIRS:
        yield assert_truncated, i, o



WRAP_BASIC_PAIRS = [
        ('This is a test.', 'This is a test.'),
        ('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod.', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do\neiusmod.'),
        ('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do. eiusmod', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do.\neiusmod'),
        ('Loremipsumdolorsitamet,consecteturadipisicingelit,seddoeiusmodtemporincididunt', 'Loremipsumdolorsitamet,consecteturadipisicingelit,seddoeiusmodtemporinci\ndidunt'),
        ('Foo\n\nBar', 'Foo\n\nBar')
    ]


def assert_wrapped(testing, expected):
    assert wrap(testing, 72) == expected, "Expected '%s', returned '%s'." % (expected, wrap(testing, 72))

def test_wrap_basic():
    for i, o in WRAP_BASIC_PAIRS:
        yield assert_wrapped, i, o
