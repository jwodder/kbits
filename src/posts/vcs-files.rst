=================
Special VCS Files
=================

:Date: 2021-06-22
:Category: Software
:Tags: Git, VCS, dotfiles
:Summary:
    A list of VCS-specific files that one may find in the working directories
    of common version control systems

The following is a list of VCS-specific files that one may find in the working
directories of common version control systems.  This list is useful for, say,
knowing what files to ignore when traversing a project directory.

Did I leave anything out?  `Feel free to send a pull request.`__

__ https://github.com/jwodder/kbits

.. table::
    :align: center
    :widths: auto

    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | VCS          | File/Directory     | Purpose                                              | Documentation              |
    +==============+====================+======================================================+============================+
    | Git_         | ``.git/``          | Repository data                                      | `gitrepository-layout(5)`_ |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.gitattributes`` | Defines per-path attributes                          | `gitattributes(5)`_        |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.gitignore``     | Lists files to exclude from version control          | `gitignore(5)`_            |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.gitmodules``    | Defines submodules                                   | `gitmodules(5)`_           |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.mailmap``       | Maps names & e-mails to canonical values             | `gitmailmap(5)`_           |
    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | Mercurial_   | ``.hg/``           | Repository data                                      | `wiki:FileFormats`_        |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.hgignore``      | Lists files to exclude from version control          | `hgignore(5)`_             |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.hgsigs``        | Contains changeset signatures from the GPG extension | —                          |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.hgtags``        | Defines tags                                         | —                          |
    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | Darcs_       | ``_darcs/``        | Repository data                                      | —                          |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.binaries``      | Lists files to treat as binary [#fn1]_               | `Manual <binaries>`_       |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.boring``        | Lists files to exclude from version control [#fn1]_  | `Manual <boring_>`_        |
    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | Bazaar_      | ``.bzr/``          | Repository data                                      | —                          |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``.bzrignore``     | Lists files to exclude from version control          | `bzr ignore`_              |
    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | Subversion_  | ``.svn/`` or       | Local copy of repository data [#fn3]_                |                            |
    |              | ``_svn/`` [#fn2]_  |                                                      |                            |
    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | CVS_         | ``CVS/``           | Local copy of repository data (one per directory)    | `Manual <CVS-dir_>`_       |
    +--------------+--------------------+------------------------------------------------------+----------------------------+
    | RCS_         | *filename*\ ``,v`` | Verson history for *filename*                        | `Manual <comma-v_>`_       |
    |              +--------------------+------------------------------------------------------+----------------------------+
    |              | ``RCS/``           | Conventional directory for storing ``*,v`` files     | —                          |
    +--------------+--------------------+------------------------------------------------------+----------------------------+

.. _Git: https://git-scm.com
.. _gitrepository-layout(5): https://git-scm.com/docs/gitrepository-layout
.. _gitattributes(5): https://git-scm.com/docs/gitattributes
.. _gitignore(5): https://git-scm.com/docs/gitignore
.. _gitmodules(5): https://git-scm.com/docs/gitmodules
.. _gitmailmap(5): https://git-scm.com/docs/gitmailmap

.. _Mercurial: https://www.mercurial-scm.org
.. _hgignore(5): https://www.selenic.com/mercurial/hgignore.5.html
.. _wiki:FileFormats: https://www.mercurial-scm.org/wiki/FileFormats

.. _Darcs: http://darcs.net
.. _binaries: http://darcs.net/manual/Configuring_darcs.html#SECTION00410050000000000000
.. _boring: http://darcs.net/manual/Configuring_darcs.html#SECTION00410040000000000000

.. _Bazaar: https://bazaar.canonical.com
.. _bzr ignore: http://doc.bazaar.canonical.com/bzr.2.7/en/user-reference/ignore-help.html

.. _Subversion: http://subversion.apache.org

.. _CVS: http://cvs.nongnu.org
.. _CVS-dir: https://www.gnu.org/software/trans-coord/manual/cvs/html_node/Working-directory-storage.html

.. _RCS: https://www.gnu.org/software/rcs/
.. _comma-v: https://www.gnu.org/software/rcs/manual/html_node/Concepts.html#RCS-file


.. [#fn1] Darcs normally stores its binaries file and boring file inside the
   ``_darcs/`` directory, but it is possible to use any file under version
   control in their place; the names listed here are the conventional names for
   such files.

.. [#fn2] For compability with ASP.NET, Subversion will use the name ``_svn``
   instead of ``.svn`` if the ``SVN_ASP_DOT_NET_HACK`` environment variable is
   defined.

.. [#fn3] Prior to version 1.7, Subversion placed a ``.svn``/``_svn`` directory
   in every subdirectory of the working directory under version control.


.. vim: set nowrap:
