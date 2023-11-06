================================
Common Python Packaging Mistakes
================================

:Date: 2020-08-22
:Modified: 2021-03-22
:Category: Programming
:Tags: Python, Python packaging, setuptools, best practices, advice
:Summary:
    An overview of common mistakes made in creating & building a Python package
    and how to avoid them

.. role:: py(code)
    :language: python

I think we can all agree that packaging a Python project is harder than it
should be.  With numerous guides & tutorials out there, people still make
mistakes.  Some of these mistakes break a project, some just make it less
attractive, and some even cause a project to step on the toes of other
projects.

As the admin of the wheel-analysis and -browsing site Wheelodex_, I see a
number of poorly-built wheels each morning as I peruse the day's new entries.
This eventually motivated me to create check-wheel-contents_ — a program for
scanning a wheel for many of the below problems plus several others — in an
attempt to get people to clean up their wheels, yet still the poorly-packaged
projects persist.

In yet another attempt to get people to fix their broken packages, here now are
some of the more frequent types of mistakes I see — along with advice on how to
avoid & correct them — in no particular order.

.. _Wheelodex: https://www.wheelodex.org
.. _check-wheel-contents: https://github.com/jwodder/check-wheel-contents

.. note::

    Unless otherwise specified, references to packaging configurations assume
    that the project is using setuptools and that configuration is being placed
    in ``setup.py`` instead of ``setup.cfg``.  Consult the appropriate
    documentation if your project is structured differently.

.. contents::


Avoiding General Mistakes
=========================

First, some general advice that will help you avoid (or at least detect) the
vast majority of packaging errors.


Look at Your Built Distributions
--------------------------------

Before you upload your sdist and wheel (especially if it's your first release
for the project in question), actually take a look at what files are inside and
make sure that everything you want to include is in there.  An sdist is either
a tarball (``*.tar.gz``) or a zipfile (``*.zip``), so its contents can be
listed with one of these two commands:

.. code:: shell

    # Tarball
    $ tar ztf projectname-version.tar.gz

    # Zipfile
    $ zipinfo projectname-version.zip

At time of writing, the exact layout of an sdist has yet to be standardized,
but if you're building with a recent version of setuptools, the contents are
structured as follows:

- Everything in the sdist is inside a top-level directory named
  ``{projectname}-{version}/``.  This directory contains a copy of your package
  code, the project's ``setup.py``/``pyproject.toml`` file, and various other
  files from your project directory; see `here <a MANIFEST.in file_>`_ for more
  information on what gets included by default.

- There exists a ``PKG-INFO`` file containing the project metadata.  For
  historical reasons, this does not include project dependencies.

- Next to your Python package, there is a ``{projectname}.egg-info/`` directory
  containing more metadata, including a copy of ``PKG-INFO``, a ``SOURCES.txt``
  file listing the files in the sdist, and a ``requires.txt`` file listing your
  project's dependencies.  Other files may be present depending on what
  features your project uses.

If your sdist is missing some files from your project directory or contains
some files that you don't want in there, then (assuming you're building your
project with setuptools), you can adjust what gets included via |a MANIFEST.IN
file|_ and rebuild.

.. |a MANIFEST.in file| replace:: a ``MANIFEST.in`` file
.. _a MANIFEST.in file: https://packaging.python.org/guides/using-manifest-in/

.. note::

    Exactly what files should and should not be included in an sdist is, for
    the most part, largely a matter of opinion, but your sdist needs to include
    your Python code and anything from your project directory that's needed to
    built a complete wheel.  The files that setuptools includes by default
    should generally be left in there, and most people will recommend also
    including tests and documentation.  Things that should generally be left
    out include ``*.pyc`` files, repository metadata like ``.gitignore`` and
    ``.hgtags``, and (except in special circumstances) anything that you
    wouldn't commit to version control.

Wheels (``*.whl``), meanwhile, are just zipfiles with a funny extension, so you
can list their contents with ``zipinfo``.  The basic layout of a wheel is as
follows:

- Your Python package is located at the root of the wheel, rather than inside
  a directory.

