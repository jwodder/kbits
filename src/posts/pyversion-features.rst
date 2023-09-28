==================================================
Notable Features Introduced in Each Python Version
==================================================

:Date: 2021-07-11
:Modified: 2023-09-28
:Category: Programming
:Tags: Python, history
:Summary:
    Notable features introduced in each major release of Python, from Python
    3.0 forwards

The following is a list of all of the notable or interesting (in my biased
opinion) features introduced in each major release of Python, starting with
Python 3.0.

.. contents::


Python 3.0 (2008-12-03), Relative to Python 2.6
===============================================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.0.html>`__

- ``print`` statement replaced with a ``print()`` function

- ``exec`` keyword replaced with an ``exec()`` function, which does not take a
  stream argument

- ``dict.keys()``, ``dict.items()`` and ``dict.values()`` now return "views"
  instead of lists

- ``dict.iterkeys()``, ``dict.iteritems()``, and ``dict.itervalues()`` removed

- ``map()`` now returns an iterator, stops when the shortest iterable is
  exhausted, and cannot take ``None`` as a function

- ``filter()`` now returns an iterator

- Python 2's ``xrange()`` is Python 3's ``range()``; Python 2's ``range()`` is
  no more

- Python 2's ``raw_input()`` is Python 3's ``input()``; Python 2's ``input()``
  is no more

- Python 2's ``long`` is Python 3's ``int``

  - The ``repr()`` of a (long) integer no longer includes a trailing ``L``

- Python 2's ``unichr`` is Python 3's ``chr``

- ``zip()`` now returns an interator

- Order comparison operators now raise ``TypeError`` when given operands of
  different types

- ``sorted()`` and ``list.sort()`` no longer accept the ``cmp`` parameter

- ``cmp()`` and ``__cmp__()`` removed

- Dividing two integers with ``/`` now returns a float

- ``sys`` module:

  - ``stdin``, ``stdout``, and ``stderr`` are now text streams
  - ``maxint``, ``exitfunc()``, ``exc_clear()``, ``exc_type``, ``exc_value``,
    and ``exc_traceback`` removed

- ``itertools`` module:

  - ``imap()``, ``ifilter()``, and ``izip()`` removed
  - ``ifilterfalse()`` renamed to ``filterfalse()``
  - ``izip_longest()`` renamed to ``zip_longest()``

- ``math`` module: ``ceil()`` and ``floor()`` now return integers

- ``array`` module:

  - ``array.read()`` and ``array.write()`` removed
  - ``c`` typecode removed

- ``operator`` module: ``sequenceIncludes()`` and ``isCallable()`` removed

- ``random`` module: ``jumpahead()`` API removed

- ``os`` module: ``tmpnam()``, ``tempnam()``, and ``tmpfile()`` removed

- ``string`` module: ``letters``, ``lowercase``, and ``uppercase`` removed

- ``__builtin__`` module renamed to ``builtins``

- Octal literals now use the prefix ``0o`` instead of just ``0``

- Python 2's ``str`` is Python 3's ``bytes``; Python 2's ``unicode`` is Python
  3's ``str``

- All string literals are now text/Unicode ``str``\s

- The ``u`` prefix for text string literals is no longer supported (later
  reintroduced in Python 3.3)

- Mixing byte strings and text strings now produces a ``TypeError``

- ``\uXXXX`` and ``\UXXXXXXXX`` escapes in raw string literals are now
  interpreted literally instead of being converted to Unicode characters

  - As a consequence of this, the ``ur`` string prefix is no longer supported

- ``basestring`` removed

- The ``repr()`` of a string now longer escapes non-ASCII characters

- The default Python source encoding is now UTF-8

- Non-ASCII letters are now allowed in identifiers

- ``StringIO`` and ``cStringIO`` removed; use ``io.StringIO`` and
  ``io.BytesIO`` instead

- Function arguments and return values can now be annotated

- Functions now have an ``__annotations__`` attribute

- Named parameters after ``*args`` or a bare ``*`` in a function signature are
  now keyword-only

- Keyword arguments are allowed after the list of base classes in a class
  definition

- New keyword: ``nonlocal``

- Extended iterable unpacking: Statements like ``a, b, *rest = some_sequence``
  are now supported

- Dictionary comprehensions added: ``{k: v for k, v in stuff}``

- Set literals and set comprehensions added: ``{1, 2}`` and ``{x for x in
  stuff}``

- New builtin functions: ``ascii()`` and ``next()``

- ``intern()`` moved to ``sys.intern()``

- Builtins ``apply()``, ``buffer()``, ``callable()`` (later reintroduced in
  Python 3.2), ``coerce()``, ``execfile()``, and ``file`` removed

- ``reduce()`` moved to ``functools.reduce()``

- ``reload()`` moved to ``imp.reload()``

- ``dict.has_key()`` removed

- ``round()``'s rounding strategy and return type changed

- ``True``, ``False``, and ``None`` are now reserved words

- The syntax for using a metaclass has changed from:

  .. code:: python

      class C:
          __metaclass__ = M
          ...

  to:

  .. code:: python

      class C(metaclass=M):
          ...

- Special method ``__prepare__`` on metaclasses added

- Module-global ``__metaclass__`` variable no longer supported

- List comprehensions of the form ``[... for var in item1, item2, ...]`` must
  now be written ``[... for var in (item1, item2, ...)]`` instead.

- The loop control variables of list comprehensions are no longer leaked into
  the surrounding scope

- ``...`` (the ellipsis) can now be used as an expression anywhere, and it can
  no longer be spelled ``. . .``

- Tuple unpacking in function parameters no longer supported

- Calling ``repr()`` via backticks no longer supported

- ``<>`` removed

- Trailing ``l`` or ``L`` on integer literals no longer supported

- ``from module import *`` is no longer allowed inside functions

- All module imports where the module name does not start with a period are now
  treated as absolute imports

- Classic classes removed; all classes are now new-style

- The following modules are removed: ``audiodev``, ``Bastion/rexec``,
  ``bsddb185``, ``bsddb3``, ``Canvas``, ``cfmfile``, ``cl``, ``commands``,
  ``compiler``, ``dircache``, ``dl``, ``fpformat``, ``gopherlib``, ``htmllib``,
  ``ihooks``, ``imageop``, ``imputil``, ``linuxaudiodev``, ``md5``, ``mhlib``,
  ``mimetools``, ``MimeWriter``, ``mimify``, ``multifile``, ``mutex``, ``new``,
  ``popen2``, ``posixfile``, ``pure``, ``rfc822``, ``sets``, ``sgmllib``,
  ``sha``, ``sre``, ``statvfs``, ``stringold``, ``sunaudio``, ``sv``,
  ``test.testall``, ``thread``, ``timing``, ``toaiff``, ``user``, ``UserDict``
  (moved to ``collections``), ``UserList`` (moved to ``collections``), and
  ``UserString`` (moved to ``collections``)

- All IRIX-specific, Mac-specific, and Solaris-specific modules removed

- ``_winreg`` module renamed to ``winreg``

- ``ConfigParser`` module renamed to ``configparser``

- ``copy_reg`` module renamed to ``copyreg``

- ``Queue`` module renamed to ``queue``

- ``SocketServer`` module renamed to ``socketserver``

- ``cPickle`` module renamed to ``_pickle``

- ``cProfile`` module renamed to ``_profile``

- ``repr`` module renamed to ``reprlib``

- ``test.test_support`` module renamed to ``test.support``

- The modules ``anydbm``, ``dbhash``, ``dbm``, ``dumbdm``, ``gdbm``, and
  ``whichdb`` have been combined into a new ``dbm`` module

- ``HTMLParser`` module renamed to ``html.parser``

- ``htmlentitydefs`` module renamed to ``html.entities``

- ``httplib`` module renamed to ``http.client``

- The modules ``BaseHTTPServer``, ``CGIHTTPServer``, and ``SimpleHTTPServer``
  have been combined into a new ``http.server`` module

- ``Cookie`` module renamed to ```http.cookies``

