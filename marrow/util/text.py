# encoding: utf-8

"""Text processing helper functions."""

import re


__all__ = ['normalize']


NORMALIZE_EXPRESSION = re.compile('\W+')



def normalize(name, collection=[]):
    base = NORMALIZE_EXPRESSION.sub('-', name.lower())
    suffix = 0
    
    while True:
        if ("%s%s" % (base.strip('-'), ("-%d" % (suffix, )) if suffix else "")) not in collection: break
        suffix += 1
    
    return ("%s%s" % (base.strip('-'), ("-%d" % (suffix, )) if suffix else ""))
