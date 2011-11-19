# encoding: utf-8

from __future__ import unicode_literals
import sys
from unittest import TestCase


from marrow.util import compat


if sys.version_info >= (3, 0):
    from uni_compat3 import uchar

else:
    from uni_compat2 import uchar



class TestPy3K(TestCase):
    def test_exception(self):
        try:
            1/0
        
        except:
            exc = compat.exception()
            
            self.assertEquals(exc.name, 'ZeroDivisionError')
            self.assertEquals(exc.cls, ZeroDivisionError)
            self.assertTrue('division or modulo by zero' in exc.args[0])
        
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
        if sys.version_info < (3, 0):
            self.assertRaises(UnicodeEncodeError, lambda: compat.binary(uchar()))
        
        else:
            self.assertRaises(TypeError, lambda: compat.binary(uchar()))


class TestIO(TestCase):
    def test_string_bytes_io(self):
        io = compat.IO(b"Hello world!")
        value = io.read()
        
        self.assertEquals(value, b"Hello world!")
        self.failUnless(isinstance(value, compat.binary))
        
        self.assertRaises(TypeError, lambda: compat.IO(uchar()))


class TestStringConversion(TestCase):
    # unicodestr:

    def test_convert_unicode_to_unicode(self):
        input = 'unicode'
        u = compat.unicodestr(input)
        # assert good performance:
        assert u is input

    def test_convert_bytestring_to_unicode(self):
        u = compat.unicodestr(b'bytestring')
        self.assertEqual(u, 'bytestring')
        self.failUnless(isinstance(u, compat.unicode))

    def test_convert_utf8_bytestring_to_unicode(self):
        expected = 'utf-8 bytestring with non-ascii characters £∫é≈Ω'
        b = expected.encode('utf-8')
        u = compat.unicodestr(b)
        # test default encoding:
        self.assertEqual(compat.unicodestr(b, encoding='utf-8'), u)
        self.assertEqual(u, expected)
        self.failUnless(isinstance(u, compat.unicode))

    def test_convert_latin1_bytestring_to_unicode(self):
        expected = 'latin-1 bytestring with non-ascii characters é'
        b = expected.encode('iso-8859-1')
        # test default fallback encoding:
        self.assertEqual(compat.unicodestr(b, encoding='iso-8859-1'), expected)
        u = compat.unicodestr(b)
        self.assertEqual(u, expected)
        self.failUnless(isinstance(u, compat.unicode))

    def test_convert_object_with_unicode_method_to_unicode(self):
        class HasUnicodeRepresentation(object):
            def __unicode__(self):
                return 'expected unicode'
        u = compat.unicodestr(HasUnicodeRepresentation())
        self.assertEqual(u, 'expected unicode')
        self.failUnless(isinstance(u, compat.unicode))

    def test_convert_object_with_utf8_str_repr_to_unicode(self):
        class HasEncodedBytestringRepresentation(object):
            def __str__(self):
                return 'expected bytestring é'.encode('utf-8')
        u = compat.unicodestr(HasEncodedBytestringRepresentation())
        self.assertEqual(u, 'expected bytestring é')
        self.failUnless(isinstance(u, compat.unicode))

    # bytestring:

    def test_convert_bytestring_to_bytestring(self):
        input = b'bytestring'
        b = compat.bytestring(input)
        # assert good performance:
        assert b is input

    def test_convert_unicode_to_bytestring(self):
        b = compat.bytestring('unicode')
        self.assertEqual(b, b'unicode')
        self.failUnless(isinstance(b, compat.bytes))

    def test_convert_unicode_to_utf8_bytestring(self):
        u = 'unicode with non-ascii characters ∂åé≠∆'
        expected = u.encode('utf-8')
        b = compat.bytestring(u)
        self.assertEqual(b, expected)
        self.failUnless(isinstance(b, compat.bytes))

    def test_convert_unicode_to_latin1_bytestring(self):
        u = 'unicode with non-ascii character é'
        expected = u.encode('iso-8859-1')
        b = compat.bytestring(u, 'iso-8859-1')
        self.assertEqual(b, expected)
        self.failUnless(isinstance(b, compat.bytes))

    def test_convert_object_with_str_method_to_unicode(self):
        class HasStrRepresentation(object):
            def __str__(self):
                return b'a bytestring'
        b = compat.bytestring(HasStrRepresentation())
        self.assertEqual(b, b'a bytestring')
        self.failUnless(isinstance(b, compat.bytes))

    def test_convert_object_with_utf8_str_repr_to_bytestring(self):
        class HasEncodedStrRepresentation(object):
            def __str__(self):
                return b'a bytestring with é'
        b = compat.bytestring(HasEncodedStrRepresentation())
        self.assertEqual(b, b'a bytestring with é')
        self.failUnless(isinstance(b, compat.bytes))

    def test_bytestring_fallback(self):
        u = '\xa1'
        self.assertRaises(UnicodeError, compat.bytestring, u, 'iso-8859-2', fallback='iso-8859-2')