- ``cookielib`` module renamed to ``http.cookiejar``

- tkinter modules renamed as follows:

  ==============  ====================
  Old Name        New Name
  ==============  ====================
  Dialog          tkinter.dialog
  FileDialog      tkinter.filedialog
  FixTk           tkinter._fix
  ScrolledText    tkinter.scrolledtext
  SimpleDialog    tkinter.simpledialog
  Tix             tkinter.tix
  Tkconstants     tkinter.constants
  Tkdnd           tkinter.dnd
  Tkinter         tkinter.__init__
  tkColorChooser  tkinter.colorchooser
  tkCommonDialog  tkinter.commondialog
  tkFileDialog    tkinter.filedialog
  tkFont          tkinter.font
  tkMessageBox    tkinter.messagebox
  tkSimpleDialog  tkinter.simpledialog
  turtle          tkinter.turtle
  ==============  ====================

- ``urllib2`` module split into ``urllib.request`` and ``urllib.error`` modules

- ``urlparse`` module renamed to ``urllib.parse``

- ``urllib`` module split into ``urllib.parse``, ``urllib.request``, and
  ``urllib.error`` modules

- ``robotparser`` module renamed to ``urllib.robotparser``

- ``xmlrpclib`` module renamed to ``xmlrpc.client``

- The modules ``DocXMLRPCServer`` and ``SimpleXMLRPCServer`` have been combined
  into a new ``xmlrpc.server`` module

- Exceptions must now inherit from ``BaseException``

- ``StandardError`` removed

- Exceptions no longer behave like sequences; use the ``args`` attribute
  instead

- ``except exc, var`` is now written ``except exc as var``

- The variable used to catch an exception is now deleted when the ``except``
  block is left

- ``raise Exception, args`` is now written ``raise Exception(args)``

- Raising an exception inside an ``except`` or ``finally`` block now causes
  implicit exception chaining

- Explicit exception chaining can be done with ``raise SecondaryException()
  from primary_exception``

- ``__getslice__()``, ``__setslice__()``, and ``__delslice__()`` removed

- Special method ``next()`` renamed to ``__next__()``

- ``__oct__()`` and ``__hex__()`` removed

- Removed support for ``__members__`` and ``__methods__``

- Function attributes of the form ``func_X`` renamed to ``__X__``

- Special method ``__nonzero__()`` renamed to ``__bool__()``

- ``super()`` can now be invoked without arguments inside an instance method


Python 3.1 (2009-06-26)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.1.html>`__

- Multiple context managers can now be used in a single ``with`` statement

- Directories & zip archives containing a ``__main__.py`` can now be executed
  by passing their path to the interpreter

- Packages containing a ``__main__`` submodule can now be executed with
  ``python -m`` and ``runpy``

- New ``bytes`` and ``bytearray`` method: ``maketrans()``

- The ``repr()``\s of ``float``\s are now shorter

- New ``int`` method: ``bit_length()``

- The fields in strings formatted with ``str.format()`` can now omit numbering
  in order to be automatically numbered, as in ``'Sir {} of
  {}'.format('Gallahad', 'Camelot')``

- The format specification mini-language now includes a thousands separator
  specifier

- ``round(x, n)`` now returns an integer if ``x`` is an integer

- New modules: ``importlib`` and ``tkinter.ttk``

- ``collections`` module:

  - ``Counter`` and ``OrderedDict`` added
  - ``namedtuple()`` now accepts a ``rename`` parameter

- ``contextlib`` module: ``nested()`` is now deprecated

- ``decimal`` module: ``Decimal.from_float()`` added

- ``io`` module: ``SEEK_SET``, ``SEEK_CUR``, and ``SEEK_END`` added

- ``itertools`` module:

  - ``combinations_with_replacement()`` and ``compress()`` added
  - ``count()`` now accepts a ``step`` parameter

- ``json`` module: Decoders now accept an ``object_pairs_hook`` parameter

- ``logging`` module: ``NullHandler`` added

- ``re`` module: ``sub()``, ``subn()``, and ``split()`` now accept a ``flags``
  parameter

- ``string`` module: ``maketrans()`` is now deprecated


Python 3.2 (2011-02-20)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.2.html>`__

- New modules: ``argparse``, ``concurrent.futures``, ``html``, and
  ``sysconfig``

- ``.pyc`` files are now stored in ``__pycache__/`` directories

- Modules now have a ``__cached__`` attribute

- New ``str`` method: ``format_map()``

- The ``str()`` of a ``float`` or ``complex`` is now the same as its ``repr()``

- New ``range`` methods: ``index()`` and ``count()``

- ``callable()`` function from Python 2 restored

- ``ResourceWarning`` warning type added

- ``abc`` module: ``abstractclassmethod()`` and ``abstractstaticmethod()``
  added

- ``ast`` module: ``literal_eval()`` now supports ``set`` & ``bytes`` literals

- ``collections`` module:

  - ``Counter.subtract()`` added
  - ``OrderedDict.move_to_end()`` added
  - ``deque.count()`` and ``deque.reverse()`` added

- ``compileall`` command-line interface: ``-i`` and ``-b`` options added

- ``configparser`` module:

  - ``ConfigParser`` class replaced with ``SafeConfigParser``, which is now
    customizable
  - New API added based on the mapping protocol

- ``contextlib`` module:

  - ``ContextDecorator`` added
  - ``nested()`` removed

- ``csv`` module:

  - ``unix_dialect`` dialect (dialect name ``"unix"``) added
  - ``DictWriter.writeheader()`` added

- ``datetime`` module:

  - ``timezone`` added
  - ``timedelta`` instances can now be multiplied by ``float``\s and divided by
    ``float``\s & ``int``\s
  - ``date.strftime()`` now supports years from 1000 through 9999

- ``decimal`` module:

  - The ``Decimal`` constructor now accepts ``float``\s
  - ``Decimal`` instances can now be compared with ``float`` and
    ``fractions.Fraction`` instances
  - ``Context.clamp`` added

- ``email.parser`` module: ``BytesFeedParser``, ``BytesParser``,
  ``message_from_bytes()`` and ``message_from_binary_file()`` added

- ``email.generator`` module: ``BytesGenerator`` added

- ``fractions`` module: The ``Fraction`` constructor now accepts ``float``\s
  and ``decimal.Decimal``\s

- ``functools`` module: ``cmp_to_key()``, ``lru_cache()``, and
  ``total_ordering()`` added

- ``gzip`` module: ``compress()`` and ``decompress()`` added

- ``hashlib`` module: ``algorithms_available`` and ``algorithms_guaranteed``
  added

- Various ABCs added to ``importlib.abc``

- ``inspect`` module: ``getgeneratorstate()`` and ``getattr_static()`` added

- ``io`` module: ``BytesIO.getbuffer()`` added

- ``itertools`` module: ``accumulate()`` added

- ``json`` module: The ``indent`` parameter to ``dumps()`` etc. can now be a
  string

- ``logging`` module:

  - ``basicConfig()`` now accepts a ``style`` parameter
  - If a logging event occurs before any explicit configuration is set up, a
    default configuration (available in ``lastResort``) is now enabled
  - Python callables returning booleans can now be used as filters

- ``logging.config`` module: ``dictConfig()`` added

- ``math`` module: ``isfinite()``, ``expm1()``, ``erf()``, ``erfc()``,
  ``gamma()``, and ``lgamma()`` added

- ``os`` module: ``fsencode()``, ``fsdecode()``, ``supports_bytes_environ``,
  ``getenvb()``, and ``environb`` added

- ``shutil`` module:

  - ``copytree()`` now accepts ``ignore_dangling_symlinks`` and
    ``copy_function`` parameters
  - ``make_archive()``, ``unpack_archive()``, etc. added

- ``site`` module: ``getsitepackage()``, ``getuserbase()``, and
  ``getusersitepackages()`` added

- ``smtplib`` module: ``SMTP.send_message()`` added