- There exists a ``{projectname}-{version}.dist-info/`` directory containing
  metadata: a ``METADATA`` file describing the project (similar to an sdist's
  ``PKG-INFO``, but including dependencies), a ``WHEEL`` file describing the
  wheel version and tags, and a ``RECORD`` file listing the files in the wheel
  and their hashes.  Licenses included in the wheel with the ``license_files``
  setting also end up in this directory.  Other files may also be present
  depending on what features your project uses and the versions of setuptools
  and wheel used to build the wheel.

- If your project includes any files that are installed outside of
  ``site-packages`` — headers, scripts, data files (not to be confused with
  package data), etc. — they are stored in a ``{projectname}-{version}.data/``
  directory.  Files in this directory are organized into subdirectories named
  after the distutils scheme keys (``purelib``, ``platlib``, ``headers``,
  ``scripts``, or ``data``) that map to the files' install locations.

.. note::

    Aside from the ``*.dist-info/`` and ``*.data/`` directories, a wheel should
    only contain Python packages & modules, consisting of code and data files.
    Files like your project's ``setup.py``, ``pyproject.toml``, ``setup.cfg``,
    etc. do not belong in a wheel.

Controlling what gets included in a wheel is more involved than for an sdist
(when using setuptools, at least); consult documentation elsewhere on how to do
this.

.. warning::

    Do NOT try to fix your sdists or wheels by manually adding, removing, or
    editing the files inside, as this is likely to make the sdist/wheel
    invalid.  Instead, change your project configuration and create new built
    distributions until you get what you want — |delbuild|_

.. |delbuild| replace:: and be sure to delete the ``build/`` directory in
   between builds!
.. _delbuild: `rebuild noclean`_


Installations are Not Namespaced
--------------------------------

A key thing to understand about how Python packages are installed is that
(almost) all of the files in a wheel are simply placed directly in
``site-packages/``; the only subdirectories present will be the directories
that are already in the wheel.  This means that, if your wheel has a ``foo/``
directory at the top level containing ``bar.py``, then ``bar.py`` will be
installed to ``site-packages/foo/bar.py``; nothing is added to the path to
separate it from other packages' ``foo/bar.py`` files.  Properly namespacing
your files must be done by putting everything under a directory (normally your
top-level Python package) with a name the same as or similar to the name of
your project — which is the standard practice anyway.  Where problems arise is
when a top-level file or directory in a wheel has a name that other projects
are also likely to use, in which case files end up overwritten with the wrong
content and bugs result.

See `pip issue #4625 <https://github.com/pypa/pip/issues/4625>`_ for pip's
attempts at handling file collisions whenever they arise.


Top-Level ``tests/`` Directory in Wheel
=======================================

