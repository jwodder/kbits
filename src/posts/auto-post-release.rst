===================================================================
Running Extra Steps after Releasing with ``auto`` in GitHub Actions
===================================================================

:Date: 2020-10-26
:Modified: 2024-05-22
:Category: Programming
:Tags: GitHub Actions, auto, continuous integration
:Summary:
    Let's say you've set up |auto|_ for your project via a GitHub Actions
    workflow, and now you want that workflow to carry out additional steps —
    such as building & uploading assets — whenever ``auto`` creates a new
    release.  Let's also say that none of the available plugins for ``auto``
    covers your use-case and you're not a JavaScript programmer, so you won't
    be writing a new plugin to do what you want.  How do you adjust your GitHub
    Actions workflow to run these extra steps at the right time?  Read to find
    out.

Let's say you've set up |auto|_ for your project via a GitHub Actions workflow,
and now you want that workflow to carry out additional steps — such as building
& uploading assets — whenever ``auto`` creates a new release.  Let's also say
that none of the available plugins for ``auto`` covers your use-case and you're
not a JavaScript programmer, so you won't be writing a new plugin to do what
you want.  How do you adjust your GitHub Actions workflow to run these extra
steps at the right time?  Read on to find out.

.. |auto| replace:: ``auto``
.. _auto: https://github.com/intuit/auto

----

So you've got a GitHub Actions workflow for ``auto`` already set up.
Presumably, it looks something liks this:

.. code:: yaml

    name: Auto-release on PR merge

    on:
      # This is the closest thing to triggering on a PR merge, as long as you
      # don't push directly to master.
      push:
        branches:
          - master

    jobs:
      auto-release:
        runs-on: ubuntu-latest
        if: "!contains(github.event.head_commit.message, 'ci skip') && !contains(github.event.head_commit.message, 'skip ci')"
        steps:
          - name: Checkout source
            uses: actions/checkout@v4
            with:
              fetch-depth: 0

          - name: Download latest auto
            run: |
              auto_download_url="$(curl -fsSL https://api.github.com/repos/intuit/auto/releases/latest | jq -r '.assets[] | select(.name == "auto-linux.gz") | .browser_download_url')"
              wget -O- "$auto_download_url" | gunzip > ~/auto
              chmod a+x ~/auto

          - name: Create release
            run: ~/auto shipit
            env:
              GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

Now you want to insert further steps that will be triggered whenever ``auto
shipit`` successfully creates a new release.

For simple cases — where the commands to run can be expressed in a single shell
command — we can use ``auto``'s |exec plugin|_ to run the desired commands via
the ``afterRelease`` hook.  For example, building & uploading a Python package
for PyPI can be integrated into ``auto`` by adding the following item to the
``"plugins"`` field in the repository's ``.autorc`` file::

    {
        ...
        "plugins": [
            ...
            [
                "exec",
                {
                    "afterRelease": "python -m build && twine upload/*"
                }
            ]
        ]
    }

(This particular example assumes that the appropriate Python dependencies are
already set up earlier in the workflow and that the twine username & password
are passed as environment variables to the ``~/auto shipit`` step.)

.. |exec plugin| replace:: ``exec`` plugin
.. _exec plugin: https://intuit.github.io/auto/docs/generated/exec

For more complex post-release activity which can only be implemented as GitHub
Actions steps, we need something else.  Just adding the steps and nothing else
directly to the workflow won't work, as ``auto shipit`` doesn't always create a
new release, such as when a pull request with a ``skip-release`` label is
merged, or when a pull request without a ``release`` label is merged while
``onlyPublishWithReleaseLabel`` is set to ``true``.  So we need some logic to
test whether there's a new release.

Theoretically, one option would be to create a separate workflow that runs
whenever a new tag is pushed or a new GitHub release is created, but this won't
work with an out-of-the-box setup; ``auto`` uses ``GITHUB_TOKEN`` to create the
tag & release, and GitHub Actions workflows `specifically do not trigger`__ on
events performed with a ``GITHUB_TOKEN``.  You could get this approach to work
by passing ``auto`` a personal access token instead of ``GITHUB_TOKEN``, but
there's a more direct way to make this work instead that also lets you keep
your release-related workflow steps in a single file.