- ``ssl`` module:

  - ``SSLContext`` and ``match_hostname()`` added
  - Server Name Indication (SNI) is now supported when linked against recent
    versions of OpenSSL

- ``string`` module: ``maketrans()`` removed

- ``sys`` module: ``hash_info`` added

- ``tarfile`` module: ``TarFile.add()`` now accepts a ``filter`` parameter, and
  the ``exclude`` parameter is now deprecated

- ``tempfile`` module: ``TemporaryDirectory`` added

- ``threading`` module: ``Barrier`` added

- ``unicodedata`` updated to Unicode 6.0.0

- ``urllib.parse`` module: ``urlparse()`` now supports IPv6 addresses


Python 3.3 (2012-09-29)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.3.html>`__

- New modules: ``faulthandler``, ``ipaddress``, ``lzma``, ``unittest.mock``,
  and ``venv``

- Support for implicit namespace packages (directories without an
  ``__init__.py``) added

- All Unicode codepoints, from U+0000 to U+10FFFF, are now always supported;
  there is no longer a distinction between "narrow" and "wide" builds

- Multiple exception types have been merged into ``OSError``, which now has
  various subclasses for common error conditions

- Delegating to a subgenerator/subiterator with ``yield from`` is now possible

- Chained exception context can be suppressed with ``raise e from None``

- The ``u"unicode"`` syntax for Unicode strings from Python 2 is now supported
  again

- Functions & classes now have a ``__qualname__`` attribute

- ``inspect`` module: ``signature()``, ``Signature``, ``Parameter``, and
  ``BoundArguments`` added

- ``sys`` module: ``implementation`` added

- ``types`` module: ``SimpleNamespace`` added

- ``importlib`` module: Various classes & functions added

- Modules now have a ``__loader__`` attribute

- ``"\N{...}"`` can now take name aliases

- ``unicodedata`` updated to UCD 6.1.0

- New ``list`` and ``bytearray`` methods: ``copy()`` and ``clear()``

- Raw bytes literals can now be written ``rb"..."`` in addition to ``br"..."``

- ``open()`` now accepts an ``opener`` parameter

- ``print()`` now accepts a ``flush`` parameter

- Hash randomization with ``hash()`` is now enabled by default

- New ``str`` method: ``casefold()``

- ``abc``:

  - It is now possible to combine ``abstractmethod`` with ``property``,
    ``classmethod``, or ``staticmethod``
  - ``abstractproperty``, ``abstractclassmethod``, and ``abstractstaticmethod``
    are now deprecated
  - ``ABCMeta.register()`` can now be used as a class decorator

- ``array`` module: ``long long`` type now supported

- ``base64`` module: Decoding functions now accept ASCII-only ``str``\s

- ``binascii`` module: The ``a2b_*`` functions now accept ASCII-only ``str``\s

- ``bz2`` module:

  - ``open()`` added
  - ``BZ2File()`` now accepts arbitrary file-like objects and implements most
    of the ``io.BufferedIOBase`` API

- ``collections`` module:

  - ``ChainMap`` added
  - ABCs moved to ``collections.abc``; aliases are still present in
    ``collections`` itself, but importing them is deprecated
  - ``Counter`` now supports ``+``, ``-``, ``+=``, ``-=``, ``|=``, and ``&=``

- ``contextlib`` module: ``ExitStack`` added

- ``datetime`` module: New ``datetime`` methods: ``timestamp()``,
  ``strftime()``, and ``astimezone()``

- ``email`` module: Policy framework added

- ``email.parser`` module: ``BytesHeaderParser`` added

- ``email.utils`` module: ``format_datetime()``, ``parsedate_to_datetime()``,
  and ``localtime()`` added

- ``functools`` module: ``lru_cache()`` now accepts a ``typed`` parameter

- ``hmac`` module: ``compare_digest()`` added

- ``http.client`` module: ``HTTPResponse.readinto()`` added

- ``html.parser`` module: ``HTMLParser`` can now parse broken markup without
  errors

- ``html.entities``: ``html5`` added

- ``inspect`` module: ``getclosurevars()`` and ``getgeneratorlocals()`` added

- ``io`` module:

  - ``x`` mode added to ``open()`` function
  - The ``TextIOWrapper`` constructor now accepts a ``write_through`` parameter

- ``itertools`` module: ``accumulate()`` now accepts a ``func`` parameter

- ``logging`` module: ``basicConfig()`` now accepts a ``handlers`` parameter

- ``math`` module: ``log2()`` added

- ``multiprocessing`` module:

  - The ``Process`` constructor now accepts a ``daemon`` parameter
  - ``Process.sentinel`` added

- ``multiprocessing.connection`` module: ``wait()`` added

- ``multiprocessing.pool`` module: New ``Pool`` methods ``starmap()`` and
  ``starmap_async()`` added

- ``os`` module:

  - ``fwalk()``, ``pipe2()``, ``sendfile()``, ``getpriority()``,
    ``setpriority()``, ``replace()``, ``get_terminal_size()``, ``getxattr()``,
    ``listxattr()``, ``removexattr()``, ``setxatter()``, ``sync()``, and others
    added
  - Various functions now accept ``dir_fd`` and/or ``follow_symlinks``
    parameters
  - Various functions can now take file descriptors as path arguments
  - ``stat()``, ``fstat()``, ``lstat()``, and ``utime()`` now support
    timestamps with nanosecond precision

- ``re`` module: ``str`` regular expressions now support ``\uXXXX`` and
  ``\UXXXXXXXX`` escapes

- ``pipes.quote()`` moved to ``shlex``

- ``shutil`` module:

  - ``disk_usage()``, ``chown()``, and ``get_terminal_size()`` added
  - Several functions now accept a ``symlink`` parameter

- ``stat`` module: ``filemode()`` added

- ``struct`` module: ``size_t`` and ``ssize_t`` now supported

- ``subprocess``:

  - Command strings can now be bytes on POSIX
  - ``DEVNULL`` added

- ``sys`` module: ``thread_info`` added

- ``textwrap`` module: ``indent()`` added

- ``time`` module: ``get_clock_info()``, ``monotonic()``, ``perf_counter()``,
  ``process_time()``, ``clock_getres()``, ``clock_gettime()``,
  ``clock_settime()``, and ``CLOCK_*`` constants added

- ``types`` module: ``MappingProxyType``, ``new_class()``, and
  ``prepare_class()`` added

- ``urllib.request`` module: The ``Request`` constructor now accepts a
  ``method`` parameter

- ``array`` module: The ``u`` format is now deprecated


Python 3.4 (2014-03-17)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.4.html>`__

- New modules: ``asyncio``, ``ensurepip``, ``enum``, ``pathlib``,
  ``selectors``, ``statistics``, and ``tracemalloc``

- ``codecs`` module: ``encode()`` and ``decode()`` are now documented

- ``unicodedata`` updated to UCD 6.3

- ``min()`` and ``max()`` now accept a ``default`` parameter

- New special method: ``__length_hint__()``

- ``abc`` module: ``ABC`` and ``get_cache_token()`` added

- ``argparse`` module: ``FileType`` now accepts ``encoding`` and ``errors``
  parameters

- ``base64`` module:

  - Encoding & decoding functions now accept any bytes-like object
  - ``a85encode()``, ``a85decode()``, ``b85encode()``, and ``b85decode()``
    added

- ``contextlib`` module: ``suppress()`` and ``redirect_stdout()`` added

- ``doctest`` command-line interface: ``-o`` and ``-f`` options added

- ``email`` module:

  - ``as_string()`` now accepts a ``policy`` argument
  - ``as_bytes()`` method added
  - ``EmailMessage`` and ``MIMEPart`` added as part of new API
  - ``contextmanager`` submodule added

- ``filecmp`` module: ``clear_cache()`` and ``DEFAULT_IGNORES`` added

- ``functools`` module: ``partialmethod()`` and ``singledispatch()`` added

- ``glob`` module: ``escape()`` added

- ``hashlib`` module: ``pbkdf2_hmac()`` added

