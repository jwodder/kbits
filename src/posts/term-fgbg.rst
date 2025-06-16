===========================================================
Getting a Terminal's Default Foreground & Background Colors
===========================================================

:Date: 2025-06-10
:Modified: 2025-06-16
:Category: Programming
:Tags: terminals, ANSI escape codes
:Summary:
    When using `ANSI escape sequences <ansi_>`_ to style text on a terminal,
    you may need to know exactly what the default foreground & background
    colors — the ones set with ``\e[39m`` and ``\e[49m`` — are, as knowing
    whether the user's terminal is light-on-dark or dark-on-light can help you
    pick an appropriate color theme.  Fortunately, the `escape sequences
    supported by xterm and compatible terminals <xtermctl_>`_ include sequences
    for doing just that.

When using `ANSI escape sequences <ansi_>`_ to style text on a terminal, you
may need to know exactly what the default foreground & background colors — the
ones set with ``\e[39m`` and ``\e[49m`` — are, as knowing whether the user's
terminal is light-on-dark or dark-on-light can help you pick an appropriate
color theme.  Fortunately, the `escape sequences supported by xterm and
compatible terminals <xtermctl_>`_ include sequences for doing just that.

.. _ansi: https://en.wikipedia.org/wiki/ANSI_escape_code
.. _xtermctl: https://invisible-island.net/xterm/ctlseqs/ctlseqs.html

A program whose standard input & standard output are both connected to an
xterm-compatible terminal can query the default foreground color by writing the
characters ``\e]10;?\e\\\\`` to standard output, where ``\e`` is the Escape
character (0x1B) and ``\\\\`` represents a single backslash; to query the
default background color instead, change the ``10`` to an ``11``.  The terminal
will then respond by writing back the query string with the ``?`` replaced by a
string describing the default foreground or background color.

In my limited experience, all color strings I've seen in responses have been
RGB values of the form ``rgb:XXXX/XXXX/XXXX``, where the ``X``'s are lowercase
hexadecimal digits (so white would be ``rgb:ffff/ffff/ffff`` and black would be
``rgb:0000/0000/0000``), but `xterm's documentation <xtermctl_>`_ seems to
suggest that color names (presumably ones from the X11 color list) and any RGB
specifications accepted by |xparsecolor|_ are also possible return values.

.. |xparsecolor| replace:: ``XParseColor(3)``
.. _xparsecolor: https://linux.die.net/man/3/xparsecolor

.. note::

    The ``\e\\\\`` portion of the query & response (called the *string
    terminator* or ST) also has a legacy variant, a single BEL character
    (0x07), which you may see sometimes.  xterm always responds using the same
    string terminator as used in the request.

.. tip::

    By replacing the ``?`` with an RGB specification, you can change the
    default foreground & background colors instead!

As with `getting the current cursor position <{filename}cursor-pos.rst>`_, the
terminal will need to be set in cbreak and noecho modes when reading the
response.

If you just want to see some code for doing all this on a Unix-like system,
here it is as a Python script:

.. code:: python

    from __future__ import annotations
    from collections.abc import Iterator
    from contextlib import contextmanager
    from copy import deepcopy
    import re
    import sys
    import termios


    def get_default_fg() -> str:
        """
        Query the attached terminal for the default foreground color and return the
        color string from the response

        :raises IOError: if stdin or stdout is not a terminal
        :raises ValueError: if the reply from the terminal is malformed
        """
        return osc_query(10)


    def get_default_bg() -> str:
        """
        Query the attached terminal for the default background color and return the
        color string from the response

        :raises IOError: if stdin or stdout is not a terminal
        :raises ValueError: if the reply from the terminal is malformed
        """
        return osc_query(11)


    def osc_query(ps: int) -> str:
        if sys.stdin.isatty() and sys.stdout.isatty():
            with cbreak_noecho():
                print(f"\x1b]{ps};?\x1b\\", end="", flush=True)
                resp = b""
                while not resp.endswith((b"\x1b\\", b"\x07")):
                    resp += sys.stdin.buffer.read(1)
            s = resp.decode("utf-8", "surrogateescape")
            if m := re.fullmatch(rf"\x1B\]{ps};(.+)(?:\x1B\\|\x07)", s):
                return m[1]
            else:
                raise ValueError(s)
        else:
            raise IOError("not connected to a terminal")


    # File descriptor for standard input:
    STDIN = 1

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
        print("Foreground color:", get_default_fg())
        print("Background color:", get_default_bg())
