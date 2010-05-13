# encoding: utf-8

from unittest import TestCase

from pulp.util.insensitive import CaseInsensitiveDict



class TestCaseInsensitiveDict(TestCase):
    def test_basic(self):
        d = CaseInsensitiveDict()
        d['Content-Type'] = 'text/plain'
        
        self.assertEqual(d['content-type'], 'text/plain')
        self.assertEqual(d.items(), [('Content-Type', 'text/plain')])
        
        d['content-type'] = 'text/html'
        self.assertEqual(d['content-type'], 'text/html')
    
    def test_default(self):
        d = CaseInsensitiveDict({'foo': 'bar'})
    
    def test_keys(self):
        d = CaseInsensitiveDict({None: 2})
        self.assertEqual(d, {None: 2})
        self.assertEqual(d.get(None), 2)
