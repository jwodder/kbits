======================================================
Converting Lists to Simple Tables and Back with ``rs``
======================================================

:Date: 2023-05-03
:Category: Software
:Tags: rs, tables, text processing, Unix utilities
:Summary:
    If you have a file that's just a list of items, one item per line, and you
    want to turn it into a simple table — one delimited just by whitespace
    without any border characters — how would you do that?  Follow up question:
    If you have a simple table, and you want to convert it into a list of
    items, one per line, how would you do *that*?  The answer to both questions
    is: with the ``rs`` command, and this article will show you how.

If you have a file that's just a list of items, one item per line, and you want
to turn it into a simple table — one delimited just by whitespace without any
border characters — how would you do that?  Follow up question: If you have a
simple table, and you want to convert it into a list of items, one per line,
how would you do *that*?  The answer to both questions is: with the ``rs``
command, and this article will show you how.

``rs`` is a Unix command-line program for **r**\ e\ **s**\ haping arrays of
data.  Most Linux users can get it by installing the ``rs`` package, and macOS
users will find it preinstalled.


Converting a List of Lines to a Simple Table
============================================

When ``rs`` is invoked without any options, it constructs a table from standard
input, treating each line as its own table entry, and fills in columns before
rows.  Thus, if we have the following file saved in ``lines.txt``::

    Dapper Drake
    Edgy Eft
    Feisty Fawn
    Gutsy Gibbon
    Hardy Heron
    Intrepid Ibex
    Jaunty Jackalope
    Karmic Koala
    Lucid Lynx
    Maverick Meerkat
    Natty Narwhal
    Oneiric Ocelot
    Precise Pangolin
    Quantal Quetzal
    Raring Ringtail
    Saucy Salamander
    Trusty Tahr
    Utopic Unicorn
    Vivid Vervet
    Wily Werewolf
    Xenial Xerus
    Yakkety Yak
    Zesty Zapus

Then running ``rs < lines.txt`` will produce the following output::

    Dapper Drake      Jaunty Jackalope  Precise Pangolin  Vivid Vervet
    Edgy Eft          Karmic Koala      Quantal Quetzal   Wily Werewolf
    Feisty Fawn       Lucid Lynx        Raring Ringtail   Xenial Xerus
    Gutsy Gibbon      Maverick Meerkat  Saucy Salamander  Yakkety Yak
    Hardy Heron       Natty Narwhal     Trusty Tahr       Zesty Zapus
    Intrepid Ibex     Oneiric Ocelot    Utopic Unicorn    

.. important::

    When ``rs`` is run without any arguments, it acts like it was given the
    ``-e`` (Read one table entry from each line of input) and ``-t`` (Fill in
    columns before rows) options.  If you specify any arguments of your own,
    then ``-e`` and ``-t`` will not be in effect unless you specify them
    explicitly.

