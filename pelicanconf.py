from datetime import date

# Site metadata
AUTHOR = 'John T. Wodder II'
SITENAME = 'Knowledge Bits'
#SITESUBTITLE = 'All about the things I know'
#SITESUBTITLE = 'Things I know about stuff'
DEFAULT_LANG = 'en'
TIMEZONE = 'America/New_York'
LOCALE = 'en_US.UTF-8'


# Site input layout
PATH = 'src'
ARTICLE_PATHS = ['posts']
STATIC_PATHS = ['static']
IGNORE_FILES = ['.*.swp']
USE_FOLDER_AS_CATEGORY = False


# Site output layout
OUTPUT_PATH = 'docs'
PAGE_URL = PAGE_SAVE_AS = '{slug}.html'
AUTHOR_SAVE_AS = AUTHORS_SAVE_AS = ''  # Disable author pages
ARCHIVES_SAVE_AS = ''  # Disable archive pages (in favor of index)


# Building & formatting settings
CACHE_CONTENT = False
STATIC_CHECK_IF_MODIFIED = True

DOCUTILS_SETTINGS = {
    "smart_quotes": True,
    "strip_comments": True,
    "math_output": "mathjax irrelevant.value",
}

DEFAULT_PAGINATION = False
SLUGIFY_SOURCE = 'basename'
PAGE_ORDER_BY = 'title'
DEFAULT_CATEGORY = 'Miscellanea'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# <https://github.com/getpelican/pelican/pull/2785>
FORMATTED_FIELDS = ['summary', 'Summary']


# Plugins
PLUGINS = []


# Themes
THEME = './theme'


# Theme variables
GITHUB_URL = 'https://github.com/jwodder/kbits'
PATH_IN_REPO = PATH  # PATH relative to root of repository
SHOW_AUTHOR = True
LINK_AUTHOR = False

site_creation_year = 2020
this_year = date.today().year
if this_year == site_creation_year:
    copyright_years = site_creation_year
else:
    copyright_years = f'{site_creation_year}–{this_year}'

FOOTER_HTML = f'''
Copyright © {copyright_years} {AUTHOR}.  This site's content is licensed under
a <a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons
Attribution 4.0 International License</a>.
'''

# TODO: Should these be shown on the top in the menu or on the side with LINKS?
SITE_MENU_ITEMS = [
    ('Categories', 'categories.html'),
    ('Tags', 'tags.html'),
]

LINKS_WIDGET_NAME = 'Links'
LINKS = [
    ('Site Repository', 'https://github.com/jwodder/kbits'),
]


# Variables to leave unset during development:
SITEURL = ''
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Other
BIND = '127.0.0.1'
