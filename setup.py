#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup, find_packages


if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "util", "release.py")).read())



setup(
        name = "marrow.util",
        version = version,
        
        description = "A collection of many commonly reimplemented utility classes and functions.",
        long_description = """\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.util""",
        
        author = "Alice Bevan-McGregor",
        author_email = "alice+marrow@gothcandy.com",
        url = "https://github.com/marrow/marrow.util",
        license = "MIT",
        
        test_suite = 'nose.collector',
        tests_require = ['nose', 'coverage'],
        
        classifiers = [
                "Development Status :: 5 - Production/Stable",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.1",
                "Programming Language :: Python :: 3.2",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Utilities"
            ],
        
        packages = find_packages(exclude=['examples', 'tests']),
        zip_safe = True,
        include_package_data = True,
        package_data = {'': ['README.textile', 'LICENSE']},
        
        namespace_packages = ['marrow', 'marrow.util']
    )
