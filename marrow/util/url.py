# encoding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

try:
    from urlparse import urlparse
    from urllib import quote_plus, unquote_plus

except ImportError:
    from urllib.parse import urlparse, quote_plus, unquote_plus

from marrow.util.compat import basestring, native, unicode, bytestring, unicodestr as unicodestring
from marrow.util.path import Path
from marrow.util.object import NoDefault



class QueryString(object):
    def __init__(self, q=None, assignment="=", separator="&", encoded=True):
        self._l = list()
        self._d = dict()
        self.assignment = assignment
        self.separator = separator
        
        if q is not None:
            self.update(q, __encoded=encoded)
    
    def update(self, __value=None, *args, **kw):
        if __value is None:
            return
        
        __encoded = kw.pop('__encoded', False)
        
        if isinstance(__value, tuple):
            args = [__value] + list(args)
        
        elif isinstance(__value, dict):
            __value.update(kw)
            kw = __value
        
        elif isinstance(__value, list):
            args = __value + list(args)
        
        elif isinstance(__value, basestring):
            __value = __value.replace(self.separator, ".^:SEP:^.").replace(self.assignment, ".^:ASN:^.")
            args = [tuple(i.split(".^:ASN:^.")) for i in __value.split(".^:SEP:^.")] + list(args)
        
        elif isinstance(__value, QueryString):
            args = [i for i in __value.items()] + list(args)
        
        for i in args:
            if not isinstance(i, tuple) or len(i) != 2:
                raise ValueError()
            
            name, value = i
            if value is None:
                if name in self._d:
                    self._l.remove(name)
                    del self._d[i]
                
                continue
            
            if __encoded:
                name = unquote_plus(name)
                value = unquote_plus(value)
            
            if name not in self._l:
                self._l.append(name)
            
            self._d[name] = value
        
        for i in kw:
            if __value[i] is None:
                if i in self._d:
                    self._l.remove(i)
                    del self._d[i]
                
                continue
            
            if i not in self._l:
                self._l.append(i)
            
            self._d[i] = __value[i]
    
    def get(self, name, default=NoDefault):
        if name not in self._d:
            if default is not NoDefault:
                return default
            
            raise KeyError()
        
        return self._d.get(name, default)
    
    def clear(self):
        self._l = list()
        self._d = dict()
    
    def items(self):
        for i in self._l:
            yield (i, self._d[i])
    
    def keys(self):
        for i in self._l:
            yield i
    
    def values(self):
        for i in self._l:
            yield self._d[i]
    
    def append(self, value):
        self.update([value])
    
    def insert(self, value):
        # TODO
        raise NotImplementedError()
    
    def extend(self, values):
        self.update(values)
    
    def index(x, start=None, stop=None):
        return self._l.index(x, start, stop)
    
    def remove(self, x):
        self.update([(x, None)])
    
    def render(self):
        parts = []
        
        for i in self._l:
            v = self._d[i]
            i = quote_plus(i)
            
            if not isinstance(v, list):
                v = [v]
            
            for e in v:
                parts.append(i + self.assignment + quote_plus(e))
        
        return self.separator.join(parts)
    
    def __str__(self):
        return native(self.render())
    
    def __unicode__(self):
        return self.render()
    
    def __repr__(self):
        return "{" + ", ".join([("%r: %r" % (i, self._d[i])) for i in self._l]) + "}"
    
    def __len__(self):
        return len(self._l)
    
    def __getitem__(self, k):
        if isinstance(k, int):
            return self._d[self._l[k]]
        
        return self._d[k]
    
    def __setitem__(self, k, value):
        if isinstance(k, int):
            if not isinstance(value, tuple) or len(value) != 2:
                raise ValueError()
            
            name, value = value
            self._l[k] = name
            self._d[name] = value
            return
        
        self.update((k, value))
    
    def __delitem__(self, k):
        if isinstance(k, int):
            del self._d[self._l[k]]
            del self._l[k]
            return
        
        self.update((k, None))
    
    def __contains__(self, k):
        return k in self._d
    
    def __set__(self, obj, value):
        self.clear()
        self.update(value)


class URL(object):
    path = Path()
    query = QueryString()
    params = QueryString(assignment="=", separator=";")
    
    def __init__(self, url=None, scheme=None, user=None, password=None, host=None, port=None, path=None, params=None, query=None, fragment=None):
        """Construct a URL object.
        
        If arguments other than url are provided, they are used as defaults.  The parse result of the real URL overrides these.
        """
        
        self.scheme = scheme
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.path = path
        self.params = params
        self.query = query
        self.fragment = fragment
        
        if url is None:
            return
        
        if ( url[0] == '/' or url[1] == ':' ):
            url = "file://" + url
        
        result = urlparse(url)
        
        self.scheme = result.scheme or self.scheme
        
        result = urlparse(url.replace(self.scheme + '://', 'http://'))
        
        self.user = result.username or self.user
        self.password = result.password or self.password
        self.host = result.hostname or self.host
        self.port = result.port or self.port
        self.path = result.path or self.path
        self.params = result.params or self.params
        self.query = result.query or self.query
        self.fragment = result.fragment or self.fragment
    
    def render(self, safe=False):
        parts = []
        
        parts.append((self.scheme + "://") if self.scheme else "")
        parts.append(self.user or "")
        parts.append((":" + self.password) if self.user else ("@" if self.user else ""))
        parts.append(self.host or "")
        parts.append((":" + str(self.port)) if self.port else "")
        parts.append(unicode(self.path) or "/")
        parts.append((";" + unicode(self.params)) if self.params else "")
        parts.append(("?" + unicode(self.query)) if self.query else "")
        parts.append(("#" + quote_plus(self.fragment)) if self.fragment else "")
        
        return "".join(parts)
    
    def __repr__(self):
        return native(self.render(True))
    
    def __str__(self):
        return bytestring(self.render())
    
    def __unicode__(self):
        return self.render()
