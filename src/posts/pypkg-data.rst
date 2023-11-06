=====================================================
Using Package Data in Python Projects with Setuptools
=====================================================

:Date: 2020-12-29
:Modified: 2022-06-10
:Category: Programming
:Tags: Python, Python packaging, setuptools
:Summary:
    When creating a Python project, you may want to include a number of
    non-Python files in the project that the code can then access at runtime,
    such as templates, images, and data.  These files are called *package
    data*, and this article describes how to include them in & access them from
    your project.

When creating a Python project, you may want to include a number of non-Python
files in the project that the code can then access at runtime, such as
templates, images, and data.  These files are called *package data* [#f1]_, and
they are included in & accessed from your project as follows.

.. contents::

Including Package Data in Projects
==================================

.. note::

    The following section only pertains to projects built with setuptools.
    Users of flit, Poetry, and other tools must consult their respective
    backend's documentation to see how to include package data.

The first requirement for being able to include package data in your package_
[#f2]_ is for the files to be located somewhere inside the actual package
directory.  If your project is a single-file ``.py`` module, you must convert
it to a directory/package layout before you can store package data in it.

.. _package: https://docs.python.org/3/tutorial/modules.html#packages

Once your package data is inside the package, you must tell setuptools to
include the files in both the project's wheel (so that the files will be
installed when your package is installed) and sdist (so that the files can be
included in the wheel when building from an sdist).  There are two different
major ways to do this: a blanket "include all" method that uses a
``MANIFEST.in`` file and a fine-grained method that configures one package &
subpackage at time via the ``setup.py``/``setup.cfg`` file.

.. important::

    In addition to the configurations described here, you also need to ensure
    that all folders within your package that contain package data (even if
    they contain no Python source code) are listed in the ``packages`` option
    in ``setup.py``/``setup.cfg``.  This can be done automatically by using the
    ``setuptools.find_namespace_packages()`` function instead of
    ``find_packages()``.  If you don't do this, setuptools will emit a
    warning message starting in version 62.3.0, and later versions will cease
    to include such packages in your distribution at all.


Including Package Data via ``MANIFEST.in``
------------------------------------------

There are two steps to this method:

1. Create or edit your project's ``MANIFEST.in`` file with the proper commands
   to tell setuptools to include all of your package data file in the project's
   sdists.  See `the Python Packaging User Guide`__ for information on how to
   do this.

   __ https://packaging.python.org/guides/using-manifest-in/

   In the simplest case — in which you want all non-Python files in your
   package to be treated as package data — you can simply include your entire
   package in your sdist with the ``MANIFEST.in`` command "``graft
   packagename``" (or "``graft src``" if you're using a |src/ layout|_).  If
   you use this command, you should also follow it with "``global-exclude
   *.py[cod]``" so that compiled Python bytecode files are not included in the
   sdist.

   .. |src/ layout| replace:: ``src/`` layout
   .. _src/ layout: https://hynek.me/articles/testing-packaging/

2. In your ``setup.py``, pass ``include_package_data=True`` to the ``setup()``
   function.   If you are placing your project configuration in ``setup.cfg``
   instead, set ``include_package_data = True`` in the ``[options]`` section of
   ``setup.cfg``.

   Doing this tells setuptools that any non-Python files found inside your
   package that are included in the sdist should also be included in the wheel.


Including Package Data via ``setup.py``/``setup.cfg``
-----------------------------------------------------

This method allows you to specify package data file patterns on a per-package
basis through the ``package_data`` argument to ``setup()``.  ``package_data``
must be a ``dict`` mapping package or subpackage names (or the empty string, to
specify all packages & subpackages) to lists of glob patterns indicating which
files within those packages to include in the sdist and wheel.

A sample ``package_data`` looks like this:

.. code:: python

    package_data={
        # If any package or subpackage contains *.txt or *.rst files, include
        # them:
        "": ["*.txt", "*.rst"],
        # Include any *.msg files found in the "hello" package (but not in its
        # subpackages):
        "hello": ["*.msg"],
        # Include any *.csv files found in the "hello.utils" package:
        "hello.utils": ["*.csv"],
        # Include any *.dat files found in the "data" subdirectory of the
        # "mypkg" package:
        "mypkg": ["data/*.dat"],
    }

If you are placing your project configuration in ``setup.cfg``, you must
instead specify ``package_data`` via an ``[options.package_data]`` section in
which the keys are the package & subpackage names — using ``*`` instead of the
empty string to signify all packages — and the values are comma-separated glob
patterns.  The above ``setup.py`` sample translates to ``setup.cfg`` as
follows:

.. code:: ini

    [options.package_data]
    # If any package or subpackage contains *.txt or *.rst files, include them:
    * = *.txt, *.rst
    # Include any *.msg files found in the "hello" package (but not in its
    # subpackages):
    hello = *.msg
    # Include any *.csv files found in the "hello.utils" package:
    hello.utils = *.csv
    # Include any *.dat files found in the "data" subdirectory of the "mypkg"
    # package:
    mypkg = data/*.dat

Note that glob patterns only select files located directly within the given
package (or in the given subdirectory of the package, if the pattern includes a
directory path); e.g., ``"hello": ["*.msg"]`` selects ``*.msg`` files in the
``hello`` package but not in any of its subpackages.  To select files in
subpackages, you must either include an entry for each subpackage or else use
the empty string key (or asterisk key in ``setup.cfg``) to specify a pattern
for all packages & subpackages.

If a pattern contains any directory components, the forward slash (``/``) must
be used as the directory separator, even on Windows.

If a package data file is located in a directory that does not have an
``__init__.py`` file (say, a ``data/`` directory inside
``package.subpackage``), that directory does not count as a package, and the
file must be listed in ``package_data`` in the form ``"package.subpackage":
["data/PATTERN"]``.

.. warning::

    If you use both ``include_package_data`` and ``package_data``, files
    specified with ``package_data`` will not be automatically included in
    sdists; you must instead list them in your ``MANIFEST.in``.


Excluding Package Data via ``setup.py``/``setup.cfg``
-----------------------------------------------------

The ``exclude_package_data`` argument to ``setup()`` can be used in conjunction
with either of the above methods to prevent one or more files from being
treated as package data.  ``exclude_package_data`` takes a ``dict`` with the
same structure as ``package_data``, and any matched files are excluded from
wheels.  Matched files are also excluded from sdists if they are not already
matched by the project's ``MANIFEST.in``.

In a ``setup.cfg``, ``exclude_package_data`` becomes an
``[options.exclude_package_data]`` section whose contents have the same
structure as ``[options.package_data]``.


Including Package Data via Setuptools Plugins
---------------------------------------------

As an alternative to the above methods, you can use a plugin for setuptools
that automatically recognizes & includes package data in sdists & wheels,
usually based on what files in the project directory are under version control.
One example of such a plugin is setuptools_scm_, which automatically finds all
files under version control in a Git or Mercurial repository and augments the
project's ``MANIFEST.in`` (if any) with the found files.  This eliminates the
need to write a ``MANIFEST.in`` manually (unless there are files under version
control that you want to exclude from sdists or wheels), though you still need
to set ``include_package_data`` to ``True`` for files in your package directory
to be included in wheels.

.. _setuptools_scm: https://github.com/pypa/setuptools_scm


Accessing Package Data at Runtime
=================================

There have been multiple ways to access package data over the years, from
|pkg_resources' ResourceManager API|__ to |pkgutil.get_data|_, but the most
recent and currently-recommended way is with the `importlib-resources`__
package.

.. |pkg_resources' ResourceManager API| replace:: ``pkg_resources``' ``ResourceManager`` API
__ https://setuptools.readthedocs.io/en/latest/pkg_resources.html#resourcemanager-api

.. |pkgutil.get_data| replace:: ``pkgutil.get_data()``
.. _pkgutil.get_data:
   https://docs.python.org/3/library/pkgutil.html#pkgutil.get_data

__ http://importlib-resources.readthedocs.io


Installing & Importing ``importlib-resources``
----------------------------------------------

There are two versions of ``importlib-resources`` available:

- `The one on PyPI`__ that is installed with ``pip install
  importlib-resources`` and imported with ``import importlib_resources`` (note
  underscore)

  __ https://pypi.org/project/importlib-resources/

- `The one in the Python standard library`__ starting with Python 3.7 that is
  imported with ``import importlib.resources`` (note period)

  __ https://docs.python.org/3/library/importlib.html
     #module-importlib.resources

Development of the PyPI version tends to be ahead of whatever's in the latest
Python version.  In particular, the new ``files()``-based API described here
was only introduced in version 1.1.0 of the PyPI project and was only added to
the Python standard library in Python 3.9.  In order to be guaranteed a version
of ``importlib-resources`` that supports this API, you should add the following
to your project's ``install_requires``::

    importlib-resources>=1.1.0; python_version < '3.9'

and import ``importlib-resources`` in your code as follows:

.. code:: python

    import sys

    if sys.version_info < (3, 9):
        # importlib.resources either doesn't exist or lacks the files()
        # function, so use the PyPI version:
        import importlib_resources
    else:
        # importlib.resources has files(), so use that:
        import importlib.resources as importlib_resources


The ``importlib-resources`` API
-------------------------------

To access a package data file in your project, start by calling
``importlib_resources.files()`` on the name of your package:

.. code:: python

    pkg = importlib_resources.files("packagename")
    # The argument can optionally refer to a subpackage in the form
    # "packagename.subpackage".

This gives you a Traversable_ object that acts like a limited ``pathlib.Path``
object for traversing package data files.  To refer to a ``data.csv`` file in a
``data/`` directory in your package, write:

.. _Traversable: https://github.com/python/importlib_resources/blob/
                 eb0554035b499e4a5349dcc56a2bda51835f4fde/importlib_resources/
                 abc.py#L61

.. code:: python

    pkg_data_file = pkg / "data" / "data.csv"

So now that we've got a reference to the package data file, how do we get
anything out of it?

- To open the file for reading, call the ``open()`` method:

  .. code:: python

    with pkg_data_file.open() as fp:
        # Do things with fp

- To get the file's contents as ``bytes``, call the ``read_bytes()`` method:

  .. code:: python

    b = pkg_data_file.read_bytes()

- To get the file's contents as a ``str``, call the ``read_text()`` method,
  optionally with an ``encoding`` argument:

  .. code:: python

    s = pkg_data_file.read_text(encoding="utf-8")

- To get the path to the file, call ``importlib_resources.as_file()`` on it and
  use the return value as a context manager:

  .. code:: python

    with importlib_resources.as_file(pkg_data_file) as path:
        # Do things with the pathlib.Path object that is `path`

  The use of context managers allows ``importlib-resources`` to support
  packages stored in zipfiles; when a path is requested for a package data file
  in a zipfile, the library can extract the file to a temporary location at the
  start of the ``with`` block and remove it at the end of the block.

- To iterate through a directory (either a package or a non-package directory),
  use the ``iterdir()`` method.  You can test whether a resource is a directory
  or a file with the ``is_dir()`` and ``is_file()`` methods, and you can get a
  resource's basename via the ``name`` property:

  .. code:: python

    for entry in (pkg / "data").iterdir():
        if entry.is_dir():
            print(entry.name, "DIR")
        else:
            print(entry.name, "FILE")


Footnotes
=========

.. [#f1] Specifically, package data files are files that are stored in a Python
         project's package directory next to the Python source files.  An
         alternative to package data is *data files*, which are files installed
         elsewhere on the file system.  This article only deals with the
         former.

.. [#f2] Throughout this article, the term "package" is used in the sense of a
         directory of ``.py`` files and other packages (a.k.a. an "`import
         package`_"), not in the sense of a "`distribution package`_" (i.e., an
         sdist or wheel).

.. _import package: https://packaging.python.org/glossary/#term-Import-Package
.. _distribution package:
   https://packaging.python.org/glossary/#term-Distribution-Package
