**Goal**: Create a `jwodder/kbits` repository on GitHub that is published as
<https://jwodder.github.io/kbits>

- When the site is first published:
    - Set all the articles' dates (or just the ones not previously published as
      Gists?) to that date (with varying times)
    - Update the original Gists (for those posts that originated as Gists) to
      point to the site

- Necessary settings for GitHub repository:
    - Settings > GitHub Pages > Source: master branch /docs folder
        - See <https://git.io/JJzXD>
    - Create a `404.html` page in the root of the output dir
        - Set `:Status: hidden` in the source

- For deployment to GitHub pages, use pre-commit to update the output
  directory?

- Set SITESUBTITLE

- Configure theme/style sheet
    - Themes gallery: <http://www.pelicanthemes.com>
        - Of interest:
            - <https://github.com/getpelican/pelican-themes/tree/master/dev-random>
            - <https://github.com/getpelican/pelican-themes/tree/master/dev-random2>
    - Read <https://www.smashingmagazine.com/2009/08/designing-a-html-5-layout-from-scratch/>?
    - Set up a tag cloud system? ("`tag_cloud`" plugin?)
    - Possible sources of styles:
        - `github.css` / GitHub
        - alabaster (Largely prefer over `sphinx_rtd_theme`)
        - `sphinx_rtd_theme`
        - Click theme?
    - Show SITESUBTITLE beneath SITENAME
    - Link to feeds in the document bodies (use feed logo image)
    - Add breadcrumbs to the tops of tag listings & category listings pages?
    - Put SITENAME and SITESUBTITLE at the top of the page; put the nav menu
      vertically on the left of the part of the page below it; put content to
      the right of the nav menu
        - Where should breadcrumbs go?
    - Add a favicon?
    - Improve display of article metadata in article pages
    - Use a large CC license image in the footer and have the footer text as a
      paragraph to the right of it?
    - Give the page structure `<div>`'s IDs which the CSS then refers to
    - Plugins to use:
        - <https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud>
        - <https://github.com/getpelican/pelican-plugins/tree/master/autopages>
          for adding descriptions to category/tag pages?
        - <https://github.com/pelican-plugins/more-categories>?
        - <https://github.com/davidlesieur/similar_posts>
        - <https://github.com/pelican-plugins/seo> (Just do what it says)
        - <https://github.com/pelican-plugins/sitemap>?

- Adjust CSS:
    - Remove border & background from TOCs?
    - Get post titles to be larger
    - Tweak the coloration of visited links?

- Test pagination rendering and pagination URLs
    - Goals for pagination URLs:
        - Subsequent index pages: `/{n}/`
        - Subsequent category article listings: `/categories/{cat}/{n}/`
        - Subsequent tag article listings: `/tags/{tag}/{n}/`
- Test display of "last modified" date


Content To-Dos
--------------

- powsum: Rename the variables so that `n` is the exponent
- click-config:
    - Drop last example output?
    - Add section on dealing with `multiple`, `nargs`, & type-tuples?
- unicode-latex: Add a paragraph at the end of the intro that says "Summary:
  Just use XeLaTeX/LuaLaTeX"?
