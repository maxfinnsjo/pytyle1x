#!/usr/bin/env python3

import sys
from distutils import sysconfig
from distutils.core import setup

try:
    from Xlib.display import Display
    from Xlib import X, XK, Xatom, Xutil, protocol
    from Xlib.ext import xinerama
except:
    print('\nPyTyle requires python-xlib')
    sys.exit(0)

#setup(
#      name = "pytyle",
#      author = "Andrew Gallant",
#      author_email = "andrew@pytyle.com",
#      version = "0.7.5",
#      license = "GPL",
#      description = "A manual tiling manager for EWMH compliant window managers",
#      long_description = "See README",
#      url = "http://pytyle.com",
#      platforms = 'POSIX',
#      packages = ['PyTyle', 'PyTyle.Tilers'],
#      data_files = [
#                    (sysconfig.get_python_lib() + '/PyTyle',
#                     ['./pytylerc', './INSTALL', './LICENSE', './README', './TODO', './CHANGELOG'])
#                    ],
#      scripts = ['pytyle','pytyle-client']
#      )
