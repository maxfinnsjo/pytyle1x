#!/usr/bin/env python3

import setuptools, sys

try:
    from Xlib.display import Display
    from Xlib import X, XK, Xatom, Xutil, protocol
    from Xlib.ext import xinerama
except:
    print('\nPyTyle requires python-xlib')
    sys.exit(0)

setuptools.setup(
    name = 'pytyle1x',
    version = '0.7.5',
    author = 'programical',
    description = 'A tiling manager for EWMH compliant window managers',
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/programical/pytyle1x',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3'
    ],
    scripts = ['pytyle1x'],
    python_requires = '>=3.6',
)
