**Goal**: Create a `jwodder/kbits` repository on GitHub that is published as
<https://jwodder.github.io/kbits>

- When the site is first published:
    - Set all the articles' dates (or just the ones not previously published as
      Gists?) to that date (with varying times)
    - Update the original Gists (for those posts that originated as Gists) to
      point to the site
    - Move theme directory to its own repository (kbits-theme), afterwards
      imported as a Git submodule
        - Write a README for the theme describing its features & configuration
        - Set up a kbits-theme-demo site
        - At some point, improve how translations are shown

- Necessary settings for GitHub repository:
    - Settings > GitHub Pages > Source: gh-pages branch
        - See <https://git.io/JJzXD>
    - Set up a GitHub Action to build & deploy the site

- Configure theme/style sheet
    - Themes gallery: <http://www.pelicanthemes.com>
    - Read <https://www.smashingmagazine.com/2009/08/designing-a-html-5-layout-from-scratch/>?
    - Add a favicon?
    - Merge CSS files together by origin
    - Add an author page at either `/author/` or `/jwodder/` and have the
      default author name in posts link there
        - Add an `AUTHOR_LINK` setting for setting the link for `AUTHOR`?
            - Alternatively, support an `AUTHOR_LINKS: Dict[str,
              Optional[str]]` setting?
            - Allow URL to be either relative (in which case it's prefixed with
              SITEURL) or absolute
    - Plugins to use:
        - <https://github.com/getpelican/pelican-plugins/tree/master/autopages>
          for adding descriptions to category/tag pages?
        - <https://github.com/pelican-plugins/seo> (Just do what it says)

- Adjust CSS:
    - Tweak the coloration of visited links

- Test pagination rendering and pagination URLs
    - Goals for pagination URLs:
        - Subsequent index pages: `/{n}/`
        - Subsequent category article listings: `/categories/{cat}/{n}/`
        - Subsequent tag article listings: `/tags/{tag}/{n}/`


Content To-Dos
--------------
- powsum: Rename the variables so that `n` is the exponent
- click-config:
    - Drop last example output?
    - Add section on dealing with `multiple`, `nargs`, & type-tuples?
- unicode-latex: Add a paragraph at the end of the intro that says "Summary:
  Just use XeLaTeX/LuaLaTeX"?
- rst-hyperlinks.rst: Show outputs for more examples
