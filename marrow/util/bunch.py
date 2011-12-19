# encoding: utf-8

"""A dictionary with attribute-style access."""


from marrow.util.object import NoDefault


__all__ = ['Bunch', 'MultiBunch']



class Bunch(dict):
    """A dictionary with attribute-style access. It maps attribute access to the real dictionary."""
    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, super(Bunch, self).__repr__())
    
    def __getattr__(self, name):
        try:
            value = self[name]
            return Bunch(value) if isinstance(value, dict) else value
        
        except KeyError:
            try:
                return self.partial(name, self)
            
            except ValueError:
                raise AttributeError(name)
    
    __setattr__ = dict.__setitem__
    
    def __delattr__(self, name):
        try:
            del self[name]
        
        except KeyError:
            raise AttributeError(name)
    
    @classmethod
    def partial(cls, prefix, source):
        """Strip a prefix from the keys of another dictionary, returning a Bunch containing only valid key, value pairs."""
        match = prefix + "."
        
        matches = cls([(key[len(match):], source[key]) for key in source if key.startswith(match)])
        
        if not matches:
            raise ValueError()
        
        return matches


class MultiBunch(Bunch):
    """A dictionary that will hold multiple values for a given key.
    
    Unlike other solutions, this doesn't store every value in a list; if a value is assigned multiple times it will be wrapped in a list on the second assignment.
    
    To prevent user abuse if used for CGI processing, the get() method will only return the first value.  (Attribute and dictionary access will work as expected.)
    """
    
    def __setitem__(self, name, value):
        if name in self:
            if isinstance(self[name], list):
                self[name].append(value)
                return
            
            super(MultiBunch, self).__setitem__(name, [self[name], value])
            return
        
        super(MultiBunch, self).__setitem__(name, value)
    
    __setattr__ = __setitem__
    
    def get(self, name, default=NoDefault):
        value = super(MultiBunch, self).get(name) if default is NoDefault else super(MultiBunch, self).get(name, default)
        
        if isinstance(value, list):
            return value[0]
        
        return value
