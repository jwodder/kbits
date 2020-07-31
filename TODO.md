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
    - The theme should show the site title in the `<title>`
    - Articles' full contents should only be shown on the articles' pages;
      listing of articles should always use summaries
    - Add `<link rel="canonical" href="$THIS_URL"/>` to HTML heads?
    - Don't link to author pages
        - Make author name link to my GitHub page?
    - Set up a tag cloud system ("`tag_cloud`" plugin?)
    - Possible sources of styles:
        - `github.css` / GitHub
        - alabaster (Largely prefer over `sphinx_rtd_theme`)
        - `sphinx_rtd_theme`
        - Click theme?
    - Figure out how to get math rendering applied to templated article
      listings
        - Bug: <https://github.com/pelican-plugins/render-math/issues/7>
        - Give up on the render math plugin and hardcode MathJax into every
          page?
    - Show "last modified" date in article listings
    - Show SITESUBTITLE beneath SITENAME
    - Eliminate the "all categories" and "all tags" pages and instead list all
      categories & tags on the side of every page?
    - Possible URL layouts:
        - System 1:
            - Index: `index.html`
                - Subsequent pages: `index2.html`
            - Article/page: `{slug}.html`
            - Category list: `categories.html`
                - Change to `categories/` and pluralize category page basedir?
            - Category page: `category/{cat}.html`
                - Subsequent pages: `category/{cat}2.html`
            - Tag list: `tags.html`
                - Change to `tags/` and pluralize tag page basedir?
            - Tag page: `tag/{tag}.html`
                - Subsequent pages: `tag/{tag}2.html`
        - System 2:
            - Index: `/`
                - Subsequent pages: `/{n}/`?
            - Article/page: `/{slug}/`
            - Category list: `/categories/`
            - Category page: `/categories/{cat}/`
                - Subsequent pages: `/categories/{cat}/{n}/`
            - Tag list: `/tags/`
            - Tag page: `/tags/{tag}/`
                - Subsequent pages: `/tags/{tag}/{n}/`
    - Set pagination to 50 or so?
    - Plugins to use:
        - <https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud>
        - <https://github.com/getpelican/pelican-plugins/tree/master/autopages>
          for adding descriptions to category/tag pages?
        - <https://github.com/pelican-plugins/more-categories>?
        - <https://github.com/davidlesieur/similar_posts>
        - <https://github.com/pelican-plugins/seo> (Just do what it says)
        - <https://github.com/pelican-plugins/sitemap>?

- Add license file to repo?
