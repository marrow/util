# encoding: utf-8

import sys
from unittest import TestCase


from pulp.util import compat


if sys.version_info >= (3, 0):
    def uchar():
        def inner():
            return 'ü'
        return inner()

else:
    def uchar():
        def inner():
            return u'ü'
        return inner()



class TestPy3K(TestCase):
    def test_exception(self):
        try:
            1/0
        
        except:
            exc = compat.exception()
            
            self.assertEquals(exc.name, 'ZeroDivisionError')
            self.assertEquals(exc.cls, ZeroDivisionError)
            self.assertEquals(exc.args, ('integer division or modulo by zero', ))
        
        try:
            raise Exception('foo', 1)

        except:
            exc = compat.exception()

            self.assertEquals(exc.name, 'Exception')
            self.assertEquals(exc.cls, Exception)
            self.assertEquals(exc.args, ('foo', 1))
        
    
    def test_bytes(self):
        data = compat.binary(b'\xc3\xbc')
        self.assertEquals(len(data), 2)
        
        self.failUnless(isinstance(data.decode('utf8'), compat.unicode))
        self.assertEquals(len(data.decode('utf8')), 1)
    
    def test_unicode(self):
        text = compat.unicode(uchar())
        self.assertEquals(len(text), 1)
        
        self.failUnless(isinstance(text.encode('utf8'), compat.binary))
        self.assertEquals(len(text.encode('utf8')), 2)
    
    def test_byte_errors(self):
        self.assertRaises(UnicodeEncodeError, lambda: compat.binary(uchar()))


class TestIO(TestCase):
    def test_string_bytes_io(self):
        io = compat.IO("Hello world!")
        value = io.read()
        
        self.assertEquals(value, "Hello world!")
        self.failUnless(isinstance(value, compat.binary))
        
        self.assertRaises(TypeError, lambda: compat.IO(uchar()))
