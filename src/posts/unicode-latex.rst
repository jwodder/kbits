=================
Unicode and LaTeX
=================

:Date: 2020-07-27
:Category: Software
:Tags: markup, LaTeX, XeLaTeX, LuaLaTeX, Unicode, UTF-8, encoding
:Summary:
    How to configure LaTeX to accept UTF-8 input (or just use XeLaTeX/LuaLaTeX
    instead)

.. role:: tx(code)
    :language: tex

LaTeX is a powerful document typesetting system, but (especially if you're
using a version even a few years old), getting it to accept and display
non-ASCII characters natively requires knowledge squirreled away in scattered
documents.  Here we cover how to get LaTeX to work with UTF-8 input characters
in hopes of thwarting the squirrels of obscurity.

Or you could just `skip all that <xetex and luatex_>`_ and use XeLaTeX or
LuaLaTeX instead.


pdfTeX Engine (pdfLaTeX)
========================

When using "basic" LaTeX with the pdfTeX engine, enabling UTF-8 input requires
simply placing the following commands at the top of your document preamble:

.. code:: latex

    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}

The exact effects of these commands are as follows:

- :tx:`\usepackage[T1]{fontenc}` sets the output font encoding to T1_.  A font
  encoding is a mapping between character codes and glyphs in a font; the font
  encodings defined by LaTeX are described in [#encguide]_.

  By default, LaTeX uses the OT1_ font encoding, a 7-bit encoding in which
  accented characters like "ö" are formed by adding an accent glyph to the base
  letter.  T1, by contrast, is an 8-bit encoding supporting widespread European
  languages in which many letter+accent combinations exist as single glyphs.
  [#fontenc-vs-inputenc]_ [#use-fontenc]_

  Without this command, characters will be represented using what's available
  in OT1, and, as a result, words containing accented characters won't be
  correctly hyphenated, copying-and-pasting accented characters from a built
  PDF won't work correctly, and inputting a ``|``, ``<``, or ``>`` will produce
  a completely different character in the resulting PDF. [#use-fontenc]_

  If one passes a comma-separated list of font encodings to the ``fontenc``
  package, the last encoding in the list becomes the document's default
  encoding, and switching to the other encodings (e.g., in order to enter
  characters only defined by those encodings) becomes possible using the
  command sequence :tx:`\fontencoding{INSERT ENCODING NAME HERE} \selectfont`.
  [#source2e]_ [#minimal]_ [#latex2e-unoff]_

  .. _T1: http://www.micropress-inc.com/fonts/encoding/t1.htm
  .. _OT1: http://www.micropress-inc.com/fonts/encoding/ot1.htm

- :tx:`\usepackage[utf8]{inputenc}` sets the input encoding for the document
  source to UTF-8, allowing UTF-8 characters to appear in the input document.
  Additionally, for each font encoding used in the document, ``inputenc`` loads
  a mapping of UTF-8 characters to commands usable in that font encoding.
  [#inputenc]_  When paired with the ``fontenc`` command above, on recent LaTeX
  versions, ``inputenc`` loads mappings from the files ``omsenc.dfu``,
  ``ot1enc.dfu``, ``t1enc.dfu``, and ``ts1enc.dfu`` [#minimal]_, located in
  ``$TEXDIR/texmf-dist/tex/latex/base`` in an installed TeX Live distribution;
  this in turn allows the user to input any of the characters mapped by those
  files into a document and have the characters be typeset appropriately.

  Without this command, older versions of LaTeX will use a "raw" input encoding
  in which each input byte is typeset as the glyph in the same position in the
  current font. [#ltnews28]_
  
  Beginning with the 2018-04-01 release, LaTeX uses UTF-8 as the default
  encoding for source files, making :tx:`\usepackage[utf8]{inputenc}`
  redundant. [#ltnews28]_

Once the above commands are added to your document preamble, you will be able
to enter a number of UTF-8 characters directly into your document and have them
show up in the built PDF without having to type out their commands.  You'll
even be able to write smart quotes (``“`` and ``”``) directly instead of typing
quotes out as \`\` and ``''``.

So instead of writing this:

.. code:: latex

    ``My na\"\i{}ve r\'esum\'e is attached.''  --- Se\~nor \TH{}or

you can write this:

.. code:: latex

    “My naïve résumé is attached.”  — Señor Þor

and LaTeX will handle the input correctly.

Note that LaTeX does not support combining characters; input must be in a
composed form.

If LaTeX encounters a Unicode character that it doesn't have a definition for,
typesetting will stop with an error message of the form::

    ! Package inputenc Error: Unicode char ☃ (U+2603)
    (inputenc)                not set up for use with LaTeX.

If you want to use a certain character in your document that LaTeX doesn't
recognize, you can use the :tx:`\DeclareUnicodeCharacter{hexcode}{cmd}` command
provided by ``inputenc``.  Its first argument is the hexadecimal code point of
the Unicode character to define, and the second argument is the LaTeX command
to execute when the character is encountered. [#inputenc]_  For example:

.. code:: latex

    \usepackage{tikzsymbols}  % provides \Snowman
    \DeclareUnicodeCharacter{2603}{\Snowman}
    % Now you can put ☃ in your document!

If you don't want to have to enter characters as codepoints, the
:tx:`\newunicodechar` command provided by `the newunicodechar package
<https://ctan.org/pkg/newunicodechar>`_ lets you use the character itself
instead, [#newunicodechar-docs]_ allowing us to rewrite the example above as:

.. code:: latex

    \usepackage{newunicodechar}
    \usepackage{tikzsymbols}  % provides \Snowman
    \newunicodechar{☃}{\Snowman}
    % Now you can put ☃ in your document!

As a special case, loading the ``textcomp`` package lets you input all of the
Unicode characters that can be output with ``textcomp``'s commands; for
example, ``textcomp`` defines a :tx:`\textmusicalnote` command that produces ♪
(U+266A, EIGHTH NOTE), and so including ``textcomp`` in your preamble allows
you to write "♪" in your document and have it be treated as the
:tx:`\textmusicalnote` command, producing a "♪" in the output.


Non-Latin Alphabets
-------------------

The commands described so far only provide meaningful support for text in
Latin-derived alphabets.  In order to enter text in other alphabets, more
elaborate steps are required.

Cyrillic Alphabet
^^^^^^^^^^^^^^^^^

The most direct way to enable Cyrillic input is to specify a Cyrillic font
encoding in the ``fontenc`` command.  Due to the large number of Cyrillic
characters in existence, the script is split up into three font encodings (T2A,
T2B, and T2C) that each match up with the T1 encoding in the lower 7-bit range,
plus a fourth encoding, X2, that contains all of the Cyrillic characters but is
not compatible with T1. [#encguide]_ [#cyrguide]_

A purely-Cyrillic document can be written with the X2 font encoding as follows:

.. code:: latex

    \documentclass{article}
    \usepackage[X2]{fontenc}
    \usepackage[utf8]{inputenc}
    \begin{document}
    Пролетарии всех стран, соединяйтесь!
    \end{document}

If you want to use both Cyrillic and Latin characters in your document, you
need to pass both T1 and X2 to ``fontenc``.  Whichever one is listed last in
the ``fontenc`` command becomes the default font encoding for the document; the
other font encoding can be switched to by writing :tx:`\fontencoding{INSERT
ENCODING NAME HERE} \selectfont`. [#source2e]_ [#minimal]_ [#latex2e-unoff]_
For example:

.. code:: latex

    \documentclass{article}
    \usepackage[X2,T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \begin{document}
    “{\fontencoding{X2}\selectfont Пролетарии всех стран, соединяйтесь!}” said
    Señor Þor.
    \end{document}

Managing encodings this way can get annoying; fortunately, `the babel package
<https://ctan.org/pkg/babel>`_ provides a better way.  Add a
:tx:`\usepackage[LANGUAGES]{babel}` command to your preamble, where
``LANGUAGES`` is replaced by a comma-separated list of the languages that will
be used in your document; the last language in the list will become the
document's default language.  Within the document, the language can be changed
with :tx:`\selectlanguage{LANGUAGE}` (though, for short passages, it's better
to use :tx:`\foreignlanguage{LANGUAGE}{TEXT}`), and when it's set to a
Cyrillic-using language, you can write in Cyrillic. [#babel]_ [#cyrguide]_  For
example:

.. code:: latex

    \documentclass{article}
    % If we don't explicitly load a Cyrillic font encoding, babel emits a
    % warning and defaults to loading T2A.
    \usepackage[T2A,T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage[russian,english]{babel}
    \begin{document}
    “\foreignlanguage{russian}{Пролетарии всех стран, соединяйтесь!}” said
    Señor Þor.
    \end{document}


Greek Alphabet
^^^^^^^^^^^^^^

As with Cyrillic, entering Greek in LaTeX requires setting the font encoding,
in this case to LGR: [#encguide]_

.. TODO: Does this require greek-inputenc and/or greek-fontenc to be installed?

.. code:: latex

    \documentclass{article}
    \usepackage[LGR,T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \begin{document}
    “{\fontencoding{LGR}\selectfont Ἄνδρα μοι ἔννεπε, Μοῦσα, πολύτροπον, ὃς
    μάλα πολλὰ}” said Homer.

    “Is he talking about me?” wondered Señor Þor.
    \end{document}

As before, we can let also choose to let babel take care of the encodings for
us:

.. code:: latex

    \documentclass{article}
    % No need to explicitly load LGR!
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage[greek,english]{babel}
    \begin{document}
    “\foreignlanguage{greek}{Ἄνδρα μοι ἔννεπε, Μοῦσα, πολύτροπον, ὃς μάλα
    πολλὰ}” said Homer.

    “Is he talking about me?” wondered Señor Þor.
    \end{document}

As another alternative, `the greek-fontenc package
<https://ctan.org/pkg/greek-fontenc>`_ provides a ``textalpha`` package that
allows one to write Greek directly without the need for babel or
language-switching: [#greek-utf8]_

.. code:: latex

    \documentclass{article}
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage{textalpha}
    \begin{document}
    “Ἄνδρα μοι ἔννεπε, Μοῦσα, πολύτροπον, ὃς μάλα πολλὰ” said Homer.

    “Is he talking about me?” wondered Señor Þor.
    \end{document}

greek-fontenc also provides an ``alphabeta`` package that lets one use Greek
characters directly in math mode. [#greek-utf8]_


Other Alphabets
^^^^^^^^^^^^^^^

LaTeX's built-in font encodings only cover Latin, Cyrillic, and Greek.
Enabling input in other alphabets is a separate topic for each alphabet with no
easy one-size-fits-all answer.


.. _xetex and luatex:

XeTeX Engine (XeLaTeX) and LuaTeX Engine (LuaLaTeX)
===================================================

Besides pdfTeX, LaTeX can also run on two major alternative engines:

- `The XeTeX engine <http://xetex.sourceforge.net>`_, on which LaTeX runs as
  XeLaTeX

- `The LuaTeX engine <http://www.luatex.org>`_, on which LaTeX runs as
  LuaLaTeX.  This is a TeX engine with an embedded interpreter for `the Lua
  programming language <http://www.lua.org>`_ that allows developers to extend
  the engine by coding in Lua. [#faq-xelua]_ [#wiki-luatex]_

Both engines fully support Unicode input and support modern font technologies,
including being able to use fonts from the operating system.  [#xetex]_
[#faq-xelua]_  When it comes to Unicode support, the major differences between
pdfLaTeX and XeLaTeX/LuaLaTeX are:

- XeLaTeX and LuaLaTeX documents must always be written in UTF-8, while
  pdfLaTeX accepts document in various input encodings. [#lshort]_ [#minimal]_

- The ``fontenc`` and ``inputenc`` commands used in pdfLaTeX should be omitted
  when working with XeLaTeX/LuaLaTeX; the Unicode engines ignore (and give a
  warning about) ``inputenc``, while setting ``fontenc`` can actually cause
  some characters (like smart quotes) to not be recognized.  Instead, you can
  just start entering Unicode characters directly into your document without
  having to include any packages.

- The set of available Unicode characters in XeLaTeX/LuaLaTeX is determined by
  what characters are defined in the current font. [#minimal]_  The default
  font in both XeLaTeX and LuaLaTeX is `Latin Modern
  <http://www.gust.org.pl/projects/e-foundry/latin-modern>`_, a derivative of
  TeX's Computer Modern default font that adds many more characters.

- If XeLaTeX encounters a Unicode character that does not exist in the current
  font, the resulting PDF will show the font's placeholder character if it has
  one; if the font has no placeholder character, nothing will be shown.  Either
  way, the ``.log`` file will contain a line of the form::

      Missing character: There is no ☃ in font [lmroman10-regular]:mapping=tex-text;!

- If LuaLaTeX encounters a Unicode character that does not exist in the current
  font, the character will be omitted in the resulting PDF.  No warning will be
  emitted or logged.

- :tx:`\DeclareUnicodeCharacter` is not a valid command in XeLaTeX or LuaLaTeX;
  one must instead write something like:

  .. code:: latex

      \usepackage{tikzsymbols}  % provides \Snowman
      \catcode`☃=\active
      \protected\def ☃{\Snowman}

  :tx:`\newunicodechar` can still be used in place of this method, though.
  [#newunicodechar-docs]_

- Being able to write in another alphabet is largely a matter of switching to a
  font that supports that alphabet.  See `the fontspec package
  <https://ctan.org/pkg/fontspec>`_ for how to change fonts in XeLaTeX and
  LuaLaTeX.

- While neither XeLaTeX nor LuaLaTeX natively supports combining characters,
  the Lua scripting capabilities in the latter can be used to give combining
  characters in your source code the desired effect; see
  <https://tex.stackexchange.com/a/149197> for an example.


References
==========

.. [#inputenc]
   Alan Jeffrey and Frank Mittelbach,
   :t:`inputenc.sty`.
   Version 1.3c.
   Last modified 2018 August 11,
   <http://mirrors.ctan.org/macros/latex/base/inputenc.pdf>
   (accessed 2020 July 27).

.. [#newunicodechar-docs]
   Enrico Gregorio,
   :t:`The newunicodechar package`.
   Last modified 2018 April 8,
   <http://mirrors.ctan.org/macros/latex/contrib/newunicodechar/newunicodechar.pdf>
   (accessed 2020 July 27).

.. [#fontenc-vs-inputenc]
   "fontenc vs inputenc",
   :t:`TeX - LaTeX Stack Exchange`.
   Last modified 2018 April 3,
   <https://tex.stackexchange.com/q/44694>
   (accessed 2020 July 27).

.. [#encguide]
   Frank Mittelbach, Robin Fairbairns, Werner Lemberg, and LaTeX3 Project Team,
   :t:`LaTeX font encodings`.
   Last modified 2016 February 18,
   <https://www.latex-project.org/help/documentation/encguide.pdf>
   (accessed 2020 July 27).

.. [#greek-utf8]
   Günter Milde,
   :t:`Greek Unicode with 8-bit TeX and inputenc`.
   Last modified 2019 July 11,
   <http://mirrors.ctan.org/language/greek/greek-inputenc/greek-utf8.pdf>
   (accessed 2020 July 27).

.. [#source2e] 
   Johannes Braams, David Carlisle, Alan Jeffrey, Leslie Lamport, Frank
   Mittelbach, Chris Rowley, and Rainer Schöpf,
   :t:`The LaTeX2e Sources`.
   Last modified 2020 February 2,
   <http://mirrors.ibiblio.org/CTAN/macros/latex/base/source2e.pdf>
   (accessed 2020 July 27).

.. [#babel]
   Johannes L. Braams and Javier Bezos,
   :t:`Babel: Localization and internationalization`.
   Version 3.47.
   Last modified 2020 July 13,
   <http://mirrors.ctan.org/macros/latex/required/babel/base/babel.pdf>
   (accessed 2020 July 27).

.. [#ltnews28]
   :t:`LaTeX News`, issue 28, 2018 April.
   <https://www.latex-project.org/news/latex2e-news/ltnews28.pdf>
   (accessed 2020 July 27).

.. [#latex2e-unoff] 
   :t:`LaTeX2e unofficial reference manual`.
   Last modified 2018 October,
   <http://tug.org/texinfohtml/latex2e.html>
   (accessed 2020 July 27).

.. [#lshort]
   Tobias Oetiker, Hubert Partl, Irene Hyna, and Elisabeth Schlegl,
   :t:`The Not So Short Introduction to LaTeX2ε`.
   Version 6.2.
   Last modified 2018 February 28,
   <http://tug.ctan.org/info/lshort/english/lshort.pdf>
   (accessed 2020 July 27).

.. [#cyrguide]
   Vladimir Volovich, Werner Lemberg, and LaTeX3 Project Team,
   :t:`Cyrillic languages support in LaTeX`.
   Last modified 1999 March 12,
   <https://www.latex-project.org/help/documentation/cyrguide.pdf>
   (accessed 2020 July 27).

.. [#faq-xelua]
   "What are XeTeX and LuaTeX?",
   :t:`The TeX Frequently Asked Question List`.
   <https://www.texfaq.org/FAQ-xetex-luatex>
   (accessed 2020 July 27).

.. [#minimal]
   "What Unicode characters does pdfLaTeX support with a minimal preamble?",
   :t:`TeX - LaTeX Stack Exchange`.
   Last modified 2020 July 27,
   <https://tex.stackexchange.com/q/555199>
   (accessed 2020 July 27).

.. [#use-fontenc]
   "Why should I use \\usepackage[T1]{fontenc}?",
   :t:`TeX - LaTeX Stack Exchange`.
   Last modified 2017 April 13,
   <https://tex.stackexchange.com/a/677>
   (accessed 2020 July 27).

.. [#wiki-luatex]
   Wikipedia contributors,
   "LuaTeX,"
   :t:`Wikipedia, The Free Encyclopedia`.
   <https://en.wikipedia.org/w/index.php?title=LuaTeX&oldid=965669811>
   (accessed 2020 July 27).

.. [#xetex]
   :t:`XeTeX - Unicode-based TeX`.
   <http://xetex.sourceforge.net>
   (accessed 2020 July 27).