``rs`` automatically determines the number of table columns based on what will
fit in an 80-character line.  To change the line length to, say, 60 characters,
pass ``-w60`` to the command (No space is allowed between the option and its
argument).  To ask for a specific number of table rows and let ``rs`` figure
out the number of columns, supply the desired number of rows as an argument,
e.g., ``rs -e -t 8 < lines.txt``.  To ask for a specific number of table
columns instead, pass a ``0`` argument (to tell ``rs`` "Figure the number of
rows out yourself") followed by the desired number of columns, e.g., ``rs -e -t
0 3 < lines.txt``.

By default, ``rs`` will output every column at the same width; in the example
above, this results in the first column having more padding on the right than
is strictly necessary.  The ``-z`` option will get rid of that padding; thus,
by running ``rs -e -t -z < lines.txt``, we get the following output::

    Dapper Drake   Jaunty Jackalope  Precise Pangolin  Vivid Vervet
    Edgy Eft       Karmic Koala      Quantal Quetzal   Wily Werewolf
    Feisty Fawn    Lucid Lynx        Raring Ringtail   Xenial Xerus
    Gutsy Gibbon   Maverick Meerkat  Saucy Salamander  Yakkety Yak
    Hardy Heron    Natty Narwhal     Trusty Tahr       Zesty Zapus
    Intrepid Ibex  Oneiric Ocelot    Utopic Unicorn    

One thing you might not have noticed about the output is that the last line,
having fewer columns than the others, ends in several spaces to make the end
line up with the start of the last column.  ``rs`` doesn't have an option to
disable this extra whitespace, but if you really want to get rid of it, you can
pipe the output through ``sed -e 's/ *$//'`` to strip all trailing spaces.

Lastly, if you want the rows of the table to be filled in before the columns,
invoke ``rs`` with the ``-e`` option and no ``-t`` option; thus, ``rs -e <
lines.txt`` gives us::

    Dapper Drake      Edgy Eft          Feisty Fawn       Gutsy Gibbon
    Hardy Heron       Intrepid Ibex     Jaunty Jackalope  Karmic Koala
    Lucid Lynx        Maverick Meerkat  Natty Narwhal     Oneiric Ocelot
    Precise Pangolin  Quantal Quetzal   Raring Ringtail   Saucy Salamander
    Trusty Tahr       Utopic Unicorn    Vivid Vervet      Wily Werewolf
    Xenial Xerus      Yakkety Yak       Zesty Zapus       


Converting a Simple Table to a List of Lines
============================================

Say we have the following text saved in ``table.txt``::

    Dapper Drake      Jaunty Jackalope  Precise Pangolin  Vivid Vervet
    Edgy Eft          Karmic Koala      Quantal Quetzal   Wily Werewolf
    Feisty Fawn       Lucid Lynx        Raring Ringtail   Xenial Xerus
    Gutsy Gibbon      Maverick Meerkat  Saucy Salamander  Yakkety Yak
    Hardy Heron       Natty Narwhal     Trusty Tahr       Zesty Zapus
    Intrepid Ibex     Oneiric Ocelot    Utopic Unicorn    Artful Aardvark

and we want to convert this into a list of table entries, one per line, column
by column (i.e., we want ``Intrepid Ibex`` to come before ``Jaunty Jackalope``
in the output).  Because the columns are separated by multiple spaces and the
table entries also contain spaces, we can't use ``rs`` by itself to accomplish
this.  Instead, we first use ``sed -e 's/ \{2,\}/\t/g'`` to convert runs of two
or more spaces to tab characters, and then ``rs`` can process the table using
tabs as the cell delimiter.

Next, we have to pipe the output of ``sed`` through two ``rs`` invocations: the
first invocation transposes the table so that the second invocation will split
its entries apart in the correct order (For whatever reason, ``rs`` can't do
all this in a single invocation).  The full command line will look like this::

    sed -e 's/ \{2,\}/\t/g' table.txt | rs -c -C -T | rs -c 0 1

(The ``-c`` and ``-C`` options tell ``rs`` to use a tab as the input and output
column delimiters, respectively.)

This works fine for the table above, but if the last column is short by two or
more columns, like so::

    Dapper Drake      Jaunty Jackalope  Precise Pangolin  Vivid Vervet
    Edgy Eft          Karmic Koala      Quantal Quetzal   Wily Werewolf
    Feisty Fawn       Lucid Lynx        Raring Ringtail   Xenial Xerus
    Gutsy Gibbon      Maverick Meerkat  Saucy Salamander  Yakkety Yak
    Hardy Heron       Natty Narwhal     Trusty Tahr       
    Intrepid Ibex     Oneiric Ocelot    Utopic Unicorn    

then ``rs`` will not do what we want by default.  When the ``rs -c -C -T`` step
goes to transpose its input, it finds that a direct transposition would result
in the last two columns of the output being short, which ``rs`` dislikes, and
so it decides to fix things by moving "Intrepid Ibex" (the next cell after
"Trusty Tahr") to the cell below "Trusty Tahr" and right of "Yakkety Yak" in
the output, producing this (with tabs converted to aligned spaces to make it
easier to read)::

    Dapper Drake      Edgy Eft          Feisty Fawn       Gutsy Gibbon      Hardy Heron       Oneiric Ocelot
    Jaunty Jackalope  Karmic Koala      Lucid Lynx        Maverick Meerkat  Natty Narwhal     Utopic Unicorn
    Precise Pangolin  Quantal Quetzal   Raring Ringtail   Saucy Salamander  Trusty Tahr       
    Vivid Vervet      Wily Werewolf     Xenial Xerus      Yakkety Yak       Intrepid Ibex     

and then when this table is flattened with ``rs -c 0 1``, the output will be in
the wrong order.

We can tell ``rs`` to not do this by passing the ``-n`` option to the ``rs -c
-C -T`` command, which will make it output an all-blank entry below "Trusty"
and right of "Yakkety" in the output instead of moving "Intrepid."  However,
this blank cell will result in the final ``rs -c 0 1`` command printing blank
lines at the end of the output; we can avoid this by stripping trailing tabs
before passing the table on.  Hence, the final command line, that works
regardless of how short the last column happens to be, is:

::

    sed -e 's/ \{2,\}/\t/g' table.txt | rs -c -C -T -n | sed -e 's/\t*$//' | rs -c 0 1

On the other hand, if the table we're converting to a list happens to be read
by going across the first row, then the second row, etc. — e.g., if it was
produced with ``rs -e`` without the ``-t`` option — instead of being read by
going down the first, second, etc. column, then the whole business with ``rs -c
-C -T -n`` and stripping trailing tabs is unnecessary, and we can turn this
table::

    Dapper Drake      Edgy Eft          Feisty Fawn       Gutsy Gibbon
    Hardy Heron       Intrepid Ibex     Jaunty Jackalope  Karmic Koala
    Lucid Lynx        Maverick Meerkat  Natty Narwhal     Oneiric Ocelot
    Precise Pangolin  Quantal Quetzal   Raring Ringtail   Saucy Salamander
    Trusty Tahr       Utopic Unicorn    Vivid Vervet      Wily Werewolf
    Xenial Xerus      Yakkety Yak       

into a list by just running::

    sed -e 's/ \{2,\}/\t/g' table.txt | rs -c 0 1
