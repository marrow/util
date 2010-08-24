# encoding: utf-8

"""A dictionary with case-insensitive access."""


from marrow.util.object import NoDefault


__all__ = ['CaseInsensitiveDict']


class CaseInsensitiveDict(dict):
    def __init__(self, default=None, *args, **kw):
        self._o = {}
        
        if default is None:
            default = dict()
            default.update(kw)
        
        for i in default:
            self[i] = default[i]
        
        super(CaseInsensitiveDict, self).__init__()
    
    def items(self):
        return [(self._o[k], self[k]) for k in self]
    
    def __setitem__(self, k, v):
        try:
            nk = k.lower()
        except:
            nk = k
        
        self._o[nk] = k
        super(CaseInsensitiveDict, self).__setitem__(nk, v)
    
    def __getitem__(self, k):
        try:
            nk = k.lower()
        except:
            nk = k
        
        return super(CaseInsensitiveDict, self).__getitem__(nk)