The first (and probably most common) Python packaging mistake occurs when you
put your tests in a ``tests/`` directory at the root of your project (outside
of your Python package) and then include this directory in your project's
wheels.  The ``tests/`` directory then ends up placed at the top-level of your
wheel's filesystem, and, `as stated above <Installations are Not
Namespaced_>`_, this means that it will be installed at
``site-packages/tests/``.  The problem comes from the fact that "``tests/``" is
a name that *everybody* uses for their tests and too many other projects also
include a top-level ``tests/`` directory in their wheels.  As a result,
``site-packages/tests/`` becomes a mish-mash of code from different packages,
some files even overwriting each other, and if someone tries to run those
tests, chaos will ensue.  (And if you don't expect people to be running your
tests from your installed project, why are you including tests in the wheel in
the first place?)

The most common reason why ``tests/`` ends up included in wheels is because the
project's author used ``find_packages()`` in their ``setup.py`` but didn't use
the function's ``exclude`` argument.  ``find_packages()`` works by searching
for directories in the project root (or in the directory passed as the
``where`` argument) that contain an ``__init__.py`` file, and then it searches
those directories for any subdirectories that also contain an ``__init__.py``
file, and so on until it runs out of directories with ``__init__.py`` files.
Sometimes, people put an ``__init__.py`` file in ``tests/`` (Whether this is
necessary depends on the test framework being used), and so ``find_packages()``
with the default arguments picks it up and adds it to the project's list of
packages, resulting in it being included in the wheel.

To avoid this, you have five options:

1. Remove the ``__init__.py`` files from your ``tests/`` directory and its
   subdirectories.  Whether this is doable depends on your test framework.

2. Use ``find_packages()``'s ``exclude`` argument to exclude ``tests/`` and its
   subdirectories like so:

   .. code:: python

       packages=find_packages(exclude=["tests", "tests.*"])

   Note that we list both :py:`"tests"` and :py:`"tests.*"`.  Listing just
   :py:`"tests"` would exclude ``tests/`` but not its subdirectories, so we
   need to also list :py:`"tests.*"` in order to exclude everything.

3. Use ``find_packages()``'s ``include`` argument to include only your Python
   package and its subpackages like so:

   .. code:: python

       packages=find_packages(include=["packagename", "packagename.*"])

   As with ``exclude``, we list both the package name and the package name
   followed by "``.*``" so that all subpackages of the package will be matched
   & included.

4. Move your ``tests/`` directory inside your Python package directory so it's
   no longer at the top level.

   .. _src:

5. Switch your project to a ``src/`` layout, where your Python package
   directory is located inside a directory named ``src/`` and everything else —
   including ``tests/`` — is outside of ``src/``.  With this layout, simply
   write your ``packages`` line as :py:`packages=find_packages("src")`, and
   ``find_packages()`` will only look at what's in ``src/``.

   Note that you will also need to add :py:`package_dir={"": "src"}` to your
   ``setup()`` arguments in order for setuptools to grok your layout.  More
   information about the ``src/`` layout can be found here__ and here__.

   __ https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
   __ https://hynek.me/articles/testing-packaging/

The second most common reason why ``tests/`` ends up in wheels is that the
project author used the ``exclude`` argument to ``find_packages()`` but listed
only :py:`"tests"` and not :py:`"tests.*"`, and so the subdirectories of
``tests/`` (inside an otherwise-empty ``tests/`` directory) ended up in the
wheel.  Both :py:`"tests"` and :py:`"tests.*"` need to be included in the
``exclude`` list in order to exclude the entire ``tests/`` hierarchy.

Besides ``tests/``, it is also a problem to include a top-level directory named
``test/`` (singular), ``docs/``, ``examples/``, ``data/``, or similar, as such
directories are also often included in wheels despite the clashes that will
result.

Do note that, when it comes to sdists, it's perfectly fine to have a ``tests/``
etc. directory at the base of your project, as sdists themselves are not
installed, they're just used to build wheels, which are what actually get
installed.


Top-Level ``README`` or ``LICENSE`` File in Wheel
=================================================

Similarly to the above mistake involving ``tests/``, it is also a bad idea to
include your project's ``README.rst``/``README.md`` or ``LICENSE`` file (or
``CHANGELOG`` or really anything that's not a Python module or ``*.pth`` file)
at the root of your wheel, as it will collide with the ``README``\s and
``LICENSE``\s of other projects that do the same thing.

This mistake is particularly common among projects built using `Poetry
<https://python-poetry.org>`_, where simple usage of the ``include`` option
adds files directly into both the sdist and wheel.  To include a file in only
the sdist, one needs to change the ``include`` option from this form:

.. code:: toml

    [tool.poetry]
    include = ["CHANGELOG.md"]

to this form:

.. code:: toml

    [tool.poetry]
    include = [
        { path = "CHANGELOG.md", format = "sdist" }
    ]

If you do want to include your ``README`` or ``LICENSE`` in your wheel, the
correct way is as follows:

- For ``README``, the file's contents should already be used as the project's
  (long) description, in which case the contents are already included in the
  project metadata, which is stored in ``PKG-INFO`` (for sdists) or
  ``*.dist-info/METADATA`` (for wheels), and thus there is no need to include
  the ``README`` as a separate file.  If you need to be able to retrieve the
  ``README``'s contents at runtime, this can be done by using
  |importlib.metadata|_ or similar to fetch the project's description.

  .. |importlib.metadata| replace:: ``importlib.metadata``
  .. _importlib.metadata:
     https://docs.python.org/3/library/importlib.metadata.html

- Licenses and related files belong inside a wheel's ``*.dist-info`` directory.
  If using setuptools with wheel 0.32 or higher, licenses can be placed there
  by passing them to the ``[metadata]license_files`` option in ``setup.cfg``;
  `see the wheel documentation for more information`__.

  At time of writing, Poetry does not support adding license files to a wheel's
  ``*.dist-info`` directory, but `PR #1367`__ would change that.

  __ https://wheel.readthedocs.io/en/stable/user_guide.html
     #including-license-files-in-the-generated-wheel-file

  __ https://github.com/python-poetry/poetry/pull/1367


