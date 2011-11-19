# encoding: utf-8


"""Compatability features.

Python 2.5 is the minimum version supported by Marrow, and great effort is
being made to support Python 3.x.
"""

import sys
import traceback


__all__ = ['formatdate', 'unquote', 'range', 'execfile', 'exception', 'binary',
           'unicode', 'bytestring', 'native', 'unicodestr', 'uvalues', 'IO',
           'parse_qsl']


if sys.version_info < (3, 0):  
    from email.utils import formatdate # DEPRECATE
    from urllib import unquote_plus as unquote
    from urlparse import parse_qsl
    basestring = basestring
    binary = bytes = str
    unicode = unicode
    range = xrange
    execfile = execfile

else:  # pragma: no cover
    from email.utils import formatdate # DEPRECATE
    from urllib.parse import unquote_plus as unquote_
    from cgi import parse_qsl
    basestring = str
    binary = bytes = bytes
    unicode = str
    range = range

    def execfile(filename, globals_=None, locals_=None):
        if globals_ is None:
            globals_ = globals()

        if locals_ is None:
            locals_ = globals_

        exec(open(filename).read(), globals_, locals_)

    def unquote(t):
        """Python 3 requires unquote to be passed unicode, but unicode
        characters may be encoded using quoted bytes!
        """
        return unquote_(t.decode('iso-8859-1')).encode('iso-8859-1')


def exception(maxTBlevel=None):
    """Retrieve useful information about an exception.

    Returns a bunch (attribute-access dict) with the following information:

    * name: exception class name
    * cls: the exception class
    * exception: the exception instance
    * trace: the traceback instance
    * formatted: formatted traceback
    * args: arguments to the exception instance

    This functionality allows you to trap an exception in a method agnostic to
    differences between Python 2.x and 3.x.
    """

    try:
        from marrow.util.bunch import Bunch

        cls, exc, trbk = sys.exc_info()
        excName = cls.__name__
        excArgs = getattr(exc, 'args', None)

        excTb = ''.join(traceback.format_exception(cls, exc, trbk, maxTBlevel))

        return Bunch(
                name=excName,
                cls=cls,
                exception=exc,
                trace=trbk,
                formatted=excTb,
                args=excArgs
            )

    finally:
        del cls, exc, trbk


def bytestring(v, encoding='utf-8', fallback='iso-8859-1', errors='strict'):
    """Convert a given value into a bytestring.
    
    If the value is a unicode string that contains non-ascii characters,
    will attempt to encode it using the given encoding, using the given
    errors strategy (which is the same as for the unicode encode method).
    If errors is 'strict' (the default), and encoding fails, try again
    with the fallback encoding.
    """
    try:
        return bytes(v)
    except UnicodeError:
        # unicode value has non-ascii characters:
        try:
            return v.encode(encoding, errors)
        except UnicodeError:
            return v.encode(fallback)


def native(s, encoding='utf-8', fallback='iso-8859-1'):
    """Convert a given string into a native string."""

    if isinstance(s, str):
        return s

    if str is unicode:  # Python 3.x ->
        return unicodestr(s, encoding, fallback)

    return bytestring(s, encoding, fallback)


def unicodestr(v, encoding='utf-8', fallback='iso-8859-1', errors='strict'):
    """Convert a value to unicode if it isn't already.
    
    Attempts to decode bytestrings (or values with a bytestring, but no
    unicode, representation) using the given encoding.

    The errors strategy is the same as for the bytestring decode method.
    If errors is 'strict' (the default), and decoding fails, try again
    with the fallback encoding.
    """
    try:
        return unicode(v)
    except UnicodeError:
        # bytestring value has non-ascii characters:
        v = bytes(v)

        try:
            return v.decode(encoding, errors)
        except UnicodeError:
            return v.decode(fallback)


def uvalues(a, encoding='utf-8', fallback='iso-8859-1'):
    """Return a list of decoded values from an iterator.

    If any of the values fail to decode, re-decode all values using the
    fallback.
    """

    try:
        return encoding, [s.decode(encoding) for s in a]

    except UnicodeError:
        return fallback, [s.decode(fallback) for s in a]


# In-memory binary stream representation for Python 2.5 or 2.6+.
if sys.version_info >= (2, 6):
    from io import BytesIO as IO

else:  # pragma: no cover
    try:
        from cStringIO import cStringIO as IO

    except ImportError:
        from StringIO import StringIO as IO
