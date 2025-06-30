===================================================
Process Groups, Sessions, and Controlling Terminals
===================================================

:Date: 2025-06-30
:Category: Programming
:Tags: UNIX, processes, terminals
:Summary:
    A summary of UNIX's process groups, sessions, & controlling terminals and
    how to work with them

In UNIX, job control is implemented via *process groups* and *sessions*, which
allow a shell to place processes in the foreground (directly communicating with
a terminal) or in the background and to send signals to multiple processes at
once.  This article provides an overview of the concepts and shows the basics
of how to work with them.

Unless specified otherwise, all information in this article is as per
`POSIX.1-2024`__.

__ https://pubs.opengroup.org/onlinepubs/9799919799/

.. role:: kbd(literal)

Concepts
========

Each UNIX process belongs to a *process group* (a.k.a. *job*).

- Each process group is identified by an integer *process group ID*, and the
  process (if any) whose process ID equals this process group ID is called the
  *process group leader*.

- It is possible to send a signal to all processes in a process group at once
  using ``kill()`` [POSIX__] [man7__] or ``killpg()`` [POSIX__] [man7__].

    __ https://pubs.opengroup.org/onlinepubs/9799919799/functions/kill.html
    __ https://man7.org/linux/man-pages/man2/kill.2.html
    __ https://pubs.opengroup.org/onlinepubs/9799919799/functions/killpg.html
    __ https://man7.org/linux/man-pages/man3/killpg.3.html

Each process group belongs to a *session*.

- The process that created a session is the *session leader*.  This process is
  also the process group leader of its process group.

- POSIX does not specify IDs for sessions, though Linux uses the process
  (group) ID of the session leader as the session ID.

A session may be associated with at most one terminal called its *controlling
terminal*, and each controlling terminal is associated with exactly one
session.

- The controlling terminal is established by the session leader, which then
  becomes known as the *controlling process* for as long as the terminal
  remains the controlling terminal.  When the controlling process terminates,
  the session loses the controlling terminal, and any attempts by the remaining
  processes in the session to access the terminal may result in a ``SIGHUP``
  signal.

- It is possible for an individual process in a session to dissociate from the
  controlling terminal without affecting the rest of the session.

- When a modem disconnect is detected for a controlling terminal, unless
  ``CLOCAL`` is set in the terminal's ``c_cflag`` field, ``SIGHUP`` is sent to
  the terminal's controlling process, which by default terminates it.  Any
  further attempts to read from the terminal will return EOF.

Given a session associated with a controlling terminal, at most one process
group in the session is the *foreground process group*, and all others are
*background process groups*.