Project Description Doesn't Render
==================================

The Python Package Index (PyPI) supports project (long) descriptions written in
three possible formats: reStructuredText_ (the default if no format is
specified), Markdown (either `GitHub Flavored Markdown`_ or CommonMark_), and
plain text.  Markdown and plain text are lenient formats; anything you write in
them is valid.  However, documents written in reStructuredText can be
malformed, producing errors & warning messages when rendered.  When a project
with a malformed reStructuredText description (either because it uses
reStructuredText incorrectly or because it's actually Markdown that wasn't
declared as Markdown) is uploaded to PyPI, PyPI does one of the following two
things:

.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _GitHub Flavored Markdown: https://github.github.com/gfm/
.. _CommonMark: https://commonmark.org

- If the project does not declare a ``Content-Type`` for its malformed
  description, PyPI will fall back to displaying the source of the description
  as though it were plain text.

- If the project explicitly declares the malformed description's
  ``Content-Type`` as reStructuredText (i.e., as the MIME type ``text/x-rst``),
  PyPI will reject the upload.

Neither situation is desirable, but at least the latter gives you the chance to
correct your project description before it's released on PyPI, while the former
situation means your project's PyPI page shows an ugly, unprofessional-looking
description until you make a new release.

.. note::

    When using setuptools, you may find that your project's long description
    has been mangled somewhat, with a bunch of "Field: Value" entries added to
    the bottom and various information missing from the listing on the left
    side of the PyPI project page.  This happens whenever you include a newline
    in your project's summary/short description, thereby triggering `setuptools
    bug #1390`__.  Always make sure that no newlines end up passed to the
    ``description`` argument of ``setup()``!

    __ https://github.com/pypa/setuptools/issues/1390

There are two things you can do to avoid uploading a project with a malformed
description to PyPI:

.. _set content-type:

- Set your description's ``Content-Type`` appropriately.  If you're using
  reStructuredText, this will cause PyPI to reject any uploads with malformed
  project descriptions.  If you're not using reStructuredText, setting the
  ``Content-Type`` is necessary in order for your description to be rendered
  properly.

  The content types for the supported formats are as follows:

  :reStructuredText: ``text/x-rst``
  :Markdown (GitHub Flavored Markdown):
    ``text/markdown`` or ``text/markdown; variant=GFM``
  :Markdown (CommonMark): ``text/markdown; variant=CommonMark``
  :Plain text: ``text/plain``

  If your project is built using setuptools, you set the description's
  ``Content-Type`` by setting the ``long_description_content_type`` argument to
  ``setup()`` to the appropriate value from the above table.  Note that this
  requires setuptools 36.4.0 or higher in order to work (or 38.3.0 or higher if
  you're setting it in ``setup.cfg``).

- Run the ``twine check`` command from twine_ on your sdist and wheel before
  uploading them.  This command checks whether your project description can be
  rendered on PyPI before you actually upload it.

  .. _twine: https://twine.readthedocs.io


Project Description Not Included
================================

It's just embarrassing when this happens.  A project without a long description
just looks completely pointless; how am I supposed to know what it does or how
to use it?  Sadly, too many projects on PyPI lack long descriptions.  Did the
developer not care enough to write even a README?  Did the developer forget to
use the README as the long description or not know they had to?

If your project's got a README — and really, a project that doesn't have one
isn't ready to be released — and it's written in reStructuredText, Markdown, or
plain text (a safe bet), you can (and should) use it as your project's long
description by adding the following or similar to your ``setup.py``:

.. code:: python

    with open("README.extension", encoding="utf-8") as fp:
        long_description = fp.read()

    setup(
        ...
        long_description = long_description,
        ...
    )

If your project isn't in reStructuredText, you'll also need to set
``long_description_content_type`` to the appropriate value in `the table above
<set content-type_>`_ so that the description renders properly on PyPI.


Python Package Not Included in Wheel
====================================

If not having a description is embarrassing, not having any code in your wheel
is crippling.  With a wheel like this, when people install your project, they
get nothing!  That's certainly not what you want, is it?

Possible reasons why this can happen include:

- You're using ``find_packages()`` to autolocate your project's packages, but
  you failed to add an ``__init__.py`` file to the top-level package (and
  possibly also some subpackages).  Solution: Add that ``__init__.py``.

  - If your intention is to leave out the ``__init__.py`` file in order to
    create a namespace package, you'll need to use |find_namespace_packages|_
    instead.

- Your project's code is a single Python module (as opposed to a directory of
  modules) and you're using the ``packages`` argument to ``setup()`` and/or
  ``find_packages()`` in an attempt to declare the module to setuptools.  This
  is wrong.  When your project is a single Python module, instead of the
  ``packages`` argument, you need to use the ``py_modules`` argument.  Set
  ``py_modules`` to a list of strings where each string is the name of a
  top-level Python module *without* the "``.py``" extension.  (Usually, you'll
  just have one module to list here.)  You can't use ``find_packages()`` for
  this.

