**Goal**: Create a `jwodder/kbits` repository on GitHub that is published as
<https://jwodder.github.io/kbits>

- When the site is first published:
    - Set all the articles' dates to that date
    - Update the original Gists (for those posts that originated as Gists) to
      point to the site

- Necessary settings for GitHub repository:
    - Settings > GitHub Pages > Source: master branch /docs folder
        - See <https://git.io/JJzXD>
    - Create a `404.html` page in the root of the output dir
        - Set `:Status: hidden` in the source

- For deployment to GitHub pages, use pre-commit to update the output
  directory?

- Configure theme/style sheet
    - Themes gallery: <http://www.pelicanthemes.com>
    - Read <https://www.smashingmagazine.com/2009/08/designing-a-html-5-layout-from-scratch/>?
    - The theme should use articles' summaries and show the site title in the
      `<title>`
    - Articles' full contents should only be shown on the articles' pages;
      listing of articles should always use summaries
    - Use tags to set "keywords" meta in HTML output?
    - Use summary to set "description" meta?
    - Add `<link rel="canonical" href="$THIS_URL"/>` to HTML heads?
    - Don't link to author pages
        - Make author name link to my GitHub page?
    - Include links to archives, tag list, & category list in main menu or
      somewhere
    - Link pages to their source on GitHub
        - Use `GITHUB_URL` setting
    - Set up a tag cloud system ("`tag_cloud`" plugin?)
    - Give all output documents a footer that says:

            Copyright © 2020 John T. Wodder II.  This work is licensed under a
            `Creative Commons Attribution 4.0 International License`_.

            .. _Creative Commons Attribution 4.0 International License:
               http://creativecommons.org/licenses/by/4.0/

        (Maybe adjust the intro a little.)

    - Remove archives page in favor of index?
    - Possible sources of styles:
        - `github.css`
        - `sphinx_rtd_theme`
        - alabaster
        - Click theme
    - Use a Pygments stylesheet
    - Figure out to to get math rendering applied to templated article listings
    - Plugins to use:
        - <https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud>
        - <https://github.com/getpelican/pelican-plugins/tree/master/footer_insert>
          for its ability to insert the article date as the copyright date?
            - Alternatively, set the footer as a settings variable that
              dynamically includes a range from the site start year to the
              current year
        - <https://github.com/getpelican/pelican-plugins/tree/master/autopages>
          for adding descriptions to category/tag pages?
        - <https://github.com/pelican-plugins/more-categories>?
        - <https://github.com/davidlesieur/similar_posts>
        - <https://github.com/pelican-plugins/seo> (Just do what it says)
        - <https://github.com/pelican-plugins/sitemap>?

- Add license file to repo?
