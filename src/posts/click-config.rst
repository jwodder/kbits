==========================================================
Setting Default Option Values from Config Files with Click
==========================================================

:Date: 2020-07-17
:Category: Programming
:Tags: Python, Click
:Summary:
    How to set up a Click program to read default option values from a config
    file

When developing a command-line application in Python with Click_, you may find
yourself wanting to use a configuration file to set the parameters' default
values at runtime and to be able to specify such a file with a ``--config``
option.  There are various libraries of varying quality that provide such
functionality in different ways; however, implementing such functionality on
one's own is simple enough (as this document will show), and knowing the
basics will help you develop more advanced implementations when the libraries
out there don't meet your needs.

All code in this document has been tested against Click version 7.1.2.

.. _Click: https://palletsprojects.com/p/click/


``default_map``
===============

The key feature of Click that will allow us to set parameter values from a
configuration file is the ``default_map`` attribute of ``click.Context``,
documented at `[1]
<https://click.palletsprojects.com/en/7.x/commands/#overriding-defaults>`_.
Any values set in this ``dict`` before parameters are processed will become the
parameters' new default values.  Any extra keys that do not correspond to
defined parameters are ignored.

Moreover, Click will map values in ``default_map`` through the parameters'
normal type conversion & validation routines.  This means that, if you have an
option ``--foo`` defined with ``type=int``, you can set
``ctx.default_map["foo"] = "5"``, and the value will be converted to an ``int``
by the time it's passed to the command callback.  This even works for boolean
flags: a value set for a boolean flag option will be processed by the
|click_BOOL|_ type, which maps boolean-like strings to ``bool`` values.  This
eases your workload when reading from a configuration file type like INI where
values don't come with type information; just pass the values straight to
Click, and it'll do the conversion for you the same as it does for values on
the command line.

