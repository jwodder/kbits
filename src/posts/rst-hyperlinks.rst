=====================================
All About reStructuredText Hyperlinks
=====================================

:Date: 2020-07-28
:Category: Software
:Tags: markup, reStructuredText
:Summary:
    Writing the various hyperlink syntaxes in reStructuredText, along with
    internal hyperlinks and styling link text

reStructuredText_ offers a number of different ways to write hyperlinks, but
keeping track of all of them and their gotchas isn't easy, and the information
is scattered around the spec.  This document aims to summarize all of the
hyperlink-related information from the `reStructuredText Markup Specification`_
in one (hopefully) well-organized place.

This document describes reStructuredText hyperlinks as of Docutils_ version
0.16, the latest version at time of writing.

.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _reStructuredText Markup Specification:
   https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
.. _Docutils: https://docutils.sourceforge.io


.. contents::

Standalone Hyperlinks
=====================

Firstly, reStructuredText supports *standalone hyperlinks* — just a bare URI
(including a scheme) or e-mail address without any link text:

.. code:: rst

    Go to http://www.example.com to see something neat!

    E-mail me at me@example.com.

The above renders as:

    Go to http://www.example.com to see something neat!

    E-mail me at me@example.com.

Note that, unlike Markdown, angle brackets are not required around standalone
hyperlinks, and if you do include angle brackets, the brackets will be present
in the rendered output.

Also note that the scheme is required in order for a URI to be recognized as a
standalone hyperlink.  The domains names in the following will *not* be
converted to hyperlinks:

.. code:: rst

    Go to www.example.com — or to <www.example.org>!

If you want a hyperlink that links to ``www.example.com`` without a scheme and
uses the address as the link text, you can either write out the link the long
way as an `embedded URI hyperlink with link text <Embedded URI Hyperlinks_>`_,
or you can use embedded URI syntax without any link text, in which case the URI
becomes the link text.  For example:

.. code:: rst

    Go to `<www.example.com>`_.

renders as:

    Go to `<www.example.com>`_.

This isn't very useful for linking to domains, but it can be useful when you
want a link to a page in the same directory with the page filename used as the
link text:

.. code:: rst

    See `<other_page.html>`_ for other stuff.

Rendered:

    See `<other_page.html>`_ for other stuff.


Embedded URI Hyperlinks
=======================

If you want to create a hyperlink with link text, the most straightforward way
to do so is with the *embedded URI* syntax:

.. code:: rst

    Here is `a link <http://www.example.com>`_ to somewhere.

This renders as:

    Here is `a link <http://www.example.com>`_ to somewhere.

The syntax consists of a backtick, the link text (with any embedded backticks
escaped with backslashes), whitespace, the target URI or e-mail address inside
angle brackets, another backtick, and a single underscore.  If the URI ends
with an underscore, the underscore must be preceded by a backslash in order to
not be parsed as an `embedded alias`_.

Note that link text is treated literally rather than processed for any inline
markup.  See "`Styling Link Text`_" below for a way around this.

There is a gotcha you may run into when defining two embedded URI hyperlinks
with the same link text but different URIs; `see below for more information
<gotcha_>`_.


.. _embedded alias:

Embedded Alias Hyperlinks and Hyperlink Targets
===============================================

If the URI is lengthy, or if you want to link to the same location more than
once, you may want to use an *embedded alias*.  In this form, instead of
specifying the URI next to the link text, you specify a *hyperlink reference*
containing a *reference name*, and then you specify elsewhere (in a *hyperlink
target*) what URI the reference name points to.  For example:

.. code:: rst

    Here is `a link <link_target_>`_ to somewhere.

    .. _link_target: http://www.example.com

This syntax consists of two parts:

- At the location in the prose where you want the link to appear, write a
  backtick, the link text (with embedded backticks escaped), whitespace, a
  reference name followed by an underscore and encased in angle brackets,
  another backtick, and another underscore.

  - The reference name can be any sequence of characters, though if it contains
    any backticks or angle brackets, or begins or ends with space characters,
    the characters in question will need to be escaped with backslashes when
    using the name in an embedded alias link.

    When comparing two reference names for equality, runs of whitespace are
    normalized to a single space, and alphabetic characters are converted to
    lowercase.

.. _target:

