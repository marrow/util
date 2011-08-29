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
        'Return a new NamedTuple object replacing specified fields with new values'
        result = self._make(map(kwds.pop, self._fields, self))
        
        if kwds:
            raise ValueError('Got unexpected field names: %r' % kwds.keys())
        
        return result
    
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
    
    # The following are pseudo set operations.
    
    def __or__(self, other):
        """Combine tuples, with values from self overriding ones from other."""
        
        if type(self) != type(other):
            raise TypeError("Can not merge dissimilar types.")
        
        data = other.as_dict()
        
        for i in self._fields:
            if self[i] is None:
                continue
            
            data[i] = self[i]
        
        return self.__class__(**data)
    
    # The following operations only work on fully numeric NamedTuple instances.
    
    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Can not add dissimilar types.")
        
        v = []
        
        for n in self._fields:
            v.append(((self[n] or 0) + (other[n] or 0)) or None)
        
        return self.__class__(*v)
    
    def __neg__(self):
        data = self.as_dict()
        
        for i in data:
            if data[i] is None:
                continue
            
            data[i] = -data[i]
        
        return self.__class__(**data)
