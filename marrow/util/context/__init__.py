# encoding: utf-8

import os

from contextlib import contextmanager


__all__ = ['cd', 'path']



@contextmanager
def cd(path, on=os):
    """Change the current working directory within this context.
    
    Preserves the previous working directory and can be applied to remote
    connections that offer @getcwd@ and @chdir@ methods using the @on@
    argument.
    """
    
    original = on.getcwd()
    on.chdir(path)
    
    yield
    
    on.chdir(original)


@contextmanager
def path(append=None, prepend=None, replace=None, on=os):
    """Update the PATH environment variable.
    
    Can append, prepend, or replace the path.  Each of these expects a string
    or a list of strings (for multiple path elements) and can operate on remote
    connections that offer an @environ@ attribute using the @on@ argument.
    """
    
    original = on.environ['PATH']
    
    if replace and (append or prepend):
        raise ValueError("You can not combine append or prepend with replace.")
    
    if replace:
        if not isinstance(replace, list):
            replace = list(replace)
        
        on.environ['PATH'] = ':'.join(replace)
    
    else:
        if append:
            if not isinstance(append, list):
                append = list(append)
            
            append.insert(0, on.environ['PATH'])
            on.environ['PATH'] = ':'.join(append)
        
        if prepend:
            if not isinstance(prepend, list):
                prepend = list(prepend)
            
            prepend.append(on.environ['PATH'])
            on.environ['PATH'] = ':'.join(prepend)
    
    yield
    
    on.environ['PATH'] = original


@contextmanager
def environ(on=os, **kw):
    """Update one or more environment variables.
    
    Preserves the previous environment variable (if available) and can be
    applied to remote connections that offer an @environ@ attribute using the
    @on@ argument.
    """
    
    originals = list()
    
    for key in kw:
        originals.append((key, on.environ.get(key, None)))
        on.environ[key] = kw[key]
    
    yield
    
    for key, value in originals:
        if not value:
            del on.environ[key]
            continue
        
        on.environ[key] = value
