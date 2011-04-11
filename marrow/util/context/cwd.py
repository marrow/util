# encoding: utf-8

import os

from contextlib import contextmanager
from functools import wraps


__all__ = ['PreserveWorkingDirectory', 'pcwd']



class PreserveWorkingDirectory(object):
    """A context manager to preserve the current working directory.
    
    Additionally, if @nwd@ is provided, preserve the current working
    directory and change to @nwd@.
    """
    
    def __init__(self, nwd=None):
        self.cwd = None
        self.nwd = nwd
    
    def __enter__(self):
        self.cwd = os.getcwd()
        if self.nwd: os.chdir(self.nwd)
    
    def __exit__(self, type, value, traceback):
        os.chdir(self.cwd)


def pcwd(func):
    """A decorator to provide the functionality of the
    PreserveWorkingDirectory context manager for functions and methods."""
    
    @wraps(func)
    def inner(*args, **kw):
        with PreserveWorkingDirectory():
            return func(*args, **kw)
    
    return inner
