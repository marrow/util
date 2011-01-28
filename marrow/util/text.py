# encoding: utf-8

"""Text processing helper functions."""

import re


__all__ = ['normalize', 'ellipsis', 'wrap']


NORMALIZE_EXPRESSION = re.compile('\W+')



def normalize(name, collection=[]):
    base = NORMALIZE_EXPRESSION.sub('-', name.lower())
    suffix = 0
    
    while True:
        if ("%s%s" % (base.strip('-'), ("-%d" % (suffix, )) if suffix else "")) not in collection: break
        suffix += 1
    
    return ("%s%s" % (base.strip('-'), ("-%d" % (suffix, )) if suffix else ""))


def ellipsis(text, length, symbol="..."):
    """Present a block of text of given length.
    
    If the length of available text exceeds the requested length, truncate and
    intelligently append an ellipsis.
    """
    if len(text) > length:
        pos = text.rfind(" ", 0, length)
        if pos < 0:
            return text[:length].rstrip(".") + symbol
        else:
            return text[:pos].rstrip(".") + symbol
    
    else:
        return text


def wrap(text, columns=78):
    from textwrap import wrap
    
    lines = []
    for iline in text.splitlines():
        if not iline:
            lines.append(iline)
        else:
            for oline in wrap(iline, columns):
                lines.append(oline)
    
    return "\n".join(lines)