- ``html`` module: ``unescape()`` added

- ``html.parser`` module: ``HTMLParser`` constructor now accepts a
  ``convert_charrefs`` parameter, and the ``strict`` argument is now deprecated

- ``http.server`` command-line interface: ``--bind`` option added

- ``imp.reload()`` moved to ``importlib``

- ``importlib`` module: ``InspectLoader.source_to_code()`` added

- ``importlib.util`` module: ``MAGIC_NUMBER``, ``cache_from_source()``,
  ``source_from_cache()``, and ``decode_source()`` added

- ``importlib.machinery`` module: ``ExtensionFileLoader.get_filename()`` added

- ``runpy`` and ``python -m`` can now be used with namespace packages

- ``inspect`` module:

  - Command-line interface added
  - ``unwrap()`` added

- ``ipaddress`` module: ``is_global`` property added

- ``json`` module: ``dumps()`` etc. will now automatically set ``separators``
  to ``(",", ": ")`` when ``indent`` is non-``None``

- ``multiprocessing`` module:

  - Start methods ``spawn`` and ``forkserver`` added
  - Contexts added
  - ``get_all_start_methods()``, ``get_start_method()``,
    ``set_start_method()``, and ``get_context()`` added

- ``operator`` module: ``length_hint()`` added

- ``os`` module:

  - ``cpu_count()`` added
  - ``open()`` now supports the ``O_PATH`` and ``O_TMPFILE`` flags

- ``pdb`` module: ``print`` command removed

- ``pickle`` module: Protocol 4 added

- ``plistlib`` module: ``load()``, ``dump()``, ``loads()``, and ``dumps()``
  added

- ``pprint`` module: ``PrettyPrinter``, ``pformat()``, and ``pprint()`` now
  accept a ``compact`` parameter

- ``re`` module: ``fullmatch()`` and ``regex.fullmatch()`` added

- ``resource`` module: ``prlimit()`` added

- ``shutil`` module: ``copyfile()`` now raises a ``SameFileError`` when the
  source and destination are the same file

- ``ssl`` module:

  - ``create_default_context()`` and ``get_default_verify_paths()`` added
  - New ``SSLContext`` methods: ``cert_store_stats()``, ``get_ca_certs()``, and
    ``load_default_certs()``

- ``stat`` module: ``S_IFDOOR``, ``S_IFPORT``, and ``S_IFWHT`` added

- ``struct`` module: ``iter_unpack()`` and ``Struct.iter_unpack()`` added

- ``subprocess`` module:

  - ``check_output()`` now accepts an ``input`` parameter

- ``sys`` module: ``getallocatedblocks()`` and ``__interactivehook__`` added

- ``tarfile`` module: Command-line interface added

- ``textwrap`` module:

  - The ``TextWrapper`` constructor now accepts ``max_lines`` and
    ``placeholder`` parameters
  - ``shorten()`` added

- ``threading`` module: ``main_thread()`` added

- ``traceback`` module: ``clear_frames()`` added

- ``types`` module: ``DynamicClassAttribute()`` added

- ``urllib.request`` module:

  - ``data:`` URLs now supported
  - ``Request`` objects are now reusable

- ``urllib.error`` module: ``HTTPError.headers`` added

- ``venv`` module: The ``EnvBuilder`` constructor and ``create()`` now accept a
  ``with_pip`` parameter

- ``importlib`` module: A number of methods & functions are deprecated

- The ``imp`` module is now deprecated and will be removed in Python 3.12

- The ``formatter`` module is now deprecated and will be removed in Python 3.10

- The ``U`` mode of various "open" functions is now deprecated and will be
  removed in Python 3.11


Python 3.5 (2015-09-13)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.5.html>`__

- Coroutine functions (``async def``), awaitable objects (``await`` and
  ``__await__()``), asynchronous iteration (``async for``, ``__aiter__()``, and
  ``__anext__()``), and asynchronous context managers (``async with``,
  ``__aenter__()``, and ``__aexit__()``) added

- ``@`` operator (with ``__matmul__()`` etc. special methods) for matrix
  multiplication added

- Multiple ``*`` and/or ``**`` unpackings can now be used in a single function
  call

- Tuple, list, set, & dictionary displays may now contain ``*`` or ``**``
  unpackings (as appropriate)

- Percent-formatting of ``bytes`` and ``bytearray`` objects with ``%`` added

- New modules: ``typing`` and ``zipapp``

- System calls are now retried when interrupted by a signal

- ``from __future__ import generator_stop`` added to cause ``StopIteration``
  exceptions raised inside generators to be transformed into
  ``RuntimeException``\s, which becomes the default in Python 3.7

  - Without the ``__future__`` import, such exceptions generate
    ``PendingDeprecationWarning``\s.

- ``RecursionError`` exception type (a subclass of ``RuntimeError``) added

- ``.pyo`` files eliminated; optimized bytecode is now stored in ``.pyc`` files
  with ``opt-`` tags in their name

- ``"namereplace"`` error handler added

- Various additions & improvements to the ``asyncio`` module

- ``cmath`` module: ``isclose()`` added

- ``collections`` module:

  - New ``deque`` methods: ``index()``, ``insert()``, and ``copy()``
  - ``deque`` now supports ``+`` and ``*``

- ``collections.abc`` module: ``Generator``, ``Awaitable``, ``Coroutine``,
  ``AsyncIterator``, and ``AsyncIterable`` added

- ``configparser`` module: ``ConfigParser`` can now take a dictionary of
  converters, and subclasses can define additional converters as methods

- ``contextlib`` module: ``redirect_stderr()`` added

- ``enum`` module: The ``Enum`` callable now accepts a ``start`` parameter

- ``glob`` module: ``glob()`` and ``iglob()` now support the ``**`` pattern

- ``http`` module: ``HTTPStatus`` added

- ``importlib.util`` module: ``module_from_spec()`` added

- ``inspect`` module:

  - ``BoundArguments.apply_defaults()`` added
  - ``Signature.from_callable()`` added
  - ``signature()`` now accepts a ``follow_wrapped`` parameter
  - ``iscoroutine()``, ``iscoroutinefunction()``, ``isawaitable()``,
    ``getcoroutinelocals()``, and ``getcoroutinestate()`` added

- ``io`` module: new ``BufferedIOBase`` method: ``readinto1()``

- ``ipaddress`` module:

  - The ``IPv4Network`` and ``IPv6Network`` constructors now accept an
    ``(address, netmask)`` argument
  - New ``IPv4Network`` and ``IPv6Network`` attribute: ``reverse_pointer``

- ``json`` module: JSON decoding errors now raise ``JSONDecodeError``

- ``json.tool`` command-line interface: The input order of keys is now
  preserved on output; the ``--sort-keys`` option will sort the keys instead

- ``linecache`` module: ``lazycache()`` added

- ``locale`` module: ``delocalize()`` added

- ``logging`` module: Logging methods now accept exception instances as
  ``exc_info`` arguments

- ``math`` module: ``isclose()``, ``gcd()``, ``inf``, and ``nan`` added

- ``fractions`` module: ``gcd()`` is now deprecated and will be removed in
  Python 3.9

- ``operator`` module: ``matmul()`` and ``imatmul()`` added

- ``os`` module: ``scandir()`` added

- ``os.path`` module: ``commonpath()`` added

- ``pathlib`` module:

  - New ``Path`` methods: ``samefile()``, ``expanduser()``, ``write_text()``,
    ``read_text()``, ``write_bytes()``, and ``read_bytes()``
  - Class method ``Path.home()`` added
  - ``Path.mkdir()`` now accepts an ``exist_ok`` parameter

- ``readline`` module: ``append_history_file()`` added

- ``selectors`` module: ``DevpollSelector`` added

- ``shutil`` module: ``move()`` now accepts a ``copy_function`` argument

- ``signal`` module: ``SIG*`` contants have been converted to enums

- ``socket`` module: ``socket.sendfile()`` added

- ``ssl`` module: ``SSLObject`` added

