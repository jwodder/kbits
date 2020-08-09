from datetime import date

# Site metadata
AUTHOR = 'John T. Wodder II'
SITENAME = 'Knowledge Bits'
#SITESUBTITLE = 'All about the things I know'
#SITESUBTITLE = 'Things I know about stuff'
#SITESUBTITLE = 'Bits of knowledge I possess'
#SITESUBTITLE = 'On the things I know'
#SITESUBTITLE = 'Hopefully useful write-ups'
#SITESUBTITLE = 'A knowledge blog'
#SITESUBTITLE = 'A reference blog'
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
OUTPUT_PATH = 'build'

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
ARTICLE_LANG_URL = '{lang}/posts/{slug}/'
ARTICLE_LANG_SAVE_AS = ARTICLE_LANG_URL + 'index.html'

ARCHIVES_SAVE_AS = 'posts/index.html'

DRAFT_URL = 'drafts/{slug}/'
DRAFT_SAVE_AS = DRAFT_URL + 'index.html'
DRAFT_LANG_URL = '{lang}/drafts/{slug}/'
DRAFT_LANG_SAVE_AS = DRAFT_LANG_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'
PAGE_LANG_URL = '{lang}/{slug}/'
PAGE_LANG_SAVE_AS = PAGE_LANG_URL + 'index.html'

DRAFT_PAGE_URL = 'drafts/{slug}/'
DRAFT_PAGE_SAVE_AS = DRAFT_PAGE_URL + 'index.html'
DRAFT_PAGE_LANG_URL = '{lang}/drafts/{slug}/'
DRAFT_PAGE_LANG_SAVE_AS = DRAFT_PAGE_LANG_URL + 'index.html'

#AUTHOR_URL = 'authors/{slug}/'
#AUTHOR_SAVE_AS = AUTHOR_URL + 'index.html'
AUTHOR_SAVE_AS = ''  # Disable author pages
#AUTHORS_SAVE_AS = 'authors/index.html'
AUTHORS_SAVE_AS = ''  # Disable authors listing

CATEGORY_URL = 'categories/{slug}/'
CATEGORY_SAVE_AS = CATEGORY_URL + 'index.html'
CATEGORIES_SAVE_AS = 'categories/index.html'

TAG_URL = 'tags/{slug}/'
TAG_SAVE_AS = TAG_URL + 'index.html'
TAGS_SAVE_AS = 'tags/index.html'

DEFAULT_PAGINATION = 20

PAGINATION_PATTERNS = [
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/{number}/', '{base_name}/{number}/index.html'),
]


# Building & formatting settings
CACHE_CONTENT = False
STATIC_CHECK_IF_MODIFIED = True

DOCUTILS_SETTINGS = {
    "smart_quotes": True,
    "strip_comments": True,
    "math_output": "mathjax irrelevant.value",
    "toc_backlinks": "top",
}

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
GITHUB_SOURCE_URL = 'https://github.com/jwodder/kbits'
PATH_IN_REPO = PATH  # PATH relative to root of repository
SHOW_AUTHOR = True
LINK_AUTHOR = False
SHOW_AUTHOR_IN_LISTINGS = False

author_footer_link = 'https://github.com/jwodder'
site_creation_year = 2020
this_year = date.today().year
if this_year == site_creation_year:
    copyright_years = site_creation_year
else:
    copyright_years = f'{site_creation_year}–{this_year}'

FOOTER_HTML = f'''
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
    <img alt="Creative Commons License" style="border-width: 0; vertical-align: middle;" src="https://i.creativecommons.org/l/by/4.0/80x15.png" />
</a>

Copyright © {copyright_years} <a xmlns:cc="http://creativecommons.org/ns#"
href="{author_footer_link}" property="cc:attributionName"
rel="cc:attributionURL">{AUTHOR}</a>.  This site's content is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative
Commons Attribution 4.0 International License</a>.
'''

DISPLAY_CATEGORIES_ON_MENU = False

MENUITEMS = [
    ('Categories', 'categories/'),
    ('Tags', 'tags/'),
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
