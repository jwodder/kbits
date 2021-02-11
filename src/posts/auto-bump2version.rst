==========================================
Integrating ``auto`` with ``bump2version``
==========================================

:Date: 2021-02-11
:Category: Programming
:Tags: GitHub Actions, auto, bump2version, continuous integration
:Summary:
    |auto|_ by Intuit lets you set up automatic creation of tags & releases and
    population of changelogs in a GitHub project.  It takes care of determining
    the version number for new releases, but, by default, it does not set the
    new version number in your code.  This isn't a problem if your project uses
    something like |setuptools_scm|_ or |versioneer|_ to fetch the version
    number from Git, but if your project's version number is hardcoded in your
    code, you'll need another solution.  |bump2version|_ is that solution, and
    it can be integrated into ``auto`` as shown here.

|auto|_ by Intuit lets you set up automatic creation of tags & releases and
population of changelogs in a GitHub project.  It takes care of determining the
version number for new releases, but, by default, it does not set the new
version number in your code.  This isn't a problem if your project uses
something like |setuptools_scm|_ or |versioneer|_ to fetch the version number
from Git, but if your project's version number is hardcoded in your code,
you'll need another solution.  |bump2version|_ is that solution, and it can be
integrated into ``auto`` as follows.

.. |auto| replace:: ``auto``
.. _auto: https://github.com/intuit/auto

.. |setuptools_scm| replace:: ``setuptools_scm``
.. _setuptools_scm: https://github.com/pypa/setuptools_scm

.. |versioneer| replace:: ``versioneer``
.. _versioneer: https://github.com/python-versioneer/python-versioneer

.. |bump2version| replace:: ``bump2version``
.. _bump2version: https://github.com/c4urself/bump2version


Set up ``bump2version``
=======================

To make your project's repository usable with ``bump2version``, create a
``.bumpversion.cfg`` (no "2"!) file as follows:

.. code:: ini

    [bumpversion]
    # Replace the value here with your project's current version number:
    current_version = 0.1.0

    commit = True

    # If integrating with GitHub Actions, you'll need to include "[skip ci]" in
    # the bump2version commit message in order to prevent auto from running
    # unnecessarily:
    message = [skip ci] Bump version: {current_version} → {new_version}

    # auto will be taking care of the tagging for us, so set `tag` to False:
    tag = False

    # For each file in your code that contains your project's version number,
    # add a `[bumpversion:file:PATH]` section header, like so:
    [bumpversion:file:src/myproject/__init__.py]

With this file in place and ``bump2version`` installed, you can automatically
update your project's version number by running ``bump2version $PART``, where
``$PART`` is the part of the version number to increase (``major``, ``minor``,
or ``patch``).

See `the bump2version documentation`__ for more information.

__ https://github.com/c4urself/bump2version/blob/master/README.md


Integrate with ``auto``
=======================

I assume `you've already set up auto for your repository`__.  To get ``auto``
to run ``bump2version`` automatically at the right time when creating a new
release, use the |exec plugin|_ to register an |afterChangelog|_ hook.  Add the
following to the ``"plugins"`` field in your repository's ``.autorc`` file::

    {
        ...
        "plugins": [
            ...
            [
                "exec",
                {
                    "afterChangelog": "bump2version \"$(printf '%s\n' \"$ARG_0\" | jq -r .bump)\""
                }
            ]
        ]
    }

.. tip::

    Despite what the ``exec`` documentation may imply, the ``$ARG_0``
    environment variable is a JSON object containing the payload passed to the
    respective hook.  This means we must extract the semantic version part to
    bump using ``jq``.

.. warning::

    **Do not** use ``echo`` in place of ``printf`` here!  The ``$ARG_0``
    variable contains JSON containing strings with ``\n`` escape sequences,
    which ``echo`` would convert into newlines, resulting in invalid JSON.

With this setting in place, ``auto`` will run ``bump2version`` on each new
release after populating the changelog, and the commit created by
``bump2version`` will be the commit to receive the new version tag.

__ https://intuit.github.io/auto/docs/welcome/getting-started

.. |exec plugin| replace:: ``exec`` plugin
.. _exec plugin: https://intuit.github.io/auto/docs/generated/exec

.. |afterChangelog| replace:: ``afterChangelog``
.. _afterChangelog: https://intuit.github.io/auto/docs/plugins
                    /release-lifecycle-hooks#afterchangelog


Integrate with GitHub Actions
=============================

Assuming you've already set up a GitHub Actions workflow for running ``auto``
(`see here <{filename}auto-post-release.rst>`_ for an example), the only
addition needed to support ``bump2version`` is to install it before running
``auto``:

.. code:: yaml

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '^3.6'

    - name: Install bump2version
      run: python -m pip install bump2version
