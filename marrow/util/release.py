# encoding: utf-8

"""Release information about Marrow Interface."""

from collections import namedtuple


__all__ = ['version_info', 'version']


version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(1, 2, 0, 'final', 0)

version = ".".join([str(i) for i in version_info[:3]]) + ((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')



# encoding: utf-8

"""Release information about Marrow."""


name = "marrow.util"
version = "1.1.0"
release = "1.1"

summary = "Commonly shared Python utility subclasses and functions."
description = """"""
author = "Alice Bevan-McGregor"
email = "alice+marrow@gothcandy.com"
url = "http://github.com/pulp/marrow.util"
download_url = "http://cheeseshop.python.org/pypi/marrow.util/"
copyright = "2009-2011, Alice Bevan-McGregor"
license = "MIT"