- ``subprocess``: ``run()`` added

- ``sys`` module: ``set_coroutine_wrapper()``, ``get_coroutine_wrapper()``, and
  ``is_finalizing()`` added

- ``time`` module: ``monotonic()`` is now always available

- ``timeit`` command-line interface: ``--unit`` option added

- ``traceback`` module: ``TracebackException``, ``StackSummary``,
  ``FrameSummary``, ``walk_stack()``, and ``walk_tb()`` added

- ``types`` module: ``CoroutineType`` and ``coroutine()`` added

- ``unicodedata`` updated to Unicode 8.0.0

- ``unittest`` command-line interface: ``--locals`` option added

- ``unittest.mock`` module: ``Mock.assert_not_called()`` added

- ``urllib.request`` module: ``HTTPPasswordMgrWithPriorAuth`` added

- ``platform`` module: ``dist()`` and ``linux_distribution()`` are now
  deprecated

- ``html.parser`` module: The ``convert_charrefs`` parameter to the
  ``HTMLParser`` constructor now defaults to ``True``


Python 3.6 (2016-12-23)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.6.html>`__

- Formatted string literals ("f-strings")

- Variables can now be annotated by following the name of the variable with a
  colon and the annotation

- Underscores can now be used in numeric literals

- ``await`` and ``yield`` can now be used in the same function, thereby
  enabling asynchronous generators

- ``async for`` can now be used in list, set, & dict comprehensions and in
  generator expressions

- ``await`` expressions can now be used in any comprehension

- Special methods ``__init_subclass__()`` and ``__set_name__()`` added

- ``os.PathLike``, the ``__fspath__()`` method, and ``os.fspath()`` added

  - Relevant file functions now accept ``os.PathLike`` objects

- ``ModuleNotFoundError`` exception type (a subclass of ``ImportError``) added

- ``datetime`` module:

  - ``fold`` attribute added to ``datetime`` and ``time`` for denoting the
    second instance of a time duplicated due to DST
  - The ``strftime()`` method of ``date`` and ``datetime`` now supports ``%G``,
    ``%u``, and ``%V``
  - ``datetime.astimezone()`` can now be called on naïve instances

- The file system and console encodings on Windows are now both UTF-8

- A class's ``__dict__`` now preserves the order in which the attributes were
  defined

- ``**kwargs`` now preserves insertion order

- ``dict``\s are now implemented in such a way that they preserve insertion
  order

- New module: ``secrets``

- Various additions & improvements to the ``asyncio`` module

- ``cmath`` module: ``tau``, ``inf``, ``nan``, ``infj``, and ``nanj`` added

- ``collections.abc``: ``Collection``, ``Reversible``, and ``AsyncGenerator``
  added

- ``enum`` module: ``auto``, ``Flag``, and ``IntFlag`` added

- ``json`` module: ``load()`` and ``loads()`` now support binary input in
  UTF-8, UTF-16, and UTF-32

- ``math`` module: ``tau`` added

- ``random`` module: ``choices()`` added

- ``re`` module:

  - Modifier spans (e.g., as in ``'(?i)g(?-i:v)r'``) are now supported in
    regular expressions
  - Match objects can now be indexed to access groups

- ``statistics`` module: ``harmonic_mean()`` added

- The ``smtpd`` module is now deprecated and will be removed in Python 3.12

- ``subprocess`` module:

  - ``encoding`` and ``errors`` arguments added to ``Popen`` and the wrappers
    around it
  - The ``args`` parameter to ``Popen`` and the wrappers around it can now be a
    path-like object or sequence of path-like objects on POSIX systems

- ``time`` module: The ``tm_gmtoff`` and ``tm_zone`` attributes of
  ``struct_time`` are now available on all platforms

- ``typing`` module:

  - Generic type aliases like ``Dict[str, Tuple[S, T]]`` are now supported
  - ``TYPE_CHECKING`` added
  - ``ClassVar`` added
  - ``NewType()`` added
  - ``NamedTuple`` now supports variable annotation syntax

- ``unittest.mock`` module: New ``Mock`` methods ``assert_called()`` and
  ``assert_called_once()`` added

- ``venv`` command-line interface: ``--prompt`` option added

- Using ``async`` or ``await`` as a name will now generate a
  ``DeprecationWarning``

- ``StopIteration`` exceptions raised inside generators now generate
  ``DeprecationWarnings``

- Invalid escape sequences now generate a ``DeprecationWarning``

- The ``asynchat`` and ``asyncore`` modules are now deprecated and will be
  removed in Python 3.12

- The ``pyvenv`` script for creating venvs is now deprecated and will be
  removed in Python 3.8

- ``unicodedata`` updated to Unicode 9.0.0


Python 3.7 (2018-06-27)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.7.html>`__

- ``from __future__ import annotations`` added to enable postponed evaluation
  of annotations

- ``dict``\s are now guaranteed to preserve insertion order

- ``async`` and ``await`` are now reserved keywords

- New modules: ``contextvars``, ``dataclasses``, ``importlib.resources``

- New builtin function: ``breakpoint()``

- The interpreter now coerces ASCII locales to UTF-8 under certain
  circumstances on non-Windows OSes

- ``__aiter__()`` methods can no longer be asynchronous

- ``__getattr__()`` and ``__dir__()`` can now be defined on modules

- ``time`` module: variants of the timer functions added that return a number
  of nanoseconds as an integer

- Special methods ``__class_getitem__()`` and ``__mro_entries__()`` added

- Python Development Mode added

- New ``str``, ``bytes``, and ``bytearray`` method: ``isascii()``

- ``argparse`` module: ``ArgumentParser.parser_intermixed_args()`` added

- Various additions & improvements to the ``asyncio`` module

  - ``asyncio.run()`` added

- ``collections`` module: ``defaults`` argument added to ``namedtuple()``

- ``contextlib`` module: ``nullcontext()``, ``asynccontextmanager()``, and
  ``AsyncExitStack`` added

- ``datetime`` module:

  - ``datetime.fromisoformat()`` added
  - The ``"%z"`` format of the ``strptime()`` methods now accepts timezone
    offsets containing colons as well as a timezone specifier of "``Z``".

- ``enum`` module: Support for the ``_ignore_`` class property added to
  ``Enum``

- ``functools`` module: ``singledispatch()`` now recognizes type annotations

- ``http.server`` command-line interface: ``--directory`` option added

- ``ipaddress`` module: ``subnet_of()`` and ``supernet_of()`` methods added to
  ``IPv4Network`` and ``IPv6Network``

- ``locale`` module: ``format()`` is now deprecated and will be removed in
  Python 3.12

- ``math`` module: ``remainder()`` added

- ``pathlib`` module: ``Path.is_mount()`` added

- ``queue`` module: ``SimpleQueue`` added

- ``subprocess`` module:

  - ``capture_output`` argument added to ``run()``
  - ``text`` argument added to ``run()`` and the ``Popen`` constructor

- Removed the ``fpectl`` module

- ``StopIteration`` exceptions raised inside coroutines and generators are now
  transformed into ``RuntimeException``\s

- ``unicodedata`` updated to Unicode 11


