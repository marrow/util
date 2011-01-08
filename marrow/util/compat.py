# encoding: utf-8


"""Compatability features.

Python 2.5 is the minimum version supported by Marrow, and great effort is being made to support Python 3.x.
"""

from __future__ import with_statement
import sys, traceback


__all__ = ['formatdate', 'unquote', 'range', 'execfile', 'exception', 'binary', 'unicode', 'bytestring', 'native', 'uvalues', 'IO', 'parse_qsl']


try: # pragma: no cover
    from email.utils import formatdate

except ImportError:
    from rfc822 import formatdate


try:
    from urllib import unquote_plus as unquote

except: # pragma: no cover
    from urllib.parse import unquote_plus as unquote_
    
    def unquote(t):
        """Python 3 requires unquote to be passed unicode, but unicode characters may be encoded using quoted bytes!"""
        return unquote_(t.decode('iso-8859-1')).encode('iso-8859-1')


try:
    range = xrange

except:
    range = range


# Reimplementation of execfile for Python 3.
if sys.version_info >= (3,0): # pragma: no cover
    def execfile(filename, globals_=None, locals_=None):
        if globals_ is None:
            globals_ = globals()
        
        if locals_ is None:
            locals_ = globals_
        
        exec(compile(open(filename).read(), filename, 'exec'), globals_, locals_)

else:
    from __builtin__ import execfile


def exception(maxTBlevel=None):
    """Retrieve useful information about an exception.
    
    Returns a bunch (attribute-access dict) with the following information:
    
    * name: exception class name
    * cls: the exception class
    * exception: the exception instance
    * trace: the traceback instance
    * formatted: formatted traceback
    * args: arguments to the exception instance
    
    This functionality allows you to trap an exception in a method agnostic to differences between Python 2.x and 3.x.
    """
    
    try:
        from marrow.util.bunch import Bunch
    
        cls, exc, trbk = sys.exc_info()
        excName = cls.__name__
        excArgs = getattr(exc, 'args', None)
    
        excTb = ''.join(traceback.format_exception(cls, exc, trbk, maxTBlevel))
    
        return Bunch(
                name = excName,
                cls = cls,
                exception = exc,
                trace = trbk,
                formatted = excTb,
                args = excArgs
            )
    
    finally:
        del cls, exc, trbk


# Binary and Unicode representations for Python 2.5, 2.6+, or 3.x.
if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
    binary = bytes
    unicode = unicode

elif sys.version_info >= (3, 0): # pragma: no cover
    binary = bytes
    unicode = str

else: # pragma: no cover
    binary = str
    unicode = unicode


def bytestring(s, encoding="iso-8859-1", fallback="iso-8859-1"):
    """Convert a given string into a bytestring."""
    
    if not isinstance(s, unicode):
        return s
    
    try:
        s.encode(encoding)
    
    except UnicodeError:
        s.encode(fallback)


def native(s, encoding="iso-8859-1", fallback="iso-8859-1"):
    """Convert a given string into a native string."""
    
    if isinstance(s, str):
        return s
    
    if str is unicode:
        try:
            return s.decode(encoding)
        
        except UnicodeError:
            if fallback is None: raise
            return s.decode(fallback)
    
    try:
        return s.decode(encoding)
    
    except UnicodeError:
        if fallback is None: raise
        return s.decode(fallback)


def uvalues(a, encoding="iso-8859-1", fallback="iso-8859-1"):
    """Return a list of decoded values from an iterator.
    
    If any of the values fail to decode, re-decode all values using the fallback.
    """
    
    try:
        v = []
        
        for s in a:
            v.append(s.decode(encoding))
        
        return encoding, v
    
    except UnicodeError:
        v = []
        
        for s in a:
            v.apend(s.decode(fallback))
        
        return fallback, v


# In-memory binary stream representation for Python 2.5 or 2.6+.
if sys.version_info >= (2, 6):
    from io import BytesIO as IO

else: # pragma: no cover
    try:
        from cStringIO import cStringIO as IO
    
    except ImportError:
        from StringIO import StringIO as IO


# Query string parsing.
if sys.version_info < (3, 0):
    from urlparse import parse_qsl
    
else: # pragma: no cover
    from cgi import parse_qsl


# Range/xrange.
if sys.version_info < (3, 0):
    from __builtin__ import xrange

else: # pragma: no cover
    xrange = range