__ https://docs.github.com/en/actions/using-workflows/triggering-a-workflow
   #triggering-a-workflow-from-a-workflow

Here's the key trick: By running |auto version|_ before ``auto shipit``, you
find out whether ``auto`` is about to create a new release, and you can save
the output from ``auto version`` to use to trigger extra steps later.  If
``auto`` is about to create a new release, ``auto version`` will output the
release level ("``patch``", "``minor``", or "``major``"); otherwise, if ``auto
shipit`` would do nothing, ``auto version`` just outputs an empty line.

.. |auto version| replace:: ``auto version``
.. _auto version: https://intuit.github.io/auto/docs/generated/version

Hence, insert the following step before the ``auto shipit`` step:

.. code:: yaml

          - name: Check whether a release is due
            id: auto-version
            run: |
              version="$(~/auto version)"
              echo "version=$version" >> "$GITHUB_OUTPUT"
            env:
              GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

Here, we use a `workflow command`_ to make the output from ``auto version``
available to subsequent steps.  Later steps can then be configured to only run
if a new release is being made by adding an |if field|_ to them, like so:

.. _workflow command: https://docs.github.com/en/actions/using-workflows/
                      workflow-commands-for-github-actions
                      #setting-an-output-parameter

.. |if field| replace:: ``if`` field
.. _if field: https://docs.github.com/en/actions/using-workflows/
              workflow-syntax-for-github-actions#jobsjob_idstepsif

.. code:: yaml

          - name: Build asset for new release
            run: ...
            if: steps.auto-version.outputs.version != ''

If you have multiple steps that you want to run after a release, adding an
``if`` field to all of them can become excessive; isn't there a way to apply an
``if`` to a whole block of steps?  There is indeed; you can split off the extra
steps into a separate job in the same workflow and have that entire job be
guarded by a single ``if``.

First, in order to make the output from the ``auto version`` step available to
other jobs in the workflow, you need to add an |outputs field|_ to the original
``auto`` job (the one that in the example above is named "``auto-release``"),
at the same level as the ``runs-on`` and ``steps`` keys.  This ``outputs``
field should contain a YAML object mapping a name for the output value to a
``${{ steps.….outputs.… }}`` expression that evaluates to the output from the
``auto version`` step.  For the example workflow configurations shown so far,
this would mean a configuration like the following:

.. |outputs field| replace:: ``outputs`` field
.. _outputs field: https://docs.github.com/en/actions/using-workflows/
                   workflow-syntax-for-github-actions#jobsjob_idoutputs

.. code:: yaml

    jobs:
      auto-release:
        runs-on: ubuntu-latest
        if: "!contains(github.event.head_commit.message, 'ci skip') && !contains(github.event.head_commit.message, 'skip ci')"
        ### vv Add this bit vv ###
        outputs:
          auto-version: ${{ steps.auto-version.outputs.version }}
        ### ^^ Add this bit ^^ ###
        steps:
          # ...

With this in place, a new job can be added to the workflow containing all the
steps you want to run after a new release is made.  This new job needs two
special fields (at the same level as ``runs-on`` and ``steps``):

- A |needs field|_ containing the job ID of the ``auto`` job (so ``needs:
  auto-release`` for the examples given here) to declare a dependency on it

  .. |needs field| replace:: ``needs`` field
  .. _needs field: https://docs.github.com/en/actions/using-workflows/
                   workflow-syntax-for-github-actions#jobsjob_idneeds

- An ``if`` field containing an expression of the form
  ``needs.AUTO_JOB_NAME.outputs.AUTO_VERSION_OUTPUT_NAME != ''`` (so ``if:
  needs.auto-release.outputs.auto-version != ''`` for the examples given here);
  this causes the job to be skipped if ``auto version`` outputs nothing, i.e.,
  if no release is made

