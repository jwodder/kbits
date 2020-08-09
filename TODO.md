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
    - Show SITESUBTITLE beneath/beside SITENAME
    - Link to feeds in the document bodies (Use feed logo image)
    - Add breadcrumbs to the tops of tag listings & category listings pages?
    - Add a favicon?
    - Improve display of article metadata in article listings
    - Give the page structure `<div>`'s IDs which the CSS then refers to
    - Don't use `<h1>` for site title
    - Get rid of unused styles & IDs from templates
    - Merge CSS files together by origin
    - Plugins to use:
        - <https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud>
        - <https://github.com/getpelican/pelican-plugins/tree/master/autopages>
          for adding descriptions to category/tag pages?
        - <https://github.com/davidlesieur/similar_posts>
        - <https://github.com/pelican-plugins/seo> (Just do what it says)
        - <https://github.com/pelican-plugins/sitemap>?

- Adjust CSS:
    - Tweak the coloration of visited links
    - Prevent `.align-*` on a table from affecting the alignment of text within
    - Add vertical space above copyright footer

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
- rst-hyperlinks.rst: Show outputs for more examples
