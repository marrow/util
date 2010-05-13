# encoding: utf-8

from unittest import TestCase


from pulp.util import compat



class TestPy3K(TestCase):
    def test_bytes(self):
        data = compat.binary(b'\xc3\xbc')
        self.assertEquals(len(data), 2)
        
        self.failUnless(isinstance(data.decode('utf8'), compat.unicode))
        self.assertEquals(len(data.decode('utf8')), 1)
    
    def test_unicode(self):
        text = compat.unicode(u'ü')
        self.assertEquals(len(text), 1)
        
        self.failUnless(isinstance(text.encode('utf8'), compat.binary))
        self.assertEquals(len(text.encode('utf8')), 2)
    
    def test_byte_errors(self):
        self.assertRaises(UnicodeEncodeError, lambda: compat.binary(u'ü'))


class TestIO(TestCase):
    def test_string_bytes_io(self):
        io = compat.IO("Hello world!")
        value = io.read()
        
        self.assertEquals(value, "Hello world!")
        self.failUnless(isinstance(value, compat.binary))
        
        self.assertRaises(TypeError, lambda: compat.IO(u"ü"))
