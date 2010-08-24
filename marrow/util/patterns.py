# encoding: utf-8


__all__ = ['Borg']



class Borg(object):
    """The Borg are better than Singletons.
    
    Create instances that have the same underlying dictionary.
    
    Popeye says: "You will be askimilgrated."
    """
    
    _dict = {}
    
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls, *args, **kwds)
        obj.__dict__ = cls._dict
        
        return obj
