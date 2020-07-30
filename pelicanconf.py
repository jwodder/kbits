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

OUTPUT_PATH = 'docs'

PAGE_URL = PAGE_SAVE_AS = '{slug}.html'

# Disable author pages:
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

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

SOCIAL_WIDGET_NAME = 'Social'
SOCIAL = [
    #('GitHub', 'https://github.com/jwodder'),
]

DEFAULT_PAGINATION = False

CACHE_CONTENT = False

DEFAULT_CATEGORY = 'Miscellanea'

DOCUTILS_SETTINGS = {
    "smart_quotes": True,
    "strip_comments": True,
    "math_output": "MathML",
}

IGNORE_FILES = ['.*.swp']
STATIC_CHECK_IF_MODIFIED = True
SLUGIFY_SOURCE = 'basename'

BIND = '127.0.0.1'

DEFAULT_DATE_FORMAT = '%Y-%m-%d'

PAGE_ORDER_BY = 'title'

USE_FOLDER_AS_CATEGORY = False

# Unset during development:
SITEURL = ''
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