Python 3.8 (2019-10-14)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.8.html>`__

- Assignment expressions: ``:=`` (the "walrus operator") can now be used to
  assign a value to a variable in the middle of an expression, e.g.:

  .. code:: python

      if m := re.search(r'\d+', s):
          x = int(m.group())

- Function parameters can now be made positional-only by placing a ``/`` after
  them in the argument list

- One can now write ``f"{var=}"`` to get ``f"{var}={repr(var)}"``

- ``continue`` is now allowed in ``finally:`` clauses

- New ``int``, ``bool``, and ``fractions.Fraction`` method:
  ``as_integer_ratio()``

- ``\N{name}`` escapes are now allowed in regular expressions

- ``dict``\s and dictviews can now be passed to ``reversed()``

- Generalized iterable unpacking in ``yield`` and ``return`` statements no
  longer requires parentheses; e.g., one can now write ``return foo, *bar``
  instead of having to do ``return (foo, *bar)``

- Missing commas between tuples in a list now generate a ``SyntaxWarning`` with
  a suggestion as to what went wrong

- For integer arguments, the three-argument form of ``pow()`` can now take a
  negative exponent when the base is coprime to the modulus, in which case the
  modular multiplicative inverse (or a power thereof) is calculated

- New modules: ``importlib.metadata`` and ``multiprocessing.shared_memory``

- Running ``python -m asyncio`` now starts an async REPL

- ``asyncio`` module:

  - ``CancelledError`` now inherits directly from ``BaseException`` instead of
    ``Exception``
  - ``coroutine()`` is now deprecated and will be removed in Python 3.11
  - Passing a ``loop`` parameter is now deprecated for most of ``asyncio``'s
    high-level API; it will be removed entirely in Python 3.10
  - Explicitly passing coroutines to ``wait()`` is now deprecated

- ``datetime`` module: New ``date`` and ``datetime`` method:
  ``fromisocalendar()``

- ``functools`` module: ``cached_property()`` and ``singledispatchmethod()``
  added

- ``io`` module: ``open_code()`` (the verified open hook) added

- ``itertools`` module: ``accumulate()`` now accepts an ``initial`` parameter

- ``json.tool`` command-line interface: ``--json-lines`` option added

- ``math`` module:

  - ``comb()`` added
  - ``dist()`` added
  - ``hypot()`` can now take multiple arguments
  - ``isqrt()`` added
  - ``perm()`` added
  - ``prod()`` added

- ``pathlib`` module:

  - ``Path.link_to()`` added
  - ``Path.rename()`` and ``Path.replace()`` now return the new path
  - ``Path.unlink()`` now accepts a ``missing_ok`` argument

- ``pickle`` module: Protocol 5 (with support for out-of-band buffers) added

- ``platform`` module: ``dist()`` and ``linux_distribution()`` removed

- ``shlex`` module: ``join()`` added

- ``statistics`` module: ``NormalDist``, ``fmean()``, ``geometric_mean()``,
  ``multimode()``, and ``quantiles()`` added

- ``subprocess`` module: The ``args`` parameter to ``Popen`` and the wrappers
  around it can now be a path-like object or sequence of path-like objects on
  Windows systems in addition to POSIX

- ``sys`` module:

  - ``audit()`` and ``addaudithook()`` (for audit hooks) added
  - ``pycache_prefix`` added
  - ``unraisablehook()`` and ``__unraisablehook__`` added

- ``typing`` module: ``TypedDict``, ``Literal``, ``Final``, ``final()``,
  ``Protocol``, ``SupportsIndex``, ``get_origin()``, and ``get_args()`` added

- ``unicodedata`` module:

  - Updated to Unicode 12.1.0
  - ``is_normalized()`` added

- ``unittest.mock`` module:

  - ``AsyncMock`` added
  - ``call`` objects now have ``args`` and ``kwargs`` properties

- ``zipfile`` module: ``Path`` added

- Removed:

  - ``macpath`` module (deprecated since Python 3.7)
  - ``time.clock()`` (deprecated since Python 3.3)
  - the ``pyvenv`` script for creating venvs (Use ``pythonX.Y -m venv``
    instead)
  - ``sys.set_coroutine_wrapper()`` and ``sys.get_coroutine_wrapper()``
    (deprecated since Python 3.7)

- Using ``is`` or ``is not`` with strings, numbers, and certain other literals
  now produces a ``SyntaxWarning``


Python 3.9 (2020-10-05)
=======================

Release notes: `[link] <https://docs.python.org/3/whatsnew/3.9.html>`__

- ``dict``\s can now be merged & updated using the ``|`` and ``|=`` operators

- Any valid expression can now be used as a decorator

- New ``str``, ``bytes``, and ``bytearray`` methods: ``removeprefix()`` and
  ``removesuffix()``

- Built-in collection types like ``list`` and ``dict`` can now be used as
  generic types; e.g., ``List[str]`` can now be written ``list[str]``

  - This also applies to collections ABCs; e.g., ``typing.Sequence[str]`` can
    now be written ``collections.abc.Sequence[str]``.

  - Importing the old ``List``, ``Sequence``, etc. types from ``typing`` is now
    deprecated but does not generate ``DeprecationWarnings``\s at this time.
    The deprecated names will be removed from ``typing`` in the first Python
    release five years after 3.9.

- New modules: ``graphlib`` and ``zoneinfo``

- ``asyncio`` module: ``to_thread()`` added

- ``functools`` module: ``cache()`` added

- ``importlib.resources`` module: ``files()`` added (introduced in
  ``importlib-resources`` v1.1.0)

- Aligned ``importlib.metadata`` with ``importlib-metadata`` v1.6.1

- ``ipaddress`` module now supports IPv6 scoped addresses

- ``math`` module:

  - ``gcd()`` can now take multiple arguments
  - ``lcm()``, ``nextafter()``, and ``ulp()`` added

- ``pathlib`` module:

  - ``Path.readlink()`` added
  - ``PurePath.is_relative_to()`` added
  - ``PurePath.with_stem()`` added

- ``random`` module: ``randbytes()`` added

- ``typing`` module: ``Annotated`` added

- The ``binhex``, ``parser``, and ``symbol`` modules are now deprecated

- Using ``NotImplemented`` in a boolean context is now deprecated and will
  produce a ``TypeError`` in a future version of Python

- Removed:

  - ``fractions.gcd()`` (deprecated since Python 3.5)
  - ``encoding`` parameter of ``json.loads()`` (deprecated & ignored since
    Python 3.1)
  - ``asyncio.Task.current_task()`` and ``asyncio.Task.all_tasks()``
    (deprecated since Python 3.7); use ``asyncio.current_task()`` and
    ``asyncio.all_tasks()`` instead

- ``with (await asyncio.lock):`` and ``with (yield from asyncio.lock):``
  statements are no longer supported; use ``async with lock`` instead.
  Likewise for ``asyncio.Condition`` and ``asyncio.Semaphore``.

- ``lib2to3`` now emits a ``PendingDeprecationWarning`` and will be removed in
  Python 3.13

- ``unicodedata`` updated to Unicode 13.0.0


Python 3.10 (2021-10-04)
========================

Release notes: `[link] <https://docs.python.org/3.10/whatsnew/3.10.html>`__

- Pattern matching!

  .. code:: python

      match status:
          case 400:
              return "Bad request"
          case 401 | 403 | 404:
              return "Not allowed"
          case _:
              return "Something's wrong with the Internet"

- Context managers in ``with`` statements can now be enclosed in parentheses,
  e.g.:

  .. code:: python

      with (CtxManager1() as example,
            CtxManager2()):

- Assignment expressions can now be used unparenthesized within set literals,
  set comprehensions, and sequence indexes (but not slices)

- Numeric literals immediately followed by keywords (e.g., ``0in x``) now
  generate a deprecation warning.  Future Python versions will change this to a
  syntax warning and then a syntax error.

- Common syntax errors now have better error messages

- ``AttributeError`` and ``NameError`` error messages now include suggestions
  as to what you might have meant

- ``Union[X, Y]`` can now be written ``X | Y``

- Dictionary views returned by ``dict.keys()``, ``dict.values()``, and
  ``dict.items()`` now have ``mapping`` attributes wrapping the original
  ``dict``

- The second argument of ``isinstance()`` and ``issubclass()`` can now be a
  ``Union``

- New ``int`` method: ``bit_count()``

- ``open()`` and friends can now be passed ``encoding="locale"`` in order to
  explicitly use the current locale's encoding

- ``zip()`` now has a ``strict`` parameter for requiring that all input
  iterables have the same length

- New builtin functions: ``aiter()`` and ``anext()``

- ``EncodingWarning`` warning type added

- The ``loop`` parameter (deprecated in Python 3.8) is now removed from most of
  ``asyncio``'s high-level API

- ``base64`` module: ``b32hexencode()`` and ``b32hexdecode()`` added