.. |find_namespace_packages| replace:: ``find_namespace_packages()``
.. _find_namespace_packages:
   https://setuptools.readthedocs.io/en/latest/setuptools.html
   #find-namespace-packages

.. _pkg-test:

If your project includes any tests (which it should), you can implicitly test
that your wheel contains your project code by testing against the installed
version of your project instead of the copy in your repository.  To do this,
``pip``-install your package (ideally in a virtualenv, and not in
development/editable mode!) before running the tests and ensure that the
directory containing the repository copy of your code is not in ``sys.path``
when the tests run.  Tox_ can help with the first part.  The second part
depends in part on your test framework, but you can guarantee your tests aren't
picking up the local copy by switching to a ``src/`` layout (`see above
<src_>`_).  With these two things in place, your tests will be forced to import
your package from ``site-packages``, where it's in a form determined by the
contents of the project's wheel.  If your wheel is missing code and your tests
try to import that code, you'll get an error when the tests run, and you'll
know that you need to fix something.

.. _Tox: https://tox.readthedocs.io


Subpackages Not Included in Wheel
=================================

Sometimes, a project's top-level package directory and the files within get
included in a wheel, but the subdirectories and their contents get left out.
Admittedly, I don't know how common this is, as you can't determine whether a
wheel is missing subpackages just by looking at its contents unless you also
know what's in the project's repository.  However, it's an easy thing to mess
up, and various packaging articles I've read frequently make reference to this
problem, so it can't be that uncommon.

There are two major reasons why one or more of your Python package's
subpackages might be omitted from wheels:

- You're passing a list of packages to the ``packages`` argument to ``setup()``
  and the list fails to include every package & subpackage in your project.  If
  your project's top-level package is named "``foo``" and it contains two
  subdirectories named "``bar``" and "``baz``" that contain (directly or
  indirectly) Python source files, then ``bar`` and ``baz`` are subpackages of
  ``foo``, and they all need to be included in the packages list:

  .. code:: python

      packages=["foo", "foo.bar", "foo.baz"]

  If ``baz`` contains another directory named "``glarch``" that contains more
  Python source files, then :py:`"foo.baz.glarch"` needs to be included in the
  list as well, and so on.

  Note that directories that only contain data files and no Python source files
  do not count as packages and should not be passed to the ``packages``
  argument.  They are instead *package data* directories; `see below <package
  data_>`_ for advice on dealing with them.

  Of course, a simple alternative to listing every package explicitly is to
  just use the |find_packages| function, which brings us to cause #2 …

- You're using ``find_packages()`` to autolocate your project's packages, but
  you failed to add an ``__init__.py`` file to one or more subpackages.
  ``find_packages()`` only counts something as a package if it contains an
  ``__init__.py`` file, so you need to include that file in any subdirectory of
  your Python package that contains Python source files or contains a directory
  that contains Python source files.

.. |find_packages| replace:: ``find_packages()``
.. _find_packages:
   https://setuptools.readthedocs.io/en/latest/setuptools.html
   #using-find-packages

As with omitting the package entirely from the wheel, `proper testing practices
<pkg-test_>`_ can let you know when this happens in advance of a release.


.. _package data:

Package Data Not Included in Wheel
==================================

Sometimes, you want to include non-Python data or resource files inside a
Python package so that they can be used at runtime, but sometimes those files
fail to end up in the final wheel.  Like the omission of subpackages, it's hard
to know just how common this is, but even experienced Python programmers have
made mistakes with package data configurations on occasion.  This also happens
to be yet another situation where `testing the installed version of your code
<pkg-test_>`_ will help you out.

