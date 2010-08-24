# encoding: utf-8

import collections

from marrow.util.compat import binary, unicode


__all__ = ['Path']



class Path(collections.deque):
    def __init__(self, value=None, separator='/'):
        self.separator = unicode(separator)

        super(Path, self).__init__()

        if value is not None:
            self._assign(value)

    def _assign(self, value):
        self.clear()
        
        if isinstance(value, (binary, unicode)):
            self.extend(unicode(value).split(self.separator))
            return

        self.extend(value)
    
    def __set__(self, obj, value):
        self._assign(value)

    def __str__(self):
        return self.separator.join(self)

    def __unicode__(self):
        return unicode(self.separator).join(self)
    
    def __add__(self, other):
        return self.__class__(unicode(self) + unicode(other))
    
    def __repr__(self):
        return "<Path %r>" % super(Path, self).__repr__()

    def __cmp__(self, other):
        """Perform type coersion and attempt to compare.
        
        This works for most builtin types that accept an iterable as
        the first argument, e.g. list, tuple, and set, and will work
        for str and unicode, too.
        """
        
        return cmp(type(other)(self), other)
    
    def __eq__(self, other):
        if isinstance(other, (binary, unicode)):
            return unicode(self) == unicode(other)
        
        return list(self) == list(other)

    def __getitem__(self, i):
        try:
            return super(Path, self).__getitem__(i)

        except TypeError:
            return Path([self[j] for j in range(*i.indices(len(self)))])
    
    def __abs__(self):
        return Path([''] + list(self)) if self[0] != '' else self