- Processes in a foreground process group may read from & write to the
  controlling terminal.  If a process in a background process group tries to
  read from the controlling terminal, the entire process group will normally
  [#fn1]_ be sent a ``SITTIN`` signal, which by default stops & suspends the
  group.  If a process in a background process group tries to write to a
  controlling terminal, the entire process group will normally [#fn1]_ be sent
  a ``SIGTTOU`` signal, which by default stops & suspends the group; if
  ``TOSTOP`` is not set in the controlling terminal's ``c_lflag`` field, the
  process will instead be allowed to write to the terminal, and no signal will
  be sent.

  .. [#fn1] See the special cases listed under the `"Terminal Access
     Control"`__ section of the POSIX standard for when this is not the case.

  __ https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap11.html#tag_11_01_04

- Certain input key sequences like :kbd:`Ctrl`-:kbd:`C`, when entered at a
  controlling terminal, will cause a signal to be sent to all processes in the
  associated foreground process group.

- Processes in the foreground process group are sent a ``SIGWINCH`` signal
  whenever the size of the controlling terminal changes.

Whenever a new process is created via ``fork()`` or similar, it starts out with
the same session, process group, and controlling terminal as its parent.  A
process's session, process group, and controlling terminal remain the same
across a call to ``execve()``.

Process Groups at the Shell
===========================

.. To include:
    - how the shell divides commands into process groups
    - backgrounding & foregrounding in the shell?


In a POSIX-compatible shell, running a line composed of one or more *AND-OR
lists* (commands containing zero or more of the operators ``!``, ``|``, ``&&``,
and/or ``||``) separated by semicolons creates a single foreground process
group.  If an AND-OR list in a line is terminated by ``&`` (making it an
*asynchronous AND-OR list*), then everything before it in the line (up to the
previous ``&``, if any) is run in a single foreground process group, and the
asynchronous AND-OR list itself is run as a single background process group;
processing of the line then continues afterwards.

Examples:

.. code:: bash

    # These commands are all run in a single foreground process group:
    head bigfile.txt | grep foo && echo 'Those were the foos.'; rm bigfile.txt

    # These commands are all run in a single background process group:
    curl -fsSL -o download.html https://www.example.com || touch download-failed.txt &

    # The `echo` is run in a foreground process group, while the `wget` is
    # run in a background process group:
    echo 'Going to download now'; wget --quiet https://www.example.com &

    # The first `rm` and the `mkdir` are run in a foreground process group,
    # then the `wget` is started in a background process group, then the second
    # `rm` is started in a second background process group, and finally the
    # `echo` is run in another foreground process group.
    rm -rf download; mkdir downloads; \
        wget -qO downloads/example.html https://www.example.com & \
        rm -rf bigdir & \
        echo 'Am I done?'

A background process group created by a shell can be brought to the foreground
with the ``fg`` command, and a foreground process group can be placed in the
background by first stopping/suspending it with :kbd:`Ctrl`-:kbd:`Z` and then
running ``bg``.

Querying & Manipulating Process Groups & Sessions via System Calls
==================================================================

The process group ID of the current process can be retrieved with the
``getpgrp()`` [POSIX__] [man7__] function; the process group ID of an arbitrary
process can be retrieved with the ``getpgid()`` [POSIX__] [man7__] function.

__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/getpgrp.html
__ https://man7.org/linux/man-pages/man3/getpgrp.3p.html
__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/getpgid.html
__ https://man7.org/linux/man-pages/man3/getpgid.3p.html

A process can change its process group or the process group of a child process
via the ``setpgid()`` [POSIX__] [man7__] function; the target process group can
be either a pre-existing group in the same session or a new process group that
will be created in the same session.

- The process group ID of a session leader cannot be changed.  Thus, programs
  intending to create a new process group typically call ``fork()`` first and
  then call ``setpgid()`` from the child process in order to ensure that it's
  not being called by a session leader.

__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/setpgid.html
__ https://www.man7.org/linux/man-pages/man2/setpgid.2.html

The ``getsid()`` [POSIX__] [man7__] function can be used to retrieve the
process group ID of the session leader (equal to Linux's session ID) of a given
process.

__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/getsid.html
__ https://man7.org/linux/man-pages/man2/getsid.2.html

A new session can be created via the ``setsid()`` [POSIX__] [man7__] function,
which makes the calling process into the new session's session leader and into
the process group leader of a new process group in the session; the calling
process will have no controlling terminal afterwards.

- ``setsid()`` cannot be called by a process group leader.  Thus, programs
  intending to create a new session typically call ``fork()`` first and then
  call ``setsid()`` from the child process in order to ensure that it's not
  being called by a process group leader.

__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/setsid.html
__ https://man7.org/linux/man-pages/man2/setsid.2.html

The ``ctermid()`` [POSIX__] [man7__] function can be used to obtain the path to
the controlling terminal for the current process; the `GNU C Library
implementation`__ always returns ``"/dev/tty"``, which is a synonym for the
controlling terminal on Linux (and macOS?).

__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/ctermid.html
__ https://man7.org/linux/man-pages/man3/ctermid.3.html
__ https://www.gnu.org/software/libc/manual/html_node/Identifying-the-Terminal.html

.. tip::

    If you really want the actual path to a process's controlling terminal, and
    you don't want to invoke ``ps(1)`` to get it, you can get partway there
    using Linux's ``/proc`` filesystem: the seventh field of
    ``/proc/$PID/stat`` contains the device number for the controlling terminal
    of process ``$PID``, or 0 if the process doesn't have a controlling
    terminal.  Unfortunately, there is no convenient way to map the device
    number to a path; cf. `how ps does it`__.

    __ https://gitlab.com/procps-ng/procps/-/blob/v4.0.5/library/devname.c?ref_type=tags#L326

    Alternatively, you can approximate the controlling terminal for the current
    process with ``ttyname(STDIN_FILENO)`` or similar, but this won't be
    accurate in the rare cases where stdin has been replaced with something
    other than the controlling terminal, possibly even a different, unrelated
    terminal.

POSIX does not specify a mechanism for setting the controlling terminal.  On
Linux and macOS, the controlling terminal for a session is established when a
session leader first opens a terminal, unless the ``O_NOCTTY`` flag was passed
to the ``open()`` call.  Linux and macOS also support setting the controlling
terminal via a session leader calling ``ioctl()`` with ``op`` set to
``TIOCSCTTY`` [man7__], and any process may dissociate from its controlling
terminal by calling ``ioctl()`` with ``op`` set to ``TIOCNOTTY`` [man7__].

__ https://man7.org/linux/man-pages/man2/TIOCSCTTY.2const.html
__ https://man7.org/linux/man-pages/man2/TIOCNOTTY.2const.html

- When a session gains a controlling terminal, the process group of the session
  leader becomes the foreground process group.

- Note that a session gaining a controlling terminal will not cause any
  pre-existing processes in the session (other than the session leader) to gain
  a controlling terminal, but any processes spawned from the session leader
  afterwards will have a controlling terminal.

A process with a controlling terminal can acquire the process group ID of its
session's foreground process group by calling ``tcgetpgrp()`` [POSIX__]
[man7__], and it can set the foreground process group by calling
``tcsetpgrp()`` [POSIX__] [man7__].

__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/tcgetpgrp.html
__ https://man7.org/linux/man-pages/man3/tcgetpgrp.3.html
__ https://pubs.opengroup.org/onlinepubs/9799919799/functions/tcsetpgrp.html
__ https://man7.org/linux/man-pages/man3/tcsetpgrp.3.html

There does not appear to be any way to get a list of processes in a process
group, a list of process groups in a session, or a list of extant sessions
other than by iterating over ``/proc/*/stat`` files or using a facility that
does that for you, like ``ps(1)``.

Creating a Background Process Without a Controlling Terminal (Daemonization)
============================================================================

In order to run a process as a *daemon*, running truly in the background,
without a controlling terminal that could send ``SIGHUP`` on session exit, you
could use a super-server like ``systemd`` or ``supervisord``, but if you're
reading this, you probably want to know how they do it.

A program seeking to run itself or another executable as a daemon should take
the following steps:

1. Call ``fork()``.  The rest of the steps are carried out in the resulting
   child process, which is guaranteed not to be a session leader or process
   group leader.  The parent process can either exit immediately or else track
   the child process in order to detect & report any immediate unsuccessful
   terminations.

2. Call ``setsid()`` to create a new session, one not associated with any
   controlling terminal.

3. Close or redirect stdin, stdout, & stderr so that they no longer refer to
   the original terminal.  It's also recommended to set the current working
   directory to the root directory, as using a different working directory
   could prevent unmounting.

4. Call ``fork()`` again to create a child process that is not a session leader
   and thus cannot establish a controlling terminal.  This child process is
   then used for the actual program proper (possibly via ``execve()``), and the
   parent process exits.
