=====================================================
Retrieving Logs for a Single Service Run from systemd
=====================================================

:Date: 2026-05-10
:Category: Software
:Tags: systemd, UNIX
:Summary:
    How to get the command output for a single run of a systemd service from
    the systemd journal

`systemd <https://systemd.io>`_ is the init system and service manager (and a
bunch of other things) used by many major Linux distributions.  As a service
manager, it provides the ability to run programs (called *services*) in the
background with features like restarting failed programs or running programs on
a schedule.  By default (i.e., unless a service's unit file says to send it
somewhere else), the output from these programs is stored in a journal_ that
can be viewed with the |journalctl|_ command.  However, basic ``journalctl(1)``
invocations have the potential to swamp you with logs; sometimes you just want
to see the output from a single run of a service or see a history of when a
service was started & stopped.  Here's how you do that.

.. _journal: https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html

.. |journalctl| replace:: ``journalctl(1)``
.. _journalctl: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html

This article is based on systemd 255 on Ubuntu Noble 24.04.  There may be some
corner cases I have missed that make what I say here not 100% accurate.


Basic ``journalctl(1)`` Usage
=============================

By default, a given user only has permission to read journal entries for their
own per-user systemd service manager.  In order to read the system journal or
other users' journals, you must be ``root`` (possibly via ``sudo``) or belong
to the ``systemd-journal``, ``adm``, or ``wheel`` group.

.. important::

    Journal entries do not last forever; you only have so much disk space,
    after all.  Depending on configuration, the journal service will delete old
    entries if they reach a certain age or if the total size of the journal
    reaches a certain limit.  You therefore might not be able to retrieve
    information from the journal about things that happened too long ago.

You can get a basic view of all the journal entries for a service by running
``journalctl -u $service``, where ``$service`` is the name of the service with
or without the "``.service``" suffix.  Add the ``--user`` option if the service
belongs to your per-user manager.  The entries shown can be limited with the
``-n``/``--lines``, ``--since``, and ``--until`` options, among others; see the
|journalctl|_ manpage for more information.

By default, the output from ``journalctl`` is a chronological sequence of both
systemd-generated messages (things like "Starting myservice.service") and
service-generated messages (such as standard output from the service commands).
Each line consists of a timestamp, a hostname, a command name, a PID, and the
actual message.  The ``-o``/``--output`` option can be used to adjust the
output format, though most formats only differ in how the timestamp is
displayed.

Internally, each entry in systemd's journal consists of a number of key-value
pairs called *fields* that include data on the logged message, when it was
emitted, and where it came from.  Most of the fields are documented in
|systemd.journal-fields|_, and you can output all fields of journal entries by
passing ``-o json`` (or ``-o json-pretty`` or another supported JSON format) or
``-o verbose`` to ``journalctl``.

.. |systemd.journal-fields| replace:: ``systemd.journal-fields(7)``
.. _systemd.journal-fields: https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html

``journalctl`` entries can be filtered based on field values by passing the
command one or more *match arguments* of the form ``FIELDNAME=VALUE``.  Note
that only exact string matches on values are supported; you cannot ask
``journalctl`` to filter, say, by a regex or by whether a field is set/unset;
for that, postprocessing the output with |jq|_ or another program is necessary.
Multiple match arguments for the same field name are ORed together, while match
arguments for different fields are ANDed.  Using ``+`` as an argument causes
the preceding match arguments to be ORed as a group against the following match
arguments.

.. |jq| replace:: ``jq(1)``
.. _jq: https://jqlang.org


Systemd vs. Service Entries
===========================

When working with a service's journal logs, there are two main types of entries
that we usually want to discern between: entries emitted by systemd itself
about the service — usually messages of the form "Starting myservice.service",
"Stopped myservice.service", etc. — and entries that contain output from the
service's actual command(s).

Entries from systemd itself about a service are distinguished by having the
``INVOCATION_ID`` field (or ``USER_INVOCATION_ID`` for user services) set but
not ``_SYSTEMD_INVOCATION_ID``; the ``SYSLOG_IDENTIFIER`` field will also have
a value of "``systemd``".  The ``UNIT`` field (or ``USER_UNIT`` for user
services) will also be set to the name of the service in question (including
template arguments and the "``.service``" suffix).