Areas to be careful in include parameters defined with ``multiple=True``.
The default value for such parameters (whether declared with ``default=`` in
the parameter's decorator or set in ``default_map``) must be a list or tuple;
setting such a default to a string will cause the string to be interpreted as a
list of single-character strings.  Also requiring special attention are options
defined with ``nargs`` or with a tuple of types; correct handling for all of
these is left as an exercise for the reader.

.. |click_BOOL| replace:: ``click.BOOL``
.. _click_BOOL: https://click.palletsprojects.com/en/7.x/parameters/#parameter-types


Implementing a ``--config`` option
==================================

In order to define a ``--config FILE`` option that reads from ``FILE`` and sets
other parameters' default values, the option first of all needs to be eager_ so
that it can modify ``ctx.default_map`` before the other options read it, and it
needs to be defined with a callback that does the actual work.  Everything else
after that is straightforward.

.. _eager: https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options

Here is a sample Python script with a ``--config`` option that reads from a
given config file (or from ``config.ini`` in the current directory if no config
file is given).  The config file must be an INI file, and the values for the
options are read from the ``[options]`` section.  The command callback simply
dumps out its arguments so you can see what's being passed to it.

.. code:: python

    from   configparser import ConfigParser
    import json
    import click

    DEFAULT_CFG = 'config.ini'

    def configure(ctx, param, filename):
        cfg = ConfigParser()
        cfg.read(filename)
        try:
            options = dict(cfg['options'])
        except KeyError:
            options = {}
        ctx.default_map = options

    @click.command()
    @click.option(
        '-c', '--config',
        type         = click.Path(dir_okay=False),
        default      = DEFAULT_CFG,
        callback     = configure,
        is_eager     = True,
        expose_value = False,
        help         = 'Read option defaults from the specified INI file',
        show_default = True,
    )
    @click.option('--integer', type=int, default=42)
    @click.option('--flag/--no-flag', default=False)
    @click.option('--str', default='foo')
    @click.option('--choice', type=click.Choice(['red', 'green', 'blue']))
    def main(**kwargs):
        print(json.dumps(kwargs, sort_keys=True, indent=4))

    if __name__ == '__main__':
        main()

If we run this script with no options when ``config.ini`` does not exist or is
empty, we get the parameters' built-in default values:

.. code:: console

    $ python3 config01.py
    {
        "choice": null,
        "flag": false,
        "integer": 42,
        "str": "foo"
    }

That's boring!  Try populating ``example.ini`` with the below text:

.. code:: ini

    [options]
    integer = 23
    flag = yes
    str = bar
    choice = green

… and then run with ``--config example.ini``:

.. code:: console

    $ python3 config01.py --config example.ini
    {
        "choice": "green",
        "flag": true,
        "integer": 23,
        "str": "bar"
    }

Note that the values set for the ``flag`` and ``integer`` options have been
converted to their appropriate types.

Of course, options set in the config file are overridden by command-line
options, no matter where the options occur in relation to ``--config``:

.. code:: console

    $ python3 config01.py --integer 17 --config example.ini --str glarch
    {
        "choice": "green",
        "flag": true,
        "integer": 17,
        "str": "glarch"
    }

What if a value in the config file is invalid?  Try saving the following text
to ``bad.ini``:

.. code:: ini

    [options]
    choice = mauve

The script will then error when passed this config file:

.. code:: console

    $ python3 config01.py --config bad.ini
    Usage: config01.py [OPTIONS]
    Try 'config01.py --help' for help.

    Error: Invalid value for '--choice': invalid choice: mauve. (choose from red, green, blue)

Not the best possible error message (It doesn't tell us the bad value was in
the config file), but it's better than a stack trace.

Note that, with this code, parameters in the config file must be named using
the same name & spelling as the parameter's corresponding argument to the
command callback.  For example, the ``--integer`` option must be written
``integer``, not ``--integer`` or ``-i`` or ``i``; any entries in the config
file with an invalid spelling will be ignored.  For options with medial hyphens
on the command line, like ``--log-level``, the hyphens must become underscores
in the configuration file, like ``log_level``.  If you want to support the
spelling ``log-level`` as well, insert the following line after ``cfg =
ConfigParser()`` to make the ``ConfigParser`` object convert hyphens in option
names to underscores:

.. code:: python

    cfg.optionxform = lambda s: s.replace('-', '_')


Configuring command groups
==========================

``default_map`` supports passing values to subcommands in command groups in a
very simple way: if the main command has a subcommand named "``foo``", then
``ctx.default_map["foo"]`` can be set to a ``dict`` of parameter names & values
for ``foo``.  For example, the following assignment:

.. code:: python

    ctx.default_map = {
        "color": "red",
        "foo": {
            "speed": "high",
        },
        "bar": {
            "speed": "low",
            "baz": {
                "time": "late",
            },
        },
    }

sets the default value for the main command's ``--color`` option to ``red``,
the default value of the ``foo`` subcommand's ``--speed``  option to ``high``,
the default value of the ``bar`` subcommand's ``--speed`` option to ``low``,
and the default value of the ``bar baz`` sub-subcommand's ``--time`` option to
``late``.  As you can see, this comes with one major drawback: a command can't
have a subcommand with the same name as one of its parameters.

Here is a sample Python script with command groups that reads configuration
from an INI file.  Settings in the ``[options]`` section are applied to the
top-level command, settings in the ``[options.CMD]`` section are applied to the
subcommand ``CMD``, settings in ``[options.CMD1.CMD2]`` are applied to the
``CMD2`` sub-subcommand of the ``CMD1`` subcommand, and so forth.  As above,
each command prints out the parameters it receives.

.. code:: python

    from   configparser import ConfigParser
    import json
    import click

    DEFAULT_CFG = 'config.ini'

    def configure(ctx, param, filename):
        cfg = ConfigParser()
        cfg.read(filename)
        ctx.default_map = {}
        for sect in cfg.sections():
            command_path = sect.split('.')
            if command_path[0] != 'options':
                continue
            defaults = ctx.default_map
            for cmdname in command_path[1:]:
                defaults = defaults.setdefault(cmdname, {})
            defaults.update(cfg[sect])

    @click.group(invoke_without_command=True)
    @click.option(
        '-c', '--config',
        type         = click.Path(dir_okay=False),
        default      = DEFAULT_CFG,
        callback     = configure,
        is_eager     = True,
        expose_value = False,
        help         = 'Read option defaults from the specified INI file',
        show_default = True,
    )
    @click.option('--integer', type=int, default=42)
    @click.option('--flag/--no-flag', default=False)
    @click.option('--str', default='foo')
    @click.option('--choice', type=click.Choice(['red', 'green', 'blue']))
    def main(**kwargs):
        print('* main')
        print(json.dumps(kwargs, sort_keys=True, indent=4))

    @main.command()
    @click.option('--speed', type=click.Choice(['low', 'medium', 'high', 'ludicrous']), default='medium')
    def foo(**kwargs):
        print('* foo')
        print(json.dumps(kwargs, sort_keys=True, indent=4))

    @main.group(invoke_without_command=True)
    @click.option('--speed', type=click.Choice(['low', 'medium', 'high', 'ludicrous']), default='medium')
    def bar(**kwargs):
        print('* bar')
        print(json.dumps(kwargs, sort_keys=True, indent=4))

    @bar.command()
    @click.option('--time', type=click.Choice(['early', 'late', 'exact']), default='early')
    def baz(**kwargs):
        print('* baz')
        print(json.dumps(kwargs, sort_keys=True, indent=4))

    if __name__ == '__main__':
        main()

Set ``config.ini`` to the following:

.. code:: ini

    [options]
    integer = 23
    flag = yes
    str = bar
    choice = green

    [options.foo]
    speed = high

    [options.bar]
    speed = low

    [options.bar.baz]
    time = late

… and then invoke some commands to see the results:

.. code:: console

    $ python3 config02.py
    * main
    {
        "choice": "green",
        "flag": true,
        "integer": 23,
        "str": "bar"
    }
    $ python3 config02.py foo
    * main
    {
        "choice": "green",
        "flag": true,
        "integer": 23,
        "str": "bar"
    }
    * foo
    {
        "speed": "high"
    }
    $ python3 config02.py bar
    * main
    {
        "choice": "green",
        "flag": true,
        "integer": 23,
        "str": "bar"
    }
    * bar
    {
        "speed": "low"
    }
    $ python3 config02.py bar baz
    * main
    {
        "choice": "green",
        "flag": true,
        "integer": 23,
        "str": "bar"
    }
    * bar
    {
        "speed": "low"
    }
    * baz
    {
        "time": "late"
    }
    $ python3 config02.py --choice red foo --speed medium
    * main
    {
        "choice": "red",
        "flag": true,
        "integer": 23,
        "str": "bar"
    }
    * foo
    {
        "speed": "medium"
    }