- Elsewhere in the reStructuredText document (either before or after the
  hyperlink reference), write a *(external) hyperlink target* on a line of its
  own: optional whitespace, two periods, a space, an underscore, the same
  reference name as before (*without* the trailing underscore from before), a
  colon, whitespace, and then the URI or e-mail address that the link should
  point to.

  - If the reference name contains any colons or is just a single underscore,
    you must either escape the characters in question or else enclose the
    reference name in backticks (in which case any backticks in the reference
    name need to be escaped).  Either way, any leading or trailing space
    characters or backticks in the reference name need to be escaped as well.

  - If the URI contains any space characters or ends with an underscore, the
    characters in question will need to be escaped with backslashes.

    .. _multiline:

  - The reference name and the URI may be on the same line, or you can put them
    on separate lines, in which case the URI must be indented relative to the
    two periods and there must be no intervening blank lines.  The URI may even
    span multiple lines, in which case the lines are concatenated and any
    whitespace in the URI that isn't escaped is discarded.  For example, the
    following hyperlink targets all map to the same URI:

    .. code:: rst

        .. _one-liner: http://docutils.sourceforge.net/rst.html

        .. _starts-on-this-line: http://
           docutils.sourceforge.net/rst.html

        .. _entirely-below:
           http://docutils.
           sourceforge.net/rst.html

  - If the same reference name is used for two or more hyperlink targets with
    different URIs, a warning is produced, and the reference name will be
    unusable.

  - Hyperlink reference names, footnote labels, and citation labels share the
    same namespace.  This means you can link to a footnote or citation by its
    label, but it also means that you can't define a reference name that is the
    same as a footnote or citation label.

Once a reference name is defined in a hyperlink target, the same reference name
can be used in any number of embedded alias links to create multiple hyperlinks
to the same destination.

As with embedded URI hyperlinks, link text is treated literally rather than
processed for any inline markup.  See "`Styling Link Text`_" below for a way
around this.


.. _named hyperlink reference:

Named Hyperlink References
==========================

We can simplify embedded aliases one step further and use the link text as the
reference name.  Simply omit the part in angle brackets:

.. code:: rst

    Here is `a link`_ to somewhere.

    .. _a link: http://www.example.com

If the link text ends with text inside angle brackets, at least one of the
angle brackets needs to be escaped — or an escaped space character should be
added to the end of the link text — in order to prevent the link from being
parsed as an embedded URI or alias hyperlink.

.. _simple reference name:

This gets even simpler if the link text is a *simple reference name* — a single
word (no whitespace) consisting only of letters, numbers, hyphens, underscores,
periods, colons, and/or plus signs, with no punctuation at the beginning or
end, and with no occurrences of two or more punctuation characters in a row.  A
simple reference name can be written with just the trailing underscore, no
backticks:

.. code:: rst

    This following word_ is a hyperlink.

    .. _word: https://www.example.com

The same reference name may be used both as a named hyperlink reference and in
an embedded alias link:

.. code:: rst

    `This site`_ links to the same location as `these words <This site_>`_.

    .. _This site: https://www.example.com


.. _anon:

Anonymous Hyperlinks
====================

What if you want to use the hyperlink reference syntax, but it's for a URI that
will only be linked once, you don't feel like giving it a reference name, and
the link text is too long to use as an efficient reference name?  The solution:
*anonymous hyperlinks*.

.. code:: rst

    `This link`__ goes to a dot-com.  `This other link`__ goes to a dot-net.

    .. __: https://www.example.com
    __ https://www.example.net
 
Write the link text as a `named hyperlink reference`_, but instead of ending it
with one underscore, use two.  (As with named hyperlink references, the
backticks can be omitted for a `simple reference name`_.) Then, for the
`hyperlink target <target_>`_, use an underscore in place of the reference name
(so that you have two underscores in a row); alternatively, the entire
hyperlink target can be written as just two underscores, whitespace, and the
URI or e-mail address.

The first anonymous hyperlink in a document will link to the URI given by the
first anonymous hyperlink target, the second anonymous hyperlink will link to
the second anonymous target, etc.


Embedded URI Hyperlinks and Automatic Reference Names
=====================================================

Here's an interesting fact about `embedded URI hyperlinks`_: they're equivalent
to a `named hyperlink reference`_ using the link text as the reference name.
That means this:

.. code:: rst

    `This website <https://www.example.com>`_ is awesome!

is exactly equivalent to:

.. code:: rst

    `This website`_ is awesome!

    .. _This website: https://www.example.com

As a consequence of this, you can link to the same location as an embedded URI
link by using its link text as the reference name:

.. code:: rst

    I changed my mind; `this website <https://www.example.com>`_ sucks.  Let me
    reiterate: The website at `this link <this website_>`_ is nothing special.


.. _gotcha:

Gotcha: Duplicate Link Text
---------------------------

As stated above, if a reference name is associated with two different URIs,
rendering the document will produce a warning, and the reference name will be
unusable in hyperlinks.  So what happens if we define two embedded URI
hyperlinks with the same link text but different URIs, like so?