.. caution::

    Field names without leading underscores are not "trusted" journal fields,
    and thus any program that writes directly to the journal can create an
    entry with ``INVOCATION_ID``, ``SYSLOG_IDENTIFIER``, or ``UNIT`` set to
    whatever it wants.  In order to exclude any potential deceptive entries
    when using ``journalctl`` to filter by one or more of these fields, include
    ``_PID=1`` as a match argument so that you only see entries from
    ``systemd`` itself.  Note that this only works when querying the system
    manager; for user managers, there does not seem to be a foolproof way to
    say "only show entries generated by the manager."

Entries for actual output from a service's commands (including child commands)
are distinguished by having the ``_SYSTEMD_INVOCATION_ID`` field set, but not
``INVOCATION_ID`` or ``USER_INVOCATION_ID``.  The ``_SYSTEMD_UNIT`` field (or
``_SYSTEMD_USER_UNIT`` for user services) will also be set to the name of the
service in question (including template arguments and the "``.service``"
suffix).

Note that the latter kind of entries don't just cover the service's stdout &
stderr; if the service command logged anything via syslog or wrote to the
journal directly, that's in here, too.  You can separate out these sources by
filtering on the ``_TRANSPORT`` field, which has a value of "``stdout``" for
the command's standard output & standard error (and for input to
|systemd-cat|_), "``syslog``" for syslog messages, and "``journal``" for
messages written directly to the journal with the |sd_journal_print|_ APIs.

.. |systemd-cat| replace:: ``systemd-cat(1)``
.. _systemd-cat: https://www.freedesktop.org/software/systemd/man/latest/systemd-cat.html

.. |sd_journal_print| replace:: ``sd_journal_print(3)``
.. _sd_journal_print: https://www.freedesktop.org/software/systemd/man/latest/sd_journal_print.html

You may be wondering about the value of the ``SYSLOG_IDENTIFIER`` mentioned
above when it comes to command output entries.  As far as I can determine, when
``_TRANSPORT`` is "``stdout``" or "``journal``", ``SYSLOG_IDENTIFIER`` is
usually the filename of the executable that produced the message, except for
messages produced with ``systemd-cat``, which use the identifier specified on
the command line with ``--identifier``, leaving the field unset if the option
is not given.  For ``_TRANSPORT=syslog``, ``SYSLOG_IDENTIFIER`` is the program
name by default, but programs that write to syslog are free to use any string
they want as their identifier.


Invocation IDs
==============

As you may have noticed above, journal entries related to a service run all
have an invocation ID associated with them.  Each invocation ID is a random
32-character hexadecimal string that identifies a specific *runtime cycle* of a
service (the period between when the service changes from "inactive" to
"active"/"activating" and when it becomes inactive again).  An invocation ID is
the key information needed to get the logs for a single service run from
``journalctl``.

If you want to view the logs for the most-recently started run of a service,
begin by getting that run's invocation ID via::

    systemctl show --no-pager -P InvocationID $service

Replace ``$service`` with the name of the service in question (with or without
the "``.service``" suffix).  If querying a user session unit, add ``--user`` to
the command.  If the service has stopped and not been restarted, this command
will nevertheless output the invocation ID for the most recent (stopped) run.
If the given service does not exist or was never started, the command will
output a blank line.

If the run you want logs for is not the most recent, you'll need to determine
the run's invocation ID by looking back through the journal for the service.
If you just know the approximate time at which the desired run occurred, you
can browse the "Starting $service.service" and "Stopped $service.service"
systemd messages with their timestamps & corresponding invocation IDs by using
|jq|_ and the following shell command::

    journalctl -o json -t systemd -u $service | jq -r '"[\(.__REALTIME_TIMESTAMP|tonumber / 1000000 | todate)] [\(.INVOCATION_ID)] \(.MESSAGE)"'

Replace ``$service`` with the name of the service in question (with or without
the "``.service``" suffix).  If querying a user session unit, add ``--user`` to
the ``journalctl`` command and change ``.INVOCATION_ID`` in the ``jq`` command
to ``.USER_INVOCATION_ID``.

