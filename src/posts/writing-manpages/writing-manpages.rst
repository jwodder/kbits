================================
Basics of Writing Unix Man Pages
================================

:Date: 2022-11-24
:Category: Software
:Tags: documentation, groff, roff, markup, man pages, Unix utilities
:Summary: A guide to the basic syntax & commands of Unix man pages

On Unix-like systems, the documents that one views with the ``man`` command
(known as "man pages") are written in a markup language called "roff" (short
for "run off") that dates back to the pre-Unix days in the 1960's.  roff is
technically a full-blown programming language with numerous features, but you
only need to know a very small subset in order to produce most man pages.  This
article will describe that subset so that you can go on to write man pages for
your own software.

Man pages, like most roff documents, use a roff *macro package* that defines a
set of high-level commands.  The macro package used by most man pages is,
unsurprisingly, the ``man`` package, and that is what is covered here.  Some
man pages instead use the ``mdoc`` package, which originated in BSD.  Modern
versions of the ``man`` command use the ``mandoc`` package for processing man
pages, which autodetects whether a file is written using ``man`` or ``mdoc``
and processes it accordingly.

.. contents::


roff Syntax
===========

A roff file is composed of a mixture of *control lines* — lines that start with
a *control character*, usually a period or single-quote — and *text lines* —
lines that do not.

