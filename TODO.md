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
    - Add an author autopage
    - Plugins to use:
        - <https://github.com/pelican-plugins/seo> (Just do what it says)

- Adjust CSS:
    - Tweak the coloration of visited links
    - Convert all(?) px lengths to ems (1 em = font-size = 16px)

- Test pagination rendering and pagination URLs
    - Goals for pagination URLs:
        - Subsequent index pages: `/{n}/`
        - Subsequent category article listings: `/categories/{cat}/{n}/`
        - Subsequent tag article listings: `/tags/{tag}/{n}/`


Content To-Dos
--------------
- click-config:
    - Drop last example output?
    - Add section on dealing with `multiple`, `nargs`, & type-tuples?
- rst-hyperlinks.rst: Show outputs for more examples
