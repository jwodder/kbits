import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# Publication settings
SITEURL = 'https://jwodder.github.io/kbits'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL

FEED_ALL_ATOM = 'feeds/posts.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/category.{slug}.atom.xml'
TAG_FEED_ATOM = 'feeds/tag.{slug}.atom.xml'
AUTHOR_FEED_ATOM = None

FEED_ALL_RSS = 'feeds/posts.rss'
CATEGORY_FEED_RSS = 'feeds/category.{slug}.rss'
TAG_FEED_RSS = 'feeds/tag.{slug}.rss'
AUTHOR_FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = True