Control lines are commands to roff (also known as *requests*).  They consist of
a control character & a command name followed by some number of space-separated
(not tab-separated!) arguments.  To include spaces in an argument, either
escape them with a backslash or enclose the entire argument in double-quotes;
to use double-quotes inside an argument, write them as ``\(dq``.

- There may be any number of spaces & tabs (or none at all) between the control
  character and the command name, but the control character must be the first
  character in the line.

- A line with just a period is ignored.

Text lines give the text that will be displayed.  They can contain *escape
sequences*, inline commands that start with backslashes.

- Whitespace around escape sequences is significant and is not discarded.  The
  syntax of an escape sequence allows roff to automatically determine where it
  ends; for example, escape sequences starting with ``\(`` are always followed
  by two more characters to complete the sequence, and so an escape sequence
  like ``\(em`` (em-dash) can be embedded in the middle of a word:
  ``foo\(embar`` becomes "foo—bar".

- To start a text line with a period, precede the period with either a
  backslash or the escape sequence ``\&``.

- To render a literal backslash in text, use the escape sequence ``\\``,
  ``\e``, or ``\(rs``.

A comment consists of a backslash and double quote (``\"``) and extends to the
end of the line.  A full-line comment can be formed by using the command
``.\"``.

A single logical line can be broken across multiple physical lines by placing a
backslash at the end of each physical line.


Document Structure Commands
===========================

``.TH title section [footer-middle] [footer-outside] [header-middle]``
    This must be the first non-comment command in a man page, and it must appear
    exactly once.  It sets the page title (which is conventionally in all-caps)
    and section number for the man page (see "`Manual Sections`_" below) to the
    given values, to be displayed in the form ``title(section)`` at the left &
    right sides of the header of the rendered manual page.

    The remaining three arguments are optional.  To omit an argument but still
    be able to specify an argument after it, write ``\&`` in place of the
    omitted argument.

    - If ``footer-middle`` is given, it will be rendered in the middle of the
      footer.  This argument is usually set to the date the man page was
      written.

    - If ``footer-outside`` is given, it will be rendered on the left side of
      the footer.  This is usually set to the version of the software being
      documented.

    - If ``header-middle`` is given, it will be rendered in the middle of the
      header.  If it is omitted and ``section`` is a number from 1 to 9,
      certain versions of ``man`` will supply a default value.

``.SH [name]``
    Start a section with the given name.  If no argument is given, the next
    line will be used as the name.

``.SS [name]``
    Start a subsection with the given name.  If no argument is given, the next
    line will be used as the name.

``.LP`` or ``.PP`` or ``.P``
    Paragraph break, resetting any indentation caused by the ``.TP``, ``.IP``,
    or ``.HP`` command

``.TP [n]``
    Start a labelled, indented paragraph.  The next text line after this
    command is the paragraph label, and any following text lines up to the next
    ``.PP`` will be indented.  If a numeric argument is given, the paragraph
    will be indented by that many columns.

``.IP [text] [n]``
    Start an indented paragraph.  The text argument, if given, will be used as
    the paragraph's bullet/"tag"; this is usually the bullet escape sequence
    (``\(bu``), the em-dash escape sequence (``\(em``), or a number followed by
    a period.  If no text argument is supplied, no bullet will be present, but
    the following paragraph will still be indented; this can be used to start a
    new indented paragraph after an initial indented paragraph created by
    ``.TP``, ``.IP``, or ``.HP``.

    If a numeric second argument is given, the paragraph will be indented by
    that many columns.

``.HP [n]``
    Start an indented paragraph in which the first line is not indented.  If a
    numeric second argument is given, the paragraph will be indented by that
    many columns.

``.RS [n]``
    Increase the amount of indentation until a corresponding ``.RE``.  If a
    numeric second argument is given, the indentation will be increased by that
    many columns.

``.RE``
    Undo the increase in indentation caused by the last ``.RS``

``.br``
    Insert a line break

``.sp``
    Skip a line

``.sp N``
    Skip ``N`` lines


Font Commands
=============

The following escape sequences can be used to change the font within a text
line:

``\fB``
    Change the font to bold

``\fI``
    Change the font to italic (on a terminal, underlined)

``\fR``
    Change the font to roman

``\fP``
    Change back to the previous font

The following requests render an argument in a given font:

``.B [text]``
    Renders the given text (or the text of the next line if no argument is
    given) in bold with a word break before & after.

``.I [text]``
    Renders the given text (or the text of the next line if no argument is
    given) in italic (on a terminal, underlined) with a word break before &
    after.

The following commands take multiple arguments and render them in alternating
fonts.  A word break/whitespace will be inserted before & after the arguments,
but there will be no words breaks/whitespace inserted between the arguments.
For example, the following:

.. code:: groff

    This is
    .BI very styled
    text.

will render as:

    This is **very**\ *styled* text.

``.RB text ...``
    Renders the given arguments in alternating roman and bold, roman first.

``.BR text ...``
    Renders the given arguments in alternating bold and roman, bold first.

``.RI text ...``
    Renders the given arguments in alternating roman and italic/underlined,
    roman first.

``.IR text ...``
    Renders the given arguments in alternating italic/underlined and roman,
    italic/underlined first.

``.BI text ...``
    Renders the given arguments in alternating bold and italic/underlined, bold
    first.

``.IB text ...``
    Renders the given arguments in alternating italic/underlined and bold,
    italic/underlined first.

.. tip::

    While modern groff lets you use these commands with any number of
    arguments, traditional implementations limit usage to six arguments; keep
    this in mind if you want to make your man page portable.


Additional Escape Sequences
===========================

Select Non-ASCII Characters
---------------------------

See |grof_char|_ for the complete set of available character escape sequences.

.. |grof_char| replace:: ``grof_char(7)``
.. _grof_char: https://man7.org/linux/man-pages/man7/groff_char.7.html

=========  ============================
Escape     Character
=========  ============================
``\(bu``   bullet (•)
``\*R``    registration symbol (®)
``\*(Tm``  trademark symbol (™)
``\(co``   copyright (©)
``\(em``   em-dash (—)
``\(en``   en-dash (–)
``\(rq``   right double-quote (“)
``\(lq``   left double-quote (”)
``\(oq``   left single-quote (‘)
``\(cq``   right single-quote (’)
=========  ============================

.. note::

    When viewing a man page in the terminal, not all installations will display
    Unicode characters.  On systems that display man pages in ASCII (which
    include macOS as of Big Sur), non-ASCII characters will be rendered as the
    visually closest ASCII character where possible.

Special ASCII Characters
------------------------

Some output devices transform certain ASCII input characters to similar Unicode
characters, so the following escape sequences can be used to ensure that the
desired ASCII character appears in the rendered man page:

========  ============================
Escape    Character
========  ============================
``\(aq``  Apostrophe (')
``\(ga``  Grave accent (`)
``\(ha``  Caret/circumflex accent (^)
``\(ti``  Tilde (~)
``\-``    Hyphen/minus (-)
========  ============================

Other
-----

- A backslash followed by a space produces a non-breaking space that remains at
  a fixed width when text is justified.

- ``\~`` produces a non-breaking space that nevertheless stretches like a
  normal inter-word space when justifying text.

- ``\&`` produces a non-printable, zero-width character.  It can be placed next
  to a token to deprive it of any special meaning; for example, it can be
  placed after a period at the end of an abbreviation to prevent it from being
  treated as the end of a sentence.


Man Page Conventions
====================

Manual Sections
---------------

Each man page is traditionally placed into one of nine manual *sections* (not
to be confused with the sections within a man page created by the ``.SH``
command; for that, see below).  The pages for a given section are stored
together, and the section number is also used as the file extension.  The
sections are:

1. Commands for use by general users
2. C system calls
3. C library functions, libraries, & headers
4. Devices, special files, and sockets
5. File formats
6. Games
7. Miscellaneous
8. Commands for use by system administrators (including servers/daemons)
9. C kernel functions

Sections of a Man Page
----------------------

The contents of a man page are divided into sections by the ``.SH`` command.
Different sources give slightly different lists of the "standard" sections, but
the most common, in roughly the order they should appear in a man page, are:

``NAME``
    Gives the name of the man page and a short description of what it
    documents.  This is usually considered the only mandatory section.

    In order for a man page named "foobar" to be properly indexed by ``whatis``
    and ``apropos``, ``NAME`` must be the first section in the man page, and
    the ``.SH NAME`` line must be followed immediately by a line of the form
    ``foobar \- short description of foobar``.

``SYNOPSIS``
    Shows the syntax for invoking a command or calling a C function.

    The synopsis for a command usually follows the following conventions:

    - Text that should be entered as-is by the user (e.g., options and the name
      of the command) should be in **bold**, while placeholder text that should
      be replaced with some value by the user (e.g., command arguments) should
      be in *italics/underlined*.

    - Optional syntax elements (e.g., most options) should be enclosed in
      square brackets.

    - Alternative forms of a syntax element (e.g., the short and long form of
      an option) should be separated by whitespace and a vertical bar.

    - Syntax elements that can be repeated (e.g., arguments that can be given
      multiple times) are indicated by appending three periods (``...``).

    See `A Sample Man Page`_ below for an example of these rules in action.

``DESCRIPTION``
    An explanation of what the command, function, etc. does

``OPTIONS``
    A list of any command-line options a program takes and their meanings.
    This list is usually created using ``.TP`` or ``.IP`` to produce paragraphs
    labeled with the option they describe, with each option in **bold** and any
    argument it may take in *italics/underlined*.

``EXIT STATUS``
    A list of the possible exit statuses for a command and their meanings

``ENVIRONMENT``
    A description of any environment variables that affect the command or
    function

``FILES``
    A description of any files the command uses (configuration files, startup
    files, etc.).  It is recommended that file paths be styled in
    *italics/underlined*.

``NOTES``
    Any miscellaneous notes

``BUGS``
    A list of known shortcomings in the documented software or functionality

``EXAMPLES``
    Examples of how to use the software or functionality

``AUTHORS``
    A list of the authors of the software and/or man page

``REPORTING BUGS``
    Information on how to report any bugs found in the software

``COPYRIGHT``
    Copyright/license details

``SEE ALSO``
    A comma-separated list of related man pages and/or other documents.
    References to other man pages should be formatted with the name in bold and
    the section number in roman enclosed in parentheses.


Other Conventions
-----------------

- Use ``\-`` instead of plain ``-`` for ASCII hyphens, e.g., in command-line
  options.  Use plain ``-`` in hyphenated words.

- Blank lines are discouraged, as they may not render correctly in all output
  formats.  Use the ``.sp`` command instead to produce a blank line, or use
  ``.PP`` to start a new paragraph.

- Each sentence should typically start on a new line.

- Use only a single space between words in text; multiple spaces will not be
  collapsed into one when rendering.


Rendering a Man Page
====================

To render a man page in the terminal the way that ``man`` would, run ``man -l
path/to/man/page``.  (On macOS, you have to instead run ``mandoc -a
path/to/man/page``).  You may also want to pass the ``--warnings`` option
(``-Wall`` for ``mandoc``) in order to catch any problematic syntax.

If your version of ``man`` does not support the ``-l`` option, you can instead
run ``groff`` (GNU roff, the typical roff implementation on nearly all Unix
machines nowadays) directly with ``groff -man -Tutf8 path/to/man/page | less
-is``.

Of course, groff can render to more than just terminals by changing the value
passed to the ``-T`` option in the ``groff`` command.  Values of interest
include ``pdf``, ``ps`` (for PostScript), and ``html``; these require the
``gropdf``, ``grops``, and ``grohtml`` commands, respectively, to be installed
in order to work.


A Sample Man Page
=================

.. include:: foobar.1
    :code: groff

[`Download this file <{attach}foobar.1>`_]

Rendered:

.. raw:: html

    <script id="asciicast-LtGNGNNqtSYDLi72H6e8Yp1sQ" src="https://asciinema.org/a/LtGNGNNqtSYDLi72H6e8Yp1sQ.js" async data-autoplay="true" data-loop="true"></script>

Further References
==================

- ``groff(7)`` man page: <https://man7.org/linux/man-pages/man7/groff.7.html>
- ``groff_char(7)`` man page: <https://man7.org/linux/man-pages/man7/groff_char.7.html>
- ``groff_man(7)`` man page: <https://man7.org/linux/man-pages/man7/groff_man.7.html>
- ``man-pages(7)`` man page: <https://man7.org/linux/man-pages/man7/man-pages.7.html>
