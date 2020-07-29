**Goal**: Create a `jwodder/kbits` repository on GitHub that is published as
<https://jwodder.github.io/kbits>

- Gists to import into site:
    - rst-hyperlinks.rst <https://gist.github.com/jwodder/5a9264db8c3c81dad4c01e082515a9f1>
    - unicode-latex.rst <https://gist.github.com/jwodder/c82599dea8ae3168e39297aede014622>
    - click-config.rst <https://gist.github.com/jwodder/8ce218892331229c9116ed6c3e16a5bb>

- Use Pelican <https://docs.getpelican.com/en/stable/>
    - Themes gallery: <http://www.pelicanthemes.com>
    - Relevant plugins:
        - tag_cloud
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

- Configure theme/style sheet
    - The theme should use articles' summaries and show the site title in the
      `<title>`
    - Possible sources of styles:
        - `github.css`
        - `sphinx_rtd_theme`
        - alabaster
        - Click theme

- Set up a tag cloud system

- For deployment to GitHub pages, use pre-commit to update the output directory?