This will give you output like the following, letting you map timestamp ranges
to invocation IDs::

    [2026-04-22T13:41:35Z] [439e459b1db44a97974eae5c133f4543] Starting apache2.service - The Apache HTTP Server...
    [2026-04-22T13:41:36Z] [439e459b1db44a97974eae5c133f4543] Started apache2.service - The Apache HTTP Server.
    [2026-04-23T00:00:00Z] [439e459b1db44a97974eae5c133f4543] Reloading apache2.service - The Apache HTTP Server...
    [2026-04-23T00:00:00Z] [439e459b1db44a97974eae5c133f4543] Reloaded apache2.service - The Apache HTTP Server.
    [2026-04-24T00:00:00Z] [439e459b1db44a97974eae5c133f4543] Reloading apache2.service - The Apache HTTP Server...
    [2026-04-24T00:00:00Z] [439e459b1db44a97974eae5c133f4543] Reloaded apache2.service - The Apache HTTP Server.
    [2026-04-26T00:00:00Z] [439e459b1db44a97974eae5c133f4543] Reloading apache2.service - The Apache HTTP Server...
    [2026-04-26T00:00:01Z] [439e459b1db44a97974eae5c133f4543] Reloaded apache2.service - The Apache HTTP Server.
    [2026-04-27T00:00:01Z] [439e459b1db44a97974eae5c133f4543] Reloading apache2.service - The Apache HTTP Server...
    [2026-04-27T00:00:01Z] [439e459b1db44a97974eae5c133f4543] Reloaded apache2.service - The Apache HTTP Server.
    [2026-05-07T16:19:39Z] [439e459b1db44a97974eae5c133f4543] Stopping apache2.service - The Apache HTTP Server...
    [2026-05-07T16:19:40Z] [439e459b1db44a97974eae5c133f4543] apache2.service: Deactivated successfully.
    [2026-05-07T16:19:40Z] [439e459b1db44a97974eae5c133f4543] Stopped apache2.service - The Apache HTTP Server.
    [2026-05-07T16:19:40Z] [439e459b1db44a97974eae5c133f4543] apache2.service: Consumed 8min 45.667s CPU time, 111.8M memory peak, 22.5M memory swap peak.
    [2026-05-07T16:19:40Z] [c80c7d5e0453447ea57bf833b3ead2cf] Starting apache2.service - The Apache HTTP Server...
    [2026-05-07T16:19:40Z] [c80c7d5e0453447ea57bf833b3ead2cf] Started apache2.service - The Apache HTTP Server.
    [2026-05-08T00:00:00Z] [c80c7d5e0453447ea57bf833b3ead2cf] Reloading apache2.service - The Apache HTTP Server...
    [2026-05-08T00:00:01Z] [c80c7d5e0453447ea57bf833b3ead2cf] Reloaded apache2.service - The Apache HTTP Server.
    [2026-05-09T00:00:01Z] [c80c7d5e0453447ea57bf833b3ead2cf] Reloading apache2.service - The Apache HTTP Server...
    [2026-05-09T00:00:01Z] [c80c7d5e0453447ea57bf833b3ead2cf] Reloaded apache2.service - The Apache HTTP Server.
    [2026-05-10T00:00:00Z] [c80c7d5e0453447ea57bf833b3ead2cf] Reloading apache2.service - The Apache HTTP Server...
    [2026-05-10T00:00:00Z] [c80c7d5e0453447ea57bf833b3ead2cf] Reloaded apache2.service - The Apache HTTP Server.

If you don't know the run's timestamp but you can recognize the target run from
the command output, you can view all log messages prefixed with their
invocation IDs like so::

    journalctl -o json -u $service | jq -r '"[\(.INVOCATION_ID // ._SYSTEMD_INVOCATION_ID)] \(.MESSAGE)"'


Getting Logs for an Invocation ID
=================================

Once you have the invocation ID for the service run you want to view logs for,
you can get the service's output with::

    journalctl _SYSTEMD_INVOCATION_ID=$id

where ``$id`` is replaced by the invocation ID.  Note that there is no need to
specify the service name, nor even to specify ``--user`` for user session
units.

Note that the output from this command will include fields like timestamp,
hostname, command name, and PID in each line.  If you just want only the actual
output from the service with no "decorations," add ``-o cat`` to the command.
If you want custom formatting, your best bet is to output all the journal
fields with ``-o json`` and process the entries with ``jq`` or another program.

If you also want to include systemd's "Starting", "Stopped", etc. messages in
the output (say, in order to see the command's exit status), change the match
arguments like so::

    journalctl INVOCATION_ID=$id + _SYSTEMD_INVOCATION_ID=$id

If querying a user session unit, change ``INVOCATION_ID`` to
``USER_INVOCATION_ID``.
