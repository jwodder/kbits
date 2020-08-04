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

DEFAULT_PAGINATION = 20
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
AUTHOR_LINK = 'https://github.com/jwodder'
SHOW_AUTHOR_IN_LISTINGS = False

site_creation_year = 2020
this_year = date.today().year
if this_year == site_creation_year:
    copyright_years = site_creation_year
else:
    copyright_years = f'{site_creation_year}–{this_year}'

FOOTER_HTML = f'''
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
    <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" />
</a>

Copyright © {copyright_years} <a xmlns:cc="http://creativecommons.org/ns#"
href="{AUTHOR_LINK}" property="cc:attributionName"
rel="cc:attributionURL">{AUTHOR}</a>.  This site's content is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative
Commons Attribution 4.0 International License</a>.
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

# Based on <https://git.io/JJoUU>
def iter_pages(current_page, total_pages, left_edge=2, left_current=2,
               right_current=5, right_edge=2):
    """
    Iterates over the page numbers in the pagination.  The four parameters
    control the thresholds how many numbers should be produced from the sides.
    Skipped page numbers are represented as `None`.
    """
    last = 0
    for num in range(1, total_pages + 1):
        if (
            num <= left_edge
            or current_page - left_current - 1 < num < current_page + right_current
            or num > total_pages - right_edge
        ):
            if last + 1 != num:
                yield None
            yield num
            last = num

JINJA_FILTERS = {"iter_pages": iter_pages}
