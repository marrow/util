# encoding: utf-8

"""Useful datatype converters."""

import re
import collections
import inspect

from marrow.util.compat import binary, unicode


__all__ = ['boolean', 'array', 'integer', 'number', 'KeywordProcessor', 'tags', 'terms']



def boolean(input):
    """Convert the given input to a boolean value.
    
    Intelligently handles boolean and non-string values, returning
    as-is and passing to the bool builtin respectively.
    
    This process is case-insensitive.
    
    Acceptable values:
    
    True
        * yes
        * y
        * on
        * true
        * t
        * 1
    
    False
        * no
        * n
        * off
        * false
        * f
        * 0
    
    :param input: the value to convert to a boolean
    :type input: any
    
    :returns: converted boolean value
    :rtype: bool
    """
    
    try:
        input = input.strip().lower()
    except AttributeError:
        return bool(input)
    
    if input in ('yes', 'y', 'on', 'true', 't', '1'):
        return True
    
    if input in ('no', 'n', 'off', 'false', 'f', '0'):
        return False
    
    raise ValueError("Unable to convert {0!r} to a boolean value.".format(input))


def array(input, separator=',', strip=True, empty=False):
    """Convert the given input to a list.
    
    Intelligently handles list and non-string values, returning
    as-is and passing to the list builtin respectively.
    
    The default optional keyword arguments allow for lists in the form::
    
        "foo,bar, baz   , diz" -> ['foo', 'bar', 'baz', 'diz']
    
    For a far more advanced method of converting a string to a list of
    values see :class:`KeywordProcessor`.
    
    :param input: the value to convert to a list
    :type input: any
    
    :param separator: The character (or string) to use to split the
                      input.  May be None to split on any whitespace.
    :type separator: basestring or None
    
    :param strip: If True, the values found by splitting will be stripped
                  of extraneous whitespace.
    :type strip: bool
    
    :param empty: If True, allow empty list items.
    :type empty: bool
    
    :returns: converted values as a list
    :rtype: list
    """
    
    if input is None:
        return []
    
    if isinstance(input, list):
        if not empty:
            return [i for i in input if i]
        
        return input
    
    if not isinstance(input, (binary, unicode)):
        if not empty:
            return [i for i in list(input) if i]
        
        return list(input)
    
    if not strip:
        if not empty:
            return [i for i in input.split(separator) if i]
        
        return input.split(separator)
    
    if not empty:
        return [i for i in [i.strip() for i in input.split(separator)] if i]
    
    return [i.strip() for i in input.split(separator)]


def integer(input):
    """Convert the given input to an integer value.
    
    :param input: the value to convert to an integer
    :type input: any
    
    :returns: converted integer value
    :rtype: int
    """
    
    try:
        return int(input)
    except (TypeError, ValueError):
        raise ValueError("Unable to convert {0!r} to an integer value.".format(input))


def number(input):
    """Convert the given input to a floating point or integer value.
    
    In cases of ambiguity, integers will be prefered to floating point.
    
    :param input: the value to convert to a number
    :type input: any
    
    :returns: converted integer value
    :rtype: float or int
    """
    
    try:
        return int(input)
    except (TypeError, ValueError):
        pass
    
    try:
        return float(input)
    except (TypeError, ValueError):
        raise ValueError("Unable to convert {0!r} to a number.".format(input))