- ``bisect`` module: The functions now accept a ``key`` argument

- ``codecs`` module: ``unregister()`` added

- Collections ABCs can no longer be imported from ``collections``; import them
  from ``collections.abc`` instead

- ``collections`` module: ``Counter.total()`` added

- ``contextlib``: ``aclosing()`` added

- ``dataclasses``:

  - The ``dataclass`` decorator now accepts a ``slots`` argument
  - Fields can now be made keyword-only

- ``distutils`` is now deprecated and will be removed in Python 3.12

- ``glob`` module: ``glob()`` and ``iglob()`` now accept ``root_dir`` and
  ``dir_fd`` arguments

- Aligned ``importlib.metadata`` with ``importlib-metadata`` v4.6

  - ``entry_points()`` and ``package_distributions()`` added

- ``inspect`` module: ``get_annotations()`` added

- ``io`` module: ``text_encoding()`` added

- ``itertools`` module: ``pairwise()`` added

- ``os.path.realpath()`` now has a ``strict`` parameter for erroring when a
  path doesn't exist or a symlink loop is encountered

- ``pathlib`` module:

  - Slice and negative indexing support added to ``Path.parents``
  - ``Path.hardlink_to()`` added, superseding ``Path.link_to()``, which is now
    deprecated and will be removed in Python 3.12
  - ``Path.stat()`` and ``Path.chmod()`` now have a ``follow_symlinks``
    argument

- ``platform`` module: ``freedesktop_os_release()`` added

- ``statistics`` module: ``covariance()``, ``correlation()``, and
  ``linear_regression()`` added

- ``sys`` module: ``orig_argv`` and ``stdlib_module_names`` added

- ``traceback`` module: ``format_exception()``, ``format_exception_only()``,
  and ``print_exception()`` can now take just an exception argument as a
  positional-only parameter

- ``types`` module: ``EllipsisType``, ``NoneType``, and
  ``NotImplementedType`` added

- ``typing`` module: ``Concatenate``, ``ParamSpec``, ``TypeAlias``,
  ``TypeGuard``, and ``is_typeddict()`` added

- Removed the ``formatter`` and ``parser`` modules (deprecated in Python 3.4
  and 3.9, respectively)


Python 3.11 (2022-10-03)
========================

Release notes: `[link] <https://docs.python.org/3.11/whatsnew/3.11.html>`__

- Exception groups

  - ``ExceptionGroup`` and ``BaseExceptionGroup`` exception types added
  - ``try: ... except* ...: ...`` syntax (note asterisk) for matching exception
    groups

- Traceback messages now highlight the exact expression that caused the error

- Starred expressions can now be used in ``for`` statements (e.g., ``for x in
  *lst1, *lst2:``)

  - This was enabled by the grammar rewrite in Python 3.9 but was not noticed
    or documented until 3.11.

- Octal escapes in string & bytes literals with values greater than 0o377
  (e.g., ``\477``) now generate a ``DeprecationWarning``

- The various "open" functions no longer accept the ``U`` mode

- New ``object`` method: ``__getstate__()``

- New ``BaseException`` method: ``add_note()``

- Chaining ``@classmethod`` decorators and using them to wrap other decorators
  (such as ``@property``) is now deprecated and will be removed in Python 3.13

- Format specification mini-language: A ``z`` option can now be used with
  floating-point types in order to coerce negative zero to "regular" zero after
  rounding.

- New modules: ``tomllib`` and ``wsgiref.types``

- ``asyncio`` module:

  - ``@coroutine`` (deprecated since 3.8) and
    ``asyncio.coroutines.CoroWrapper`` removed
  - ``Barrier``, ``Runner``, ``TaskGroup``, and ``timeout()`` added

- ``binascii`` module: ``a2b_hqx()``, ``b2a_hqx()``, ``rlecode_hqx()``, and
  ``rledecode_hqx()`` removed

- ``binhex`` module removed

- ``contextlib`` module: ``chdir()`` added

- ``datetime`` module:

  - ``UTC`` added
  - The ``fromisoformat()`` methods now accept most ISO 8601 strings

- ``enum`` module:

  - ``EnumCheck``, ``FlagBoundary``, ``ReprEnum``, ``StrEnum``,
    ``@global_enum()``, ``@member()``, ``@nonmember()``, ``@property``,
    ``show_flag_values()``, and ``@verify`` added
  - ``EnumMeta`` renamed to ``EnumType``; the old name is currently as an alias

- ``functools`` module: ``singledispatch`` now supports union types

- ``hashlib`` module: ``file_digest()`` added

- ``inspect`` module:

  - ``getmembers_static()`` and ``ismethodwrapper()`` added
  - ``formatargspec()`` and ``getargspec()`` removed
  - Frame-related functions now return objects instead of tuples (though the
    new objects are backwards-compatible with the tuple interface)

- ``locale`` module:

  - ``getdefaultlocale()`` is now deprecated and will be removed in Python 3.13
  - ``getencoding()`` added

- ``logging`` module:

  - ``getLevelNamesMapping()`` added
  - ``createSocket()`` method added to ``logging.handlers.SysLogHandler``

- ``math`` module: ``cbrt()`` and ``exp2()`` added

- ``operator`` module: ``call()`` added

- ``pathlib`` module: The ``glob()`` and ``rglob()`` methods now return only
  directories if given a pattern ending with the pathname separator

- ``re`` module:

  - ``(?>...)``, ``*+``, ``++``, ``?+``, and ``{m,n}+`` can now be used in
    regular expressions
  - ``NOFLAG`` added

- ``string`` module: ``get_identifiers()`` and ``is_valid()`` methods added to
  ``string.Template``

- ``sys`` module: ``exception()`` added

- ``typing`` module:

  - ``LiteralString``, ``Never``, ``Self``, ``TypeVarTuple``, ``Unpack``,
    ``assert_never()``, ``assert_type()``, ``clear_overloads()``,
    ``get_overloads()``, ``@dataclass_transform``, and ``reveal_type()`` added
  - ``Text`` is now deprecated
  - Individual fields in a ``TypedDict`` may now be annotated as ``Required``
    or ``NotRequired``
  - The keyword-argument syntax for constructing ``TypedDict`` types is now
    deprecated and will be removed in Python 3.13

- ``unicodedata`` updated to Unicode 14.0.0

- ``zipfile`` module:

  - ``metadata_encoding`` argument added to ``ZipFile`` constructor
  - ``ZipFile.mkdir()`` added
  - ``stem``, ``suffix``, and ``suffixes`` attributes added to ``zipfile.Path``

- The following modules are now deprecated and are planned to be removed in
  Python 3.13: ``aifc``, ``audioop``, ``cgi``, ``cgitb``, ``chunk``, ``crypt``,
  ``imghdr``, ``mailcap``, ``msilib``, ``nis``, ``nntplib``, ``ossaudiodev``,
  ``pipes``, ``sndhdr``, ``spwd``, ``sunau``, ``telnetlib``, ``uu``, and
  ``xdrlib``


Python 3.12 (2023-10-02)
========================

Release notes: `[link] <https://docs.python.org/3.12/whatsnew/3.12.html>`__