The configuration for this new job would then look like:

.. code:: yaml

    jobs:

      # `auto release` job from above omitted
      # ...

      build-and-publish:
        runs-on: ubuntu-latest
        needs: auto-release
        if: needs.auto-release.outputs.auto-version != ''
        steps:
          # ...

There's one more thing to be aware of: If you check out your repository in this
new job, by default the HEAD will be the commit that triggered the workflow
originally and will not include the changelog commit or tag created by
``auto``.  If you need the commit or tag (say, because your project uses
|setuptools_scm|_ or the like to derive its version number from Git tags at
build time), you can tell the ``actions/checkout`` action to check out the
latest commit from the repository by passing the default branch as the ``ref``
input like so:

.. |setuptools_scm| replace:: ``setuptools_scm``
.. _setuptools_scm: https://pypi.org/project/setuptools-scm/

.. code:: yaml

      - name: Checkout source
        uses: actions/checkout@v4
        with:
          ref: master  # or `main` or whatever your default branch is
          # This setting is needed to fetch tags:
          fetch-depth: 0

This does come with a caveat, though: in the event that multiple commits or
merges to the default branch were made in quick succession, you may end up
checking out a later commit than the tag that ``auto`` created.  If this is a
problem, one way to deal with it is to specifically check out the tag for the
latest GitHub release, like so:

.. code:: yaml

      - name: Get tag of latest release
        id: latest-release
        run: |
          latest_tag="$(curl -fsSL https://api.github.com/repos/$GITHUB_REPOSITORY/releases/latest | jq -r .tag_name)"
          echo "tag=$latest_tag" >> "$GITHUB_OUTPUT"

      - name: Checkout source
        uses: actions/checkout@v4
        with:
          ref: ${{ steps.latest-release.outputs.tag }}
          fetch-depth: 0

This, of course, fails if ``auto`` creates multiple tags in quick succession.
I'm not aware of a decent way to deal with this eventuality; how about
`listening to the docs`__ and just not running ``auto`` that often in the first
place?

__ https://intuit.github.io/auto/docs/welcome/quick-merge

Using all of these tricks, your final workflow configuration should look
something like this:

.. code:: yaml

    name: Auto-release on PR merge

    on:
      # This is the closest thing to triggering on a PR merge, as long as you
      # don't push directly to master.
      push:
        branches:
          - master

    jobs:
      auto-release:
        runs-on: ubuntu-latest
        if: "!contains(github.event.head_commit.message, 'ci skip') && !contains(github.event.head_commit.message, 'skip ci')"
        outputs:
          auto-version: ${{ steps.auto-version.outputs.version }}
        steps:
          - name: Checkout source
            uses: actions/checkout@v4
            with:
              fetch-depth: 0

          - name: Download latest auto
            run: |
              auto_download_url="$(curl -fsSL https://api.github.com/repos/intuit/auto/releases/latest | jq -r '.assets[] | select(.name == "auto-linux.gz") | .browser_download_url')"
              wget -O- "$auto_download_url" | gunzip > ~/auto
              chmod a+x ~/auto

          - name: Check whether a release is due
            id: auto-version
            run: |
              version="$(~/auto version)"
              echo "version=$version" >> "$GITHUB_OUTPUT"
            env:
              GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

          - name: Create release
            run: ~/auto shipit
            env:
              GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      build-and-publish:
        runs-on: ubuntu-latest
        needs: auto-release
        if: needs.auto-release.outputs.auto-version != ''
        steps:
          - name: Get tag of latest release
            id: latest-release
            run: |
              latest_tag="$(curl -fsSL https://api.github.com/repos/$GITHUB_REPOSITORY/releases/latest | jq -r .tag_name)"
              echo "tag=$latest_tag" >> "$GITHUB_OUTPUT"

          - name: Checkout source
            uses: actions/checkout@v4
            with:
              ref: ${{ steps.latest-release.outputs.tag }}
              fetch-depth: 0

          # Remaining steps go here
          # ...

Enjoy!
