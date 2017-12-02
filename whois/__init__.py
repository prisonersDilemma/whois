#!/usr/bin/env python3.6

from . import database
from . import nacat
from . import targets

global PKGPATH # Not even sure how global works.
PKGPATH = __path__[0]