class KeywordProcessor(object):
    """Process user-supplied keywords, tags, or search terms.
    
    This tries to be as flexible as possible while remaining efficient.
    The vast majority of the work is done in the regular expression,
    and the primary goal of this class is to generate the complex regular
    expression.
    
    Two example converters covering the most common cases are created for
    you automatically as :data:`tags` and :data:`terms`.
    """
    
    def __init__(self, separators=' \t', quotes="\"'", groups=[], group=False, normalize=None, sort=False, result=list):
        """Configure the processor.
        
        :param separators: A list of acceptable separator characters.  The first will be used for joins.
        :type separator: list or string
        
        :param quotes: Pass a list or tuple of allowable quotes. E.g. ["\"", "'"] or None to disable.
        :param groups: Pass a string, list, or tuple of allowable prefixes.  E.g. '+-' or None to disable.
        :param group: Pass in the type you want to group by, e.g. list, tuple, or dict.
        :param normalize: Pass a function which will normalize the results.  E.g. lambda s: s.lower().strip(' \"')
        :param sort: Sort the resulting list (or lists) alphabeticlly.
        :param result: The return type.  One of set, tuple, list.
        
        If groups are defined, and group is not, the result will be a list/tuple/set of tuples, e.g. [('+', "foo"), ...]
        """
        
        self.separators = separators = list(separators)
        self.quotes = quotes = list(quotes) if quotes else []
        
        self.pattern = ''.join((
                ('[\s%s]*' % (''.join(separators), )), # Trap possible leading space or separators.
                '(',
                    ('[%s]%s' % (''.join([i for i in list(groups) if i is not None]), '?' if None in groups else '')) if groups else '', # Pass groups=('+','-') to handle optional leading + or -.
                    ''.join([(r'%s[^%s]+%s|' % (i, i, i)) for i in quotes]) if quotes else '', # Match any amount of text (that isn't a quote) inside quotes.
                    ('[^%s]+' % (''.join(separators), )), # Match any amount of text that isn't whitespace.
                ')',
                ('[%s]*' % (''.join(separators), )), # Match possible separator character.
            ))
        self.regex = re.compile(self.pattern)
        
        self.groups = list(groups)
        self.group = dict if group is True else group
        self.normalize = normalize
        self.sort = sort
        self.result = result
    
    def __call__(self, value):
        if isinstance(value, (binary, unicode)):
            return self.split(value)
        
        return self.join(value)
    
    def split(self, value):
        if not isinstance(value, (binary, unicode)): raise TypeError("Invalid type for argument 'value'.")
        
        matches = self.regex.findall(value)
        
        if hasattr(self.normalize, '__call__'): matches = [self.normalize(i) for i in matches]
        if self.sort: matches.sort()
        if not self.groups: return self.result(matches)
        
        groups = dict([(i, list()) for i in self.groups])
        if None not in groups: groups[None] = list() # To prevent errors.
        
        for i in matches:
            if i[0] in self.groups:
                groups[i[0]].append(i[1:])
            else:
                groups[None].append(i)
        
        if self.group is dict: return groups
        
        if self.group is False or self.group is None:
            results = []
            
            for group in self.groups:
                results.extend([(group, match) for match in groups[group]])
            
            return self.result(results)
        
        return self.group([[match for match in groups[group]] for group in self.groups])
    
    def join(self, values):
        def sanatize(keyword):
            if not self.quotes:
                return keyword
            
            for sep in self.separators:
                if sep in keyword:
                    return self.quotes[0] + keyword + self.quotes[0]
            
            return keyword
        
        if self.group is dict:
            if not isinstance(values, dict):
                raise ValueError("Dictionary grouped values must be passed as a dictionary.") # pragma: no cover
            
            return self.separators[0].join([(prefix + sanatize(keyword)) for prefix, keywords in values for keyword in values[prefix]])
        
        if not isinstance(values, (list, tuple, set)):
            raise ValueError("Ungrouped values must be passed as a list, tuple, or set.")
        
        return self.separators[0].join([sanatize(keyword) for keyword in values])


tags = KeywordProcessor(' \t,', normalize=lambda s: s.lower().strip('"'), sort=True, result=set)
tags.__doc__ = 'A lowercase-normalized ungrouped tagset processor, returning only unique tags.'

terms = KeywordProcessor(groups=[None, '+', '-'], group=tuple)
terms.__doc__ = 'A search keyword processor which retains quotes and groups into a dictionary of lists.'
