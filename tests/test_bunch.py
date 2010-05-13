# encoding: utf-8

from unittest import TestCase

from pulp.util.bunch import Bunch, MultiBunch



class TestAttributeDictionary(TestCase):
    def test_empty_creation(self):
        d = Bunch()
        assert not d
    
    def test_populated_creation(self):
        d = Bunch(name='value')
        self.assertEqual(d['name'], 'value')
        
        d = Bunch({'name': 'value'})
        self.assertEqual(d['name'], 'value')
    
    def test_attribute_assignment(self):
        d = Bunch()
        d.name = 'value'
        assert hasattr(d, 'name')
        self.assertEqual(d['name'], 'value')
    
    def test_attribute_read(self):
        d = Bunch()
        d.name = 'value'
        assert d.name == 'value'
    
    def test_repr(self):
        d = Bunch()
        assert repr(d) == 'Bunch({})'
        
        d.name = 'value'
        self.assertEqual(repr(d), "Bunch({'name': 'value'})")
    
    def test_delete(self):
        d = Bunch(name='value')
        del d.name
        
        self.assertEqual(repr(d), 'Bunch({})')
        
        def error_test():
            del d.foo
        
        self.assertRaises(AttributeError, error_test)
    
    def test_partial(self):
        d1 = Bunch({'foo.bar': 1, 'foo.baz': 2, 'diz': 3})
        d2 = Bunch.partial('foo', d1)
        
        self.assertEqual(d2.get('diz', None), None)
        self.assertEqual(d2.baz, 2)
        
        d2.bar = 4
        
        self.assertEqual(d1['foo.bar'], 1)
        self.assertEqual(d1.foo.bar, 1)
        


class TestMultipleAttributeDictionary(TestCase):
    def test_empty_creation(self):
        d = MultiBunch()
        assert not d
    
    def test_populated_creation(self):
        d = MultiBunch(name='value')
        self.assertEqual(d['name'], 'value')
        
        d = MultiBunch({'name': 'value'})
        self.assertEqual(d['name'], 'value')
    
    def test_attribute_assignment(self):
        d = MultiBunch()
        
        d.name = 'value'
        assert hasattr(d, 'name')
        self.assertEqual(d['name'], 'value')
        
        d.name = 'value2'
        self.assertEqual(d['name'], ['value', 'value2'])
        
        d.name = 'value3'
        self.assertEqual(d['name'], ['value', 'value2', 'value3'])
    
    def test_attribute_read(self):
        d = MultiBunch()
        d.name = 'value'
        self.assertEqual(d.name, 'value')
        self.assertEqual(d.get('name'), 'value')
        
        d.name = 'value2'
        self.assertEqual(d.name, ['value', 'value2'])
        self.assertEqual(d.get('name'), 'value')
    
    def test_repr(self):
        d = MultiBunch()
        assert repr(d) == 'MultiBunch({})'
        
        d.name = 'value'
        self.assertEqual(repr(d), "MultiBunch({'name': 'value'})")
    
    def test_delete(self):
        d = MultiBunch(name='value')
        del d.name
        
        self.assertEqual(repr(d), 'MultiBunch({})')
        
        def error_test():
            del d.foo
        
        self.assertRaises(AttributeError, error_test)
