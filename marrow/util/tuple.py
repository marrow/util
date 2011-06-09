# encoding: utf-8

# This module is licensed under the LGPLv3.
# Copyright (c) 2011 Le Site Inc.
# The text of the LGPL can be found online:
#     http://www.gnu.org/copyleft/lesser.html

__all__ = ['NamedTuple']


class NamedTuple(tuple):
    """A tuple with attribute access.
    
    When creating instances, later values can be omitted and default to None.
    """
    
    __slots__ = () 
    _fields = None # OVERRIDE THIS IN A SUBCLASS
    
    def __new__(cls, *args, **kw):
        if (len(args) + len(kw)) > len(cls._fields):
            raise TypeError('Expected no more than %d arguments, got %d' % (len(cls._fields), len(args) + len(kw)))
        
        values = list(args) + ([None] * (len(cls._fields) - len(args)))
        
        try:
            for i in kw:
                values[cls._fields.index(i)] = kw[i]
        
        except ValueError:
            raise TypeError('Unknown attribute name %r' % (i, ))
        
        return tuple.__new__(cls, tuple(values))
    
    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        result = new(cls, iterable)
        
        if len(result) != len(cls._fields):
            raise TypeError('Expected %d arguments, got %d' % (len(cls._fields), len(result)))
        
        return result
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ", ".join([("%s=%r" % (i, j)) for i, j in zip(self._fields, self)]))
    
    def as_dict(self):
        return dict(zip(self._fields, self))
    
    @classmethod
    def from_dict(cls, d, new=tuple.__new__, len=len):
        values = [None] * len(cls._fields)
        
        try:
            for i in d:
                values[cls._fields.index(i)] = d[i]
        
        except ValueError:
            raise TypeError('Unknown attribute name %r' % (i, ))
        
        return cls(*values)
    
    def _replace(self, **kwds):
        'Return a new Requirement object replacing specified fields with new values'
        result = self._make(map(kwds.pop, self._fields, self))
        
        if kwds:
            raise ValueError('Got unexpected field names: %r' % kwds.keys())
        
        return result
    
    def __getnewargs__(self):
        return tuple(self)
    
    def __getattr__(self, name):
        if name not in self._fields:
            raise AttributeError('Unknown field name: %r' % name)
        
        return self[self._fields.index(name)]
    
    def __getitem__(self, name):
        if type(name) is int:
            return tuple.__getitem__(self, name)
        
        return tuple.__getitem__(self, self._fields.index(name))
    
    def keys(self):
        return self._fields
