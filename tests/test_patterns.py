# encoding: utf-8

from unittest import TestCase

from marrow.util.patterns import Borg



class TestBorg(TestCase):
    def test_borg(self):
        a = Borg()
        b = Borg()
        
        assert a._dict is b._dict, "I am Hue."
        assert a is not b, "too alike"
        
        a.foo = 1
        
        self.assertEqual(a.foo, b.foo)
