#!/usr/bin/env python
# encoding: utf-8

import sys, os

try:
    from distribute_setup import use_setuptools
    use_setuptools()

except ImportError:
    pass

from setuptools import setup, find_packages


if sys.version_info <= (2, 5):
    raise SystemExit("Python 2.5 or later is required.")

execfile(os.path.join("pulp", "util", "release.py"))



setup(
        name = name,
        version = version,
        
        description = summary,
        long_description = description,
        author = author,
        author_email = email,
        url = url,
        download_url = download_url,
        license = license,
        keywords = '',
        
        install_requires = [],
        
        test_suite = 'nose.collector',
        tests_require = ['nose', 'coverage', 'nose-achievements'],
        
        classifiers = [
                "Development Status :: 1 - Planning",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
        
        packages = find_packages(exclude=['tests', 'tests.*', 'docs']),
        include_package_data = True,
        package_data = {
                '': ['Makefile', 'README.textile', 'LICENSE', 'distribute_setup.py'],
                'docs': ['source/*']
            },
        zip_safe = True,
        
        namespace_packages = ['pulp', 'pulp.util'],
    )