.. code:: rst

    See `here <https://www.example.com>`_ and `here <https://www.example.net>`_
    for more information.

With the above input, a warning will be produced, but the hyperlinks will still
point where you want them to, and the reference name ``here`` will refer to the
first URI.  This normally isn't all that bad, but if you're using a renderer
that fails on warnings — e.g., if you're uploading a project with a
reStructuredText README to the `Python Package Index <https://pypi.org>`_ — the
rendering will fail, and your upload to PyPI will either be rejected or end up
with an unrendered project description.

So how do we cleanly write embedded URI links with the same link text but
different URIs?  Answer: We add an extra underscore to the end of the link,
turning it into an `anonymous hyperlink <anon_>`_.

.. code:: rst

    See `here <https://www.example.com>`__ and `here
    <https://www.example.net>`__ for more information.

With two underscores, no hyperlink target is created, and so there is no
conflict.


Embedded Alias Hyperlinks and Automatic Reference Names
=======================================================

Similarly to embedded URI hyperlinks, using an `embedded alias hyperlink
<embedded alias_>`_ turns the link text into a reference name pointing at the
same location as the hyperlink reference.  The following markup defines four
hyperlinks that all point to <https://www.example.com>:

.. code:: rst

    See `this site <site_>`_ for more information.

    .. _site: https://www.example.com

    Now that I've written that link, I can write these links: `Click me! <this
    site_>`_  I link to `this site`_!  `Click me!`_

If you define multiple embedded alias hyperlinks with the same link text but
different hyperlink references, the document will render without any warnings,
and the link text will be usable as a reference name pointing to the same
location as the first hyperlink reference.


Intra-Document Links
====================

Linking to different parts of the same document is accomplished using `embedded
alias hyperlinks <embedded alias_>`_ and `named hyperlink references`_, just
like external links; the difference is in how the `hyperlink target <target_>`_
is defined.


Internal Hyperlink Targets
--------------------------

A hyperlink target without a URI creates an *internal hyperlink target* that
points to the next element in the document.

.. code:: rst

    Click `here <After Lorem_>`_ to skip the next paragraph.

    Lorem ipsum dolor sit amet …

    .. _After Lorem:

    This paragraph can be linked to with the reference name ``After Lorem``.
    Aren't you glad you didn't skip the previous paragraph now?

The target points to the next element even if the target is indented so as to
be "nested" at the end of an indented block.  This allows us to attach targets
to individual elements of a list:

.. code:: rst

    1. Any following lines that line up with "Any" belong to this list item.

       .. _item2:

    2. This list item can be linked to with the reference name ``item2``.

If the ``.. _item2:`` line above wasn't indented, it would split the list into
two lists, and the target would point to the second list.  (A target before a
list always points to the list as a whole; a target pointing to just the first
item is not possible.)


Named Directives
----------------

Most reStructuredText directives support a ``:name:`` option that takes a
string as an argument.  Setting this option allows you to link to the directive
using that name, equivalent to preceding the directive with an internal
hyperlink target.

.. code:: rst

    .. danger::
        :name: dont-or-whatever

        Don't stick your finger in the— You know what?  Forget it.  I'm not
        your mother.

    … Text passes …

    Hey, remember `that admonition from earlier <dont-or-whatever_>`_?  I was
    serious.

As this is the same as using an internal hyperlink target, a warning will be
generated if two directives have the same name or if the name of a directive is
the same as a reference name of another hyperlink target.


Inline Internal Targets
-----------------------

A phrase within a paragraph of text can be made into a target by preceding the
phrase with an underscore and a backtick, escaping any backticks inside the
phrase, and appending a backtick to the end of the phrase.  (The backticks
cannot be omitted, no matter how simple the phrase is.)  This defines the
phrase itself as a reference name that points to the phrase's location in the
document.

.. code:: rst

    They're called "paragraphs," but I've never seen them _`para`!  Know what I
    mean?

    (I don't know what I was saying `here <para_>`_.)


Implicit Hyperlink Targets for Section Titles
---------------------------------------------

A section title in a reStructuredText document implicitly defines a hyperlink
target pointing to that section with the same reference name as the section
title.

.. code:: rst
    
    Go read "`All About Eels`_" to learn about our wriggly friends!

    Didn't you hear me?  Who wouldn't want to click `this link <All About
    Eels_>`_?

    All About Eels
    ==============
    Did you know?  When you're bit in the heel by a big giant eel, that's a
    moray.

If a section has the same name as a hyperlink target or a directive, the
hyperlink target or directive takes precedence, and the section cannot be
linked to by name.  If two or more sections have the same name, none of them
can be linked to by name.  In order to link to a section that cannot be linked
by name, you must precede the section title with an internal hyperlink target
and link to that.


Chaining Hyperlink Targets
==========================

It's possible to define multiple hyperlink targets all pointing to the same
location by "chaining" the targets together, one after the other:

.. code:: rst

    .. _foo:
    .. _bar:
    .. _baz: https://www.example.com

    Now the reference names foo_, bar_, and baz_ all link to the same place.

Chained hyperlink targets all point to the same location as the last target in
the chain.  If the last target is an internal hyperlink target, the chained
targets will all point to the same document element as that last target:

.. code:: rst

    .. _foo:
    .. _bar:
    .. _baz:

    Now the reference names foo_, bar_, and baz_ all link to this paragraph.

.. _indirect hyperlink target:

Alternatively, a hyperlink target ``A`` can be defined to point to the same
location as another target ``B`` by defining the hyperlink target with ``B``
(as a named hyperlink reference) in place of the URI:

.. code:: rst

    .. _some link: https://www.example.com
    .. _foo: `some link`_

    Now `some link`_ and foo_ go to the same website.

The ``.. _foo:`` definition is called an *indirect hyperlink target*.  As with
named hyperlink references, the backticks can be dropped when the hyperlink
reference is a `simple reference name`_.  `As with external hyperlink targets
<multiline_>`_, the hyperlink reference may begin on the same or next line as
the target, and it may span multiple lines.


Styling Link Text
=================

As you may have noticed, inline markup in link text is treated literally rather
than being processed into emphasis etc.  For example, this:

.. code:: rst

    Try this recipe for `pie *à la mode* <https://www.example.com>`_.