Setuptools provides two ways to specify package data.  The first way is to
configure ``MANIFEST.in`` so that the desired package data files are included
in the sdist and then pass :py:`include_package_data=True` to ``setup()`` so
that all files inside the Python package that are included in the sdist are
also included in the wheel.  Pretty much the only way to make a mistake here is
by not matching all of the files you want with ``MANIFEST.in`` commands;
`consult this reference <a MANIFEST.in file_>`_ if you run into problems.

The second way to specify package data is with the ``package_data`` argument to
``setup()``.  This argument takes a ``dict`` mapping package & subpackage names
to lists of glob patterns defining what package data files to include in sdists
& wheels.  The biggest gotcha with this method is the fact that each glob
pattern is only applied to the corresponding package and not any of its
subpackages.  This means that, with a ``package_data`` like this:

.. code:: python

    package_data={
        "package": ["*.txt"],
    }

``*.txt`` files in ``package`` will be recognized as package data and included
in the sdist & wheel, but ``*.txt`` files in ``package.subpackage`` will not.
To include ``*.txt`` files in ``package.subpackage``, you'll need to either add
a :py:`"package.subpackage": ["*.txt"]` entry to ``package_data`` or else
include all ``*.txt`` files in all packages & subpackages by using the empty
string as a key: :py:`"": ["*.txt"]`.

No matter which method you choose, be sure to exclude ``*.pyc`` files from
consideration as package data; `see the next section <pyc_>`_ for why.

Note that if you combine the two ways to specify package data by setting
:py:`include_package_data=True` while also using ``package_data``, then the
files matched by ``package_data`` will not be included in the sdist unless
they're already included by ``MANIFEST.in``.  Getting this wrong can cause
wheels built from an sdist to lack package data files.

See `"Including Data Files" in the setuptools documentation`__ for more
information.

__ https://setuptools.readthedocs.io/en/latest/setuptools.html
   #including-data-files


.. _pyc:

``*.pyc`` Files Included in Wheel
=================================

When a Python source file is imported into a Python process, a ``*.pyc`` file
containing compiled bytecode is created and (in Python 3) stored in a
``__pycache__/`` directory so that future imports of the same file will be
faster.  These ``*.pyc`` files use a format that is specific to the OS, Python
implementation, and Python version, and so it is pointless to share them.  They
do not belong in wheels (especially considering that pip already generates a
host-appropriate set of ``*.pyc`` files when it installs a wheel), and yet too
often people distribute wheels with ``*.pyc`` files in them.

Probably the most common reason why ``*.pyc`` files end up in wheels is that
the project's ``MANIFEST.in`` file contains "``graft packagename``", "``graft
src``", or a similar line and :py:`include_package_data=True` is passed to
``setup()``.  With this configuration, all files in the Python package
directory when the wheel is built are added to the wheel.  To prevent ``*.pyc``
files from being added, "``global-exclude *.pyc``" or similar needs to be added
to the ``MANIFEST.in``, ideally at the end of the file.

Alternatively, if the project specifies its package data with the
``package_data`` argument, including a ``"*"`` pattern in the ``package_data``
mapping is liable to cause ``*.pyc`` files to be included in the wheel.  They
should be excluded from package data by setting ``exclude_package_data`` to a
``dict`` that maps the appropriate keys to :py:`["*.pyc"]`.


.. _rebuild noclean:

Rebuilding Wheels without Deleting ``build/``
=============================================

You should have noticed when building your project's wheels that, in addition
to creating a ``dist/`` directory containing the output wheel, setuptools also
creates a ``build/`` directory containing a couple directories and a copy of
your code.  This ``build/`` directory is an intermediate stage in the process
of assembling a wheel; you should exclude it from version control and feel free
to delete it at any time.  In fact, it's a good idea to delete it before
running the command to create a wheel, *especially* if you've moved or renamed
any files or directories in your code since the last time you built a wheel.

Consider the following scenario:

- You build a wheel for your project, and you leave the ``build/`` directory
  lying around afterwards.

- You move, rename, and/or delete some files in your Python package, perhaps
  even renaming the package itself.

- You build the wheel again — and when you do so, setuptools copies your new
  package tree into ``build/``.  Files that existed the last time the wheel was
  built overwrite their old copies in ``build/`` successfully, but any old
  paths that have since been removed remain in ``build/``.

