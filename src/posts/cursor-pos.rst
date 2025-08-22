===================================================
Getting the Current Cursor Position from a Terminal
===================================================

:Date: 2025-05-29
:Modified: 2025-08-22
:Category: Programming
:Tags: terminals, ANSI escape codes
:Summary:
    When using `ANSI escape sequences <ansi_>`_ to manipulate a compatible
    terminal, you may need to know where the text cursor is currently located
    on the screen, especially if its current location was set by the user or a
    previous program rather than your code.  Fortunately, the ANSI escape
    sequence standard `ECMA-48`_ provides a sequence for doing just that.

When using `ANSI escape sequences <ansi_>`_ to manipulate a compatible
terminal, you may need to know where the text cursor is currently located on
the screen, especially if its current location was set by the user or a
previous program rather than your code.  Fortunately, the ANSI escape sequence
standard `ECMA-48`_ provides a sequence for doing just that.

.. _ansi: https://en.wikipedia.org/wiki/ANSI_escape_code
.. _ECMA-48: https://ecma-international.org/publications-and-standards/standards/ecma-48/

A program whose standard input & standard output are both connected to an
ANSI-compatible terminal can query the current cursor location by writing the
characters ``\e[6n`` to standard output, where ``\e`` is the Escape character
(0x1B).  The terminal will then respond by writing back a string of the form
``\e[l;cR`` to standard input, where ``\e`` is the Escape character, ``l`` is a
decimal integer giving the line number of the cursor's current position, and
``c`` is a decimal integer giving the column number of the cursor's current
position.  The line & column numbers are both 1-based: the upper-left corner of
the screen is represented by (1, 1) rather than (0, 0).

Note that reading the terminal's response isn't as simple as it may seem at
first.  On Unix-like systems, standard input from the terminal is buffered by
default and only made available to the running program when a newline is
entered, but the terminal's response doesn't end in a newline, so typical
line-reading functions won't return until the user manually presses "Enter."
This can be solved by putting the terminal in *cbreak mode*, in which this
buffering is disabled and characters sent to standard input can be read
immediately.  (Alternatively, the terminal may be put in *raw mode* instead,
which is unbuffered like cbreak mode but also disables the special meanings of
certain terminal-affecting key sequences like Ctrl-Q and Ctrl-S.)

In addition to disabling buffering, you'll also want to disable echoing of
input.  By default, when the terminal sends its response to standard input, the
characters will appear on the screen as if the user typed them, which is likely
not what you want; turning off input echoing fixes this.

The full details of working with cbreak & noecho mode are a bit beyond the
scope of this article.  On Unix-like systems, you'll need to use the
``tcgetattr()`` and ``tcsetattr()`` functions from ``<termios.h>`` or whatever
wrapper around them your programming language of choice provides.

.. tip::

    To avoid a race condition, set cbreak and noecho mode *before* printing the
    query.

.. important::

    Be sure to set the terminal's cbreak and echo settings back to what they
    were originally when you're done reading the response!

Finally, if you just want to see some code for doing all this on a Unix-like
system, here it is as a Python script:

.. code:: python

    from __future__ import annotations
    from collections.abc import Iterator
    from contextlib import contextmanager
    from copy import deepcopy
    import re
    import sys
    import termios


    def cursor_pos() -> tuple[int, int]:
        """
        Query the attached terminal for the current cursor position and return
        the result as a ``(line, column)`` pair.

        :raises IOError: if stdin or stdout is not a terminal
        :raises ValueError: if the reply from the terminal is malformed
        """
        if sys.stdin.isatty() and sys.stdout.isatty():
            with cbreak_noecho():
                print("\x1b[6n", end="", flush=True)
                resp = b""
                while not resp.endswith(b"R"):
                    resp += sys.stdin.buffer.read(1)
            s = resp.decode("utf-8", "surrogateescape")
            if m := re.fullmatch(r"\x1B\[(?P<line>[0-9]+);(?P<col>[0-9]+)R", s):
                return (int(m["line"]), int(m["col"]))
            else:
                raise ValueError(s)
        else:
            raise IOError("not connected to a terminal")


    # File descriptor for standard input:
    STDIN = 0

    # Indices into the tuple returned by `tcgetattr()`:
    LFLAG = 3
    CC = 6


    @contextmanager
    def cbreak_noecho() -> Iterator[None]:
        """
        A context manager that configures the terminal on standard input to use
        cbreak mode and to disable input echoing.  The original terminal
        configuration is restored on exit.
        """
        orig = termios.tcgetattr(STDIN)
        term = deepcopy(orig)
        term[LFLAG] &= ~(termios.ICANON | termios.ECHO)
        term[CC][termios.VMIN] = 1
        term[CC][termios.VTIME] = 0
        termios.tcsetattr(STDIN, termios.TCSANOW, term)
        try:
            yield
        finally:
            termios.tcsetattr(STDIN, termios.TCSANOW, orig)


    if __name__ == "__main__":
        print(cursor_pos())
