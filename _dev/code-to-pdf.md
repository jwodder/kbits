Options for Converting Source Code to a PDF with Syntax Highlighting
====================================================================

GNU `enscript`
--------------

[The `enscript` program](https://www.gnu.org/software/enscript/) can be used to
convert text files to PostScript, which can then be converted to a PDF with
programs like Ghostscript's `ps2pdf`.

The following command takes a source code file `infile.py` and produces a
PostScript document `outfile.ps` that typesets the source code with syntax
highlighting and with every line numbered:

    enscript --color --highlight=python --line-numbers -o outfile.ps infile.py

Available highlight languages can be listed with `enscript --help-highlight`.

`enscript` also has options for setting the page header, printing in multiple
columns, highlighting alternating lines with grey backgrounds, and selecting
from among a small set of highlighting styles, among other features.

`enscript` does not support UTF-8.

Pygments + LaTeX
----------------

[Pygments](https://pygments.org) is a syntax highlighter written in Python that
can highlight [numerous languages](https://pygments.org/docs/lexers/) in
different styles.  It can output highlighted code in [several
formats](https://pygments.org/docs/formatters/), among them LaTeX, which can
then be processed into a PDF.

The following command takes a source code file `infile.py` and produces a
complete LaTeX document `outfile.tex` that typesets the source code with syntax
highlighting in the "`colorful`" style and with every line numbered.  (The
source code's language is determined based on the file extension; it can also
be set explicitly with the `-l <LANGUAGE>` option.)  The LaTeX file can then be
converted to a PDF with the `pdflatex` command; the `color` and `fancyvrb`
LaTeX packages are required for this step.

    pygmentize -f latex -O full,linenos,style=colorful -o outfile.tex infile.py

Note that Pygments attempts to stylize certain tokens as both bold and
monospaced, which does not work in LaTeX unless the `.tex` file is edited to
load `bold-extra` or a similar package.

One of the shortcomings of this approach is that long source lines will extend
off the edge of the page in a rendered PDF; the `minted` package includes an
option to wrap long lines instead.

Various LaTeX packages exist for invoking Pygments from within LaTeX to
highlight given text and typeset the results; these include
[`minted`](https://ctan.org/pkg/minted) (recommended),
[`texments`](https://ctan.org/pkg/texments), and
[`verbments`](https://ctan.org/pkg/verbments).

Pygments supports UTF-8.  LaTeX has UTF-8 support as well, but properly
enabling & configuring it is beyond the scope of this document.


<!-- TODO: Vim's :hardcopy command -->
<!-- TODO: LaTeX with the `listings` Package (kind of sucks) -->

<!-- a2ps <https://www.gnu.org/software/a2ps/>: sucks -->
