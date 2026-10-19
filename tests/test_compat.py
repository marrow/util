# encoding: utf-8

import os

if not os.getcwd().endswith('tests'):
    os.chdir('tests')

import sys
from unittest import TestCase

from marrow.util import compat


if sys.version_info[:2] >= (3, 0):
    from uni_compat3 import uchar

else:
    from uni_compat2 import uchar



class TestPy3K(TestCase):
    def test_parse_qsl(self):
        self.assertEqual(
            compat.parse_qsl('a=1&b=two+words'),
            [('a', '1'), ('b', 'two words')],
        )

    def test_exception(self):
        try:
            1/0
        
        except:
            exc = compat.exception()
            
            self.assertEqual(exc.name, 'ZeroDivisionError')
            self.assertEqual(exc.cls, ZeroDivisionError)
            self.assertIn('division', exc.args[0])
            self.assertIn('by zero', exc.args[0])
        
        try:
            raise Exception('foo', 1)

        except:
            exc = compat.exception()

            self.assertEqual(exc.name, 'Exception')
            self.assertEqual(exc.cls, Exception)
            self.assertEqual(exc.args, ('foo', 1))
        
    
    def test_bytes(self):
        data = compat.binary(b'\xc3\xbc')
        self.assertEqual(len(data), 2)
        
        self.assertTrue(isinstance(data.decode('utf8'), compat.unicode))
        self.assertEqual(len(data.decode('utf8')), 1)
    
    def test_unicode(self):
        text = compat.unicode(uchar())
        self.assertEqual(len(text), 1)
        
        self.assertTrue(isinstance(text.encode('utf8'), compat.binary))
        self.assertEqual(len(text.encode('utf8')), 2)
    
    def test_byte_errors(self):
        if sys.version_info < (3, 0):
            self.assertRaises(UnicodeEncodeError, lambda: compat.binary(uchar()))
        
        else:
            self.assertRaises(TypeError, lambda: compat.binary(uchar()))


class TestIO(TestCase):
    def test_string_bytes_io(self):
        io = compat.IO(b"Hello world!")
        value = io.read()
        
        self.assertEqual(value, b"Hello world!")
        self.assertTrue(isinstance(value, compat.binary))
        
        self.assertRaises(TypeError, lambda: compat.IO(uchar()))
