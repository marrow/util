# encoding: utf-8

from __future__ import unicode_literals

try:
    from urlparse import urlparse

except ImportError:
    from urllib.parse import urlparse

from marrow.util.compat import native, bytestring, unicodestr as unicodestring
from marrow.util.path import Path



class URL(object):
    path = Path()
    
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
        parts.append((":" + self.port) if self.port else "")
        parts.append(self.path or "/")
        parts.append((";" + self.params) if self.params else "")
        parts.append(("?" + self.query) if self.query else "")
        parts.append(("#" + self.fragment) if self.fragment else "")
        
        return "".join(parts)
    
    def __repr__(self):
        return native(self.render(True))
    
    def __str__(self):
        return bytestring(self.render())
    
    def __unicode__(self):
        return self.render()