- As a result, your wheel ends up containing a mixture of your new and old
  code.  In the case where you renamed your package, the wheel will contain
  both the pre-rename package and the post-rename package next to each other in
  their entirety, so you wheel has double the code with half of it under the
  wrong name.

This is clearly not desirable.  The solution is to always delete the ``build/``
directory before building a wheel, such as by cleaning your repository with
``git clean`` or similar, or by running ``python setup.py clean --all`` [1]_.

An even worse situation occurs if your ``setup.py`` uses
``find_namespace_packages()`` without any arguments.  In this case, if you
rebuild your package without first deleting the ``build/`` directory,
``find_namespace_packages()`` will notice the ``.py`` files in ``build/`` and
assume that ``build/`` is a namespace package, and so it'll include ``build/``
in your wheels — which means that ``build/`` gets copied into ``build/``,
resulting in multiple package hierarchies in your wheels, with the problem
compounding the more times you build your project without deleting the
``build/`` directory.  This particular problem can be mitigated by using the
``where``, ``exclude``, and/or ``include`` arguments to
``find_namespace_packages()``, which have the same meaning as for
``find_packages()``.


Pinning Project Requirements to Exact Versions
==============================================

There are a number of projects on PyPI where the dependencies are all of the
form "``foo == 1.2.3``", as opposed to "``foo >= 1.2.3``", "``foo >= 1.2, <
2``", or just "``foo``".  This is called *pinning* requirements.  This makes
sense when you're developing a Python application that will be the primary
project in its environment (in which case you often won't be uploading it to
PyPI), but it doesn't make sense when you're distributing a library for others
to use alongside other arbitrary libraries.  For one thing, your library is
almost certainly going to work just as well with version 1.2.4 of foo [2]_, so
why leave it out?  For another thing, if someone wants to use your library with
its pinned ``foo`` requirement alongside other libraries, sooner or later
they'll run into a situation where they're installing both it and another
project that requires a different version of ``foo`` (maybe even differing by
one micro version!), and then problems ensue [3]_.  True, clashes between
version dependencies in disparate projects can't be avoided 100%, but they can
be made to occur far less often if projects require generous version ranges
instead of specific versions.

A general way to construct a decent version range for a requirement is to first
determine the lowest version of the dependency that has all of the features you
need and then use this version as the requirement's lower bound.  If the
dependency follows or approximates `semantic versioning <https://semver.org>`_,
use the next major version (or the next minor version, if pre-v1) as the
(exclusive) upper bound.  If the dependency uses something like calendar
versioning instead, things are less clear, but my preference is to leave out
the upper bound and afterwards keep abreast of any future changes to the
dependency.  If any versions of the dependency inside the requirement's bounds
have known bugs that interfere with your project's behavior, feel free to
exclude them by adding specifiers of the form ``!= X.Y.Z`` to the version
range.


Conclusion
==========

I'm very disappointed in all of you for making these mistakes so often, and I
hope this article makes at least one Python package less broken.  (I'd prefer
it if all broken packages were less broken, but I know not to get my hopes up.)

Admittedly, most of these mistakes are due to users not using or understanding
setuptools properly (aside from a Poetry anti-pattern that sneaked in at #2).
Though flit and Poetry may promise to fix setuptools' usability issues, people
keep on using setuptools, and it keeps on outsmarting them.  Hopefully sites
like the `Python Packaging User Guide`_ eventually expand & become mature
enough in the near future to cover — if not all the edge cases — at least the
best practices that avoid them.

.. _Python Packaging User Guide: https://packaging.python.org


Footnotes
=========

.. [1] Setuptools is currently trying to get people to move away from
       ``setup.py`` commands, so ``setup.py clean`` will be discouraged — and
       probably deprecated — at some indeterminate point in the future.  Until
       that happens, though, don't feel bad about using it if you need to.

.. [2] Unless ``foo`` is an unpredictable, compatibility-breaking mess, in
       which case you should probably reconsider depending on it.

.. [3] Currently, pip handles conflicting version requirements with a warning
       and picking one requirement to follow, but pip's new dependency resolver
       due out in October 2020 (already available if you pass the right flag to
       pip) will react to such situations by searching for older versions of
       the installation candidates with non-conflicting requirements, and if it
       can't find any, it errors out without installing anything.
