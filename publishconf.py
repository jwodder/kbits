# This file is only used if you use `make publish` or explicitly specify it as
# your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://jwodder.github.io/kbits'
RELATIVE_URLS = False
FEED_DOMAIN = SITEURL

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None

FEED_ALL_RSS = 'feeds/posts.rss'
AUTHOR_FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = True
