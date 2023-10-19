=============================================
Implementing Boolean Negation Flags with Clap
=============================================

:Date: 2022-10-23
:Category: Programming
:Tags: Rust, clap, command-line parsing
:Summary:
    How to use Rust's clap_ library to implement boolean ``--foo`` and
    ``--no-foo`` flags that undo each other

Rust's clap_ library is the language's most popular crate for parsing
command-line arguments.  Though it has many useful features, programmers used
to libraries like Python's Click_ may find themselves struggling to implement
one certain CLI convention: boolean flags ``--foo`` and ``--no-foo`` that undo
each other.  This article will show you how to implement such flags using
clap's ``Parser`` derivation mode — no need to dig into the far more verbose
"builder" mode!

.. _clap: https://github.com/clap-rs/clap
.. _Click: https://palletsprojects.com/p/click/

.. note::

    The code in this article was tested with clap 4.0.18 on Rust 1.64.0.

.. tip::

    There is currently `an open issue`__ on clap's repository asking for an
    easier way to implement negation flags, but it doesn't seem that it'll be
    resolved any time soon.

    __ https://github.com/clap-rs/clap/issues/815

To implement two boolean flags ``--foo`` and ``--no-foo`` such that the field
``foo`` is true when ``--foo`` is given last and false when either no arguments
are given or when ``--no-foo`` is given last, simply declare a ``--foo``
boolean option as usual, then add a separate ``--no-foo`` option, and declare
that they override each other using overrides_with_.  The ``--foo`` option
field will then end up holding the final boolean value, and the ``--no-foo``
field will be unused, so put an underscore at the start of its name so that
clippy doesn't complain.  (If you don't want any unused fields in your
arguments struct, I'm afraid your only option is to turn to the more verbose
builder mode.)

.. _overrides_with: https://docs.rs/clap/4.0/clap/builder/struct.Arg.html#method.overrides_with

A minimal example of such code would look like this:

.. code:: rust

    use clap::Parser;

    #[derive(Debug, Parser)]
    struct Arguments {
        /// Foo all the bars
        #[clap(long, overrides_with = "_no_foo")]
        foo: bool,

        /// Don't foo any bars [default]
        #[clap(long = "no-foo")]
        _no_foo: bool,
    }

    fn main() {
        for opts in [
            vec!["arg0"],
            vec!["arg0", "--foo"],
            vec!["arg0", "--no-foo"],
            vec!["arg0", "--no-foo", "--foo"],
            vec!["arg0", "--foo", "--no-foo"],
            vec!["arg0", "--no-foo", "--foo", "--no-foo"],
            vec!["arg0", "--foo", "--no-foo", "--foo"],
        ] {
            let args = Arguments::parse_from(&opts);
            println!("{opts:?} -> {args:?}");
        }
    }

`[Link to the code on the Rust Playground]`__

__ https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=1ca92e953973e4e2649ec1c522957455

The output from the above code is::

    ["arg0"] -> Arguments { foo: false, _no_foo: false }
    ["arg0", "--foo"] -> Arguments { foo: true, _no_foo: false }
    ["arg0", "--no-foo"] -> Arguments { foo: false, _no_foo: true }
    ["arg0", "--no-foo", "--foo"] -> Arguments { foo: true, _no_foo: false }
    ["arg0", "--foo", "--no-foo"] -> Arguments { foo: false, _no_foo: true }
    ["arg0", "--no-foo", "--foo", "--no-foo"] -> Arguments { foo: false, _no_foo: true }
    ["arg0", "--foo", "--no-foo", "--foo"] -> Arguments { foo: true, _no_foo: false }

As you can see, the value of the ``foo`` field is true when ``--foo`` is the
last ``--foo/--no-foo`` option given and false otherwise.

What if you want a pair of boolean flags where the default is ``--foo``/true
rather than ``--no-foo``/false?  This is doable, but the code can look quite a
bit confusing.  Starting with the setup above, add ``action =
clap::builder::ArgAction::SetFalse`` to the ``--no-foo`` option; this will
invert the values of the ``--no-foo`` field, causing it to be true whenever
``--foo`` is the option in effect and false otherwise.  But wait — that's what
we want for the ``--foo`` field, isn't it?  So we then swap the names of the
fields (along with any documentation comments) while preserving their ``long``
and/or ``short`` attributes (which must now be given explicit values), so that
the field named ``foo``, now corresponding to the ``--no-foo`` option, will be
true when ``--foo`` is given last and also when no options are given.

Sample code:

.. code:: rust

    use clap::builder::ArgAction;
    use clap::Parser;

    #[derive(Debug, Parser)]
    struct Arguments {
        /// Don't foo any bars
        #[clap(long = "no-foo", action = ArgAction::SetFalse)]
        foo: bool,

        /// Foo all the bars [default]
        #[clap(long = "foo", overrides_with = "foo")]
        _no_foo: bool,
    }

    fn main() {
        for opts in [
            vec!["arg0"],
            vec!["arg0", "--foo"],
            vec!["arg0", "--no-foo"],
            vec!["arg0", "--no-foo", "--foo"],
            vec!["arg0", "--foo", "--no-foo"],
            vec!["arg0", "--no-foo", "--foo", "--no-foo"],
            vec!["arg0", "--foo", "--no-foo", "--foo"],
        ] {
            let args = Arguments::parse_from(&opts);
            println!("{opts:?} -> {args:?}");
        }
    }

`[Link to the code on the Rust Playground]`__

__ https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=07852c0f651919961b4653b10be521a2

Output::

    ["arg0"] -> Arguments { foo: true, _no_foo: false }
    ["arg0", "--foo"] -> Arguments { foo: true, _no_foo: true }
    ["arg0", "--no-foo"] -> Arguments { foo: false, _no_foo: false }
    ["arg0", "--no-foo", "--foo"] -> Arguments { foo: true, _no_foo: true }
    ["arg0", "--foo", "--no-foo"] -> Arguments { foo: false, _no_foo: false }
    ["arg0", "--no-foo", "--foo", "--no-foo"] -> Arguments { foo: false, _no_foo: false }
    ["arg0", "--foo", "--no-foo", "--foo"] -> Arguments { foo: true, _no_foo: true }