- New syntax for type-annotating generic classes, generic functions, and type
  aliases:

  - Generic class:

    - Old syntax:

      .. code:: python

        from typing import Generic, TypeVar

        T_str = TypeVar("T_str", covariant=True, bound=str)

        class ClassA(Generic[T_str]):
            def method1(self) -> T_str:
                ...

    - New syntax:

      .. code:: python

        # No Generic or TypeVar

        class ClassA[T: str]:
            def method1(self) -> T:
                ...

  - Generic function:

    - Old syntax:

      .. code:: python

        from typing import TypeVar

        T = TypeVar("T")

        def func(a: T, b: T) -> T:
            ...

    - New syntax:

      .. code:: python

        # No TypeVar

        def func[T](a: T, b: T) -> T:
            ...

  - Type alias:

    - Old syntax:

      .. code:: python

        from typing import TypeAlias

        IntOrStr: TypeAlias = int | str

    - New syntax:

      .. code:: python

        type IntOrStr = int | str

  - Generic type alias:

    - Old syntax:

      .. code:: python

        from typing import TypeAlias

        T = TypeVar("T")

        ListOrSet: TypeAlias = list[T] | set[T]

    - New syntax:

      .. code:: python

        # No TypeVar

        type ListOrSet[T] = list[T] | set[T]

  - Variadic type alias:

    - Old syntax:

      .. code:: python

        from typing import TypeAlias, TypeVarTuple

        Ts = TypeVarTuple("Ts")

        IntEtc: TypeAlias = tuple[int, *Ts]

    - New syntax:

      .. code:: python

        type IntEtc[*Ts] = tuple[int, *Ts]

  - Type alias with a parameter spec:

    - Old syntax:

      .. code:: python

        from collections.abc import Callable
        from typing import ParamSpec, TypeAlias

        P = ParamSpec("P")

        IntMaker: TypeAlias = Callable[P, int]

    - New syntax:

      .. code:: python

        from collections.abc import Callable

        type IntMaker[**P] = Callable[P, int]

- Types of individual fields in a ``**kwargs`` function parameter can now be
  annotated with ``typing.Unpack`` applied to a ``TypedDict``, like so:

  .. code:: python

    from typing import TypedDict, Unpack

    class Movie(TypedDict):
        name: str
        year: int

    def foo(**kwargs: Unpack[Movie]):
        # kwargs["name"] must be passed a `str`, and kwargs["year"] must be
        # passed an `int`.
        ...

- ``{..}`` placeholders inside f-strings may now contain any valid Python
  expression

  - Quotes from the enclosing string may now be reused:

    .. code:: pycon

        >>> songs = ['Take me back to Eden', 'Alkaline', 'Ascensionism']
        >>> f"This is the playlist: {", ".join(songs)}"
        'This is the playlist: Take me back to Eden, Alkaline, Ascensionism'

  - Expressions inside f-strings may now span multiple lines and contain inline
    comments.

  - Expressions inside f-strings may now contain backslashes.

- The buffer protocol is now accessible in Python code:

  - Special methods ``__buffer__()`` and ``__release_buffer__()`` added
  - ``collections.abc`` module: ``Buffer`` added
  - ``inspect`` module: ``BufferFlags`` added

- Source code containing NUL bytes now results in a ``SyntaxError``

- Invalid escape sequences now generate a ``SyntaxWarning``

- Octal escapes in string & bytes literals with values greater than 0o377
  (e.g., ``\477``) now generate a ``SyntaxWarning``

- Applying ``~`` (bitwise inversion) to a ``bool`` is now deprecated and will
  become an error in Python 3.14.

- Removed modules:

  - ``asynchat`` (deprecated in Python 3.6)
  - ``asyncore`` (deprecated in Python 3.6)
  - ``distutils`` (deprecated in Python 3.10)
  - ``imp`` (deprecated in Python 3.4)
  - ``smtpd`` (deprecated in Python 3.6)

- ``array`` module: The ``array`` class is now subscriptable and thus properly
  generic

- ``ast`` module: Accessing or using any of ``Bytes``, ``Ellipsis``,
  ``NameConstant``, ``Num``, and ``Str`` now generates a
  ``DeprecationWarning``.  They are planned to be removed in Python 3.14.

- ``asyncio`` module:

  - ``as_completed()`` and ``wait()`` now accept generators yielding tasks
  - ``create_eager_task_factory()`` and ``eager_task_factory()`` added
  - ``run()`` now takes an optional ``loop_factory`` parameter

- ``calendar`` module: ``Day`` and ``Month`` added

- ``collections.abc`` module: ``ByteString`` is now deprecated and will be
  removed in Python 3.14

- ``configparser`` module: ``ConfigParser.readfp()``,
  ``ParsingError.filename``, and ``SafeConfigParser`` removed (deprecated in
  Python 3.2)

- ``datetime`` module: ``datetime.utcnow()`` and ``datetime.utctimestamp()``
  are now deprecated

- ``fraction`` module: ``Fraction`` instances now support float-style
  formatting

- ``importlib.abc`` module: ``ResourceReader``, ``Traversable``, and
  ``TraversableResources`` are now deprecated and will be removed in Python
  3.14

- ``importlib.resources``: ``as_file()`` now supports resource directories

- ``inspect`` module: ``getasyncgenlocals()``, ``getasyncgenstate()``, and
  ``markcoroutinefunction()`` added

- ``itertools``: ``batched()`` added

- ``locale`` module: ``format()`` removed (deprecated in Python 3.7)

- ``math`` module:

  - ``nextafter()`` now takes an optional ``steps`` parameter
  - ``sumprod()`` added

- ``os`` module:

  - ``DirEntry.is_junction()`` added
  - ``listdrives()``, ``listmounts()``, ``listvolumes()``, ``pidfd_open()``,
    ``setns()``, and ``unshare()`` added
  - Calling ``fork()`` or ``forkpty()`` in a multithreaded program now
    generates a ``DeprecationWarning``

- ``os.path`` module: ``isjunction()`` and ``splitroot()`` added

- ``pathlib`` module:

  - Path classes can now be subclassed
  - ``PurePath.with_segments()`` added
  - ``Path.is_junction()`` and ``Path.walk()`` added
  - ``PurePath.match()``, ``Path.glob()``, and ``Path.rglob()`` now take an
    optional ``case_sensitive`` parameter
  - ``PurePath.relative_to()`` now takes an optional ``walk_up`` parameter

- ``pkgutil`` module: ``find_loader()`` and ``get_loader()`` are now deprecated
  and will be removed in Python 3.14

- ``random`` module:

  - ``binomialvariate()`` added
  - The ``lambd`` argument to ``expovariate()`` now defaults to ``1.0``

- ``shutil`` module:

  - ``rmtree()`` now takes an optional ``onexc`` parameter.  The ``onerror``
    parameter is deprecated and will be removed in Python 3.14.
  - ``unpack_archive()`` now takes an optional ``filter`` parameter for
    limiting what gets extracted from tar archives

- ``sqlite3`` module:

  - Command-line interface added
  - ``connect()`` now takes an optional ``autocommit`` parameter
  - ``Connection.autocommit``, ``Connection.getconfig()``, and
    ``Connection.setconfig()`` added
  - The default adapters and converters are now deprecated

- ``ssl`` module: ``match_hostname()`` and ``wrap_socket()`` removed
  (deprecated in Python 3.7)

- ``statistics`` module: ``correlation()`` now takes an optional ``method``
  parameter that can be either ``"linear"`` (the default) or ``"ranked"``

- ``sys`` module:

  - ``activate_stack_trampoline()``, ``deactivate_stack_trampoline()``,
    ``is_stack_trampoline_active()``, and ``last_exc`` added
  - ``last_type``, ``last_value``, and ``last_traceback`` are now deprecated

- ``sys.monitoring`` added

- ``tarfile`` module: The ``TarFile.extract()`` and ``TarFile.extractall()``
  methods now take an optional ``filter`` parameter for limiting what
  gets extracted in order to avoid security issues.  Calling one of these
  methods without setting a filter will generate a ``DeprecationWarning`` until
  Python 3.14, in which the default filter will become ``"data"``.

- ``tempfile`` module:

  - ``NamedTemporaryFile`` now takes an optional ``delete_on_close`` parameter
  - ``mkdtemp()`` now always returns an absolute path

- ``types`` module: ``get_original_bases()`` added

- ``typing`` module:

  - ``override`` added
  - ``dataclass_transform()`` now takes an optional ``frozen_default``
    parameter
  - ``Hashable`` and ``Sized`` are now deprecated

- ``unicodedata`` updated to Unicode 15.0.0

- ``unittest`` command-line interface: ``--durations`` option added

- ``uuid`` module: Command-line interface added

- ``venv`` module: ``setuptools`` is no longer automatically installed in
  virtual environments