renders as:

    Try this recipe for `pie *à la mode* <https://www.example.com>`_.

The asterisks are rendered as-is instead of causing the "à la mode" to be
emphasized.

Fortunately, there's a trick to use inline markup in link text: Define the link
using a substitution:

.. code:: rst

    Try this recipe for |pie à la mode|_.

    .. |pie à la mode| replace:: pie *à la mode*
    .. _pie à la mode: https://www.example.com

This works as follows:

- In our prose, we insert a *substitution reference* where we want the link to
  be.  A substitution reference consists of a vertical bar, some arbitrary
  substitution text, and another vertical bar.  Because we also want this to be
  a hyperlink, an underscore is added after the closing vertical bar, causing
  the substitution reference to also be a `named hyperlink reference`_ with the
  substitution text as the reference name.

  - The substitution text can be any text that does not begin or end with
    whitespace.  Substitution text is matched case-sensitively, but if that
    fails, a case-insensitive match is tried.

- Elsewhere in the document, a *substitution definition* is given for the
  substitution reference: two periods, a space, a vertical bar, the same
  substitution text as in the substitution reference, another vertical bar,
  whitespace, a ``replace::`` directive (without leading ``..``), whitespace,
  and then finally the inline markup to display in place of the substiution
  reference in the rendered document.

- Elsewhere in the document, a `hyperlink target <target_>`_ is created that
  maps the substitution text to the URI or e-mail address that the substituted
  text should link to.  To link to a location in the document rather than to an
  external URI, either use an `indirect hyperlink target`_:

  .. code:: rst

      Try this recipe for |pie à la mode|_.

      .. |pie à la mode| replace:: pie *à la mode*
      .. _pie à la mode: `pie recipe`_

      Some intervening text

      .. _pie recipe:

      So here's how you make pie *à la mode*: …

  or else make the substitution text the same as the reference name of the
  internal target:

  .. code:: rst

      Try this recipe for |pie recipe|_.

      .. |pie recipe| replace:: pie *à la mode*

      Some intervening text

      .. _pie recipe:

      So here's how you make pie *à la mode*: …

If desired, the substitution reference can be made into an `anonymous
hyperlink`_ instead by placing two underscores instead of one after the closing
vertical bar, in which case the hyperlink target must follow the anonymous
hyperlink target syntax.


Link Text within a Word
=======================

Normally, a hyperlink spans one or more full words, but what if we want to only
link part of a word?  To do so, we must insert a backslash (optionally followed
by a whitespace character) between the link and the rest of the word:

.. code:: rst

    These `link <https://www.example.com>`_\s are getting out of control!  Now
    they're in the in\ test_\ ines of our words.

    .. _test: https://www.example.net

This renders as:

    These `link <https://www.example.com>`_\s are getting out of control!  Now
    they're in the in\ test_\ ines of our words.

    .. _test: https://www.example.net
