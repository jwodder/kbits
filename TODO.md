**Goal**: Create a `jwodder/kbits` repository on GitHub that is published as
<https://jwodder.github.io/kbits>

- When the site is first published, set all the articles' dates to that date

- Necessary settings for GitHub repository:
    - Settings > GitHub Pages > Source: master branch /docs folder
        - See <https://git.io/JJzXD>
    - Create a `404.html` page in the root of the output dir
        - Set `:Status: hidden` in the source

- For deployment to GitHub pages, use pre-commit to update the output
  directory?
    - Use ghp-import or ghp-import2?

- Set up math rendering using MathJax
    - This will require changing `DOCUTILS_SETTINGS["math_output"]` in
      `pelicanconf.py` and also including the proper scripts in the article
      template.

- Configure theme/style sheet
    - Themes gallery: <http://www.pelicanthemes.com>
    - Read <https://www.smashingmagazine.com/2009/08/designing-a-html-5-layout-from-scratch/>?
    - The theme should use articles' summaries, show the site title in the
      `<title>`, and enable MathJax in templates
    - Use tags to set "keywords" meta in HTML output?
    - Don't link to author pages
    - Include links to archives, tag list, & category list in main menu or
      somewhere
    - Link pages to their source on GitHub ("Show Source" plugin?)
    - Set up a tag cloud system ("`tag_cloud`" plugin?)
    - Possible sources of styles:
        - `github.css`
        - `sphinx_rtd_theme`
        - alabaster
        - Click theme

- Plugins to consider using:
    - `tag_cloud`
    - Footer Insert
    - better code line numbers?
    - auto pages?
    - render math?
    - more categories?
    - multi neighbors / neighbor articles
    - pelican link class?
    - pelican page hierarchy?
    - related posts?
    - series?
    - show source?
    - similar posts?
    - sitemap?

- Gists to import into site:
    - rst-hyperlinks.rst <https://gist.github.com/jwodder/5a9264db8c3c81dad4c01e082515a9f1>
    - unicode-latex.rst <https://gist.github.com/jwodder/c82599dea8ae3168e39297aede014622>
    - click-config.rst <https://gist.github.com/jwodder/8ce218892331229c9116ed6c3e16a5bb>

- Do something with `Makefile` and/or `tasks.py`
