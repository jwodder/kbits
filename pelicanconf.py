AUTHOR = 'John T. Wodder II'
SITENAME = 'Knowledge Bits'
#SITESUBTITLE = 'All about the things I know'
#SITESUBTITLE = 'Things I know about stuff'

DEFAULT_LANG = 'en'
TIMEZONE = 'America/New_York'
LOCALE = 'en_US.UTF-8'

PATH = 'src'
ARTICLE_PATHS = ['posts']
STATIC_PATHS = ['static']
IGNORE_FILES = ['.*.swp']

OUTPUT_PATH = 'docs'

PAGE_URL = PAGE_SAVE_AS = '{slug}.html'

# Disable author pages:
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

THEME = 'theme'
SHOW_AUTHOR = True
LINK_AUTHOR = False
PATH_IN_REPO = 'src'  # PATH relative to root of repository

# TODO: Set these through the templates so the URLs can be properly built from
# config settings:
MENUITEMS = [
    ('Main', 'https://jwodder.github.io/kbits/index.html'),
    ('Archives', 'https://jwodder.github.io/kbits/archives.html'),
    # TODO: Move the below to `LINKS`?  Move the above to `LINKS`?
    ('Categories', 'https://jwodder.github.io/kbits/categories.html'),
    ('Tags', 'https://jwodder.github.io/kbits/tags.html'),
]

LINKS_WIDGET_NAME = 'Links'
LINKS = [
    ('Site Repository', 'https://github.com/jwodder/kbits'),
]

GITHUB_URL = 'https://github.com/jwodder/kbits'

DEFAULT_PAGINATION = False

CACHE_CONTENT = False

DEFAULT_CATEGORY = 'Miscellanea'

DOCUTILS_SETTINGS = {
    "smart_quotes": True,
    "strip_comments": True,
}

STATIC_CHECK_IF_MODIFIED = True
SLUGIFY_SOURCE = 'basename'

BIND = '127.0.0.1'

PAGE_ORDER_BY = 'title'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

USE_FOLDER_AS_CATEGORY = False

# Unset during development:
SITEURL = ''
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# <https://github.com/getpelican/pelican/pull/2785>
FORMATTED_FIELDS = ['summary', 'Summary']
