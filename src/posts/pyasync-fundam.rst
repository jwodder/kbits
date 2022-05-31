============================================
Python Asynchronous Programming Fundamentals
============================================

:Date: 2022-05-29
:Modified: 2022-05-30
:Category: Programming
:Tags: Python, async
:Summary:
    Python introduced asynchronous programming capabilities in version 3.4 in
    2014, with further notable improvements in almost every minor version
    since.  However, to many Python programmers, this area of the language
    remains esoteric, misunderstood, and underutilized.  This article aims to
    elucidate the fundamental concepts of asynchronous programming as part of
    the first step towards mastery.

Python introduced asynchronous programming capabilities in version 3.4 in 2014,
with further notable improvements in almost every minor version since.
However, to many Python programmers, this area of the language remains
esoteric, misunderstood, and underutilized.  This article aims to elucidate the
fundamental concepts of asynchronous programming as part of the first step
towards mastery.

There won't be many code samples in this article, but reading it should make it
easier to grok `the asyncio documentation`__ and figure out how to piece things
together.

__ https://docs.python.org/3/library/asyncio.html

.. contents::

High-Level Overview
===================

Asynchronous programming provides a way to interleave execution of multiple
functions (coroutines_) at once; at any given point, only one of the functions
is actually doing operations, while the others are waiting for things like
blocking I/O to complete (or, if the I/O has already completed, they're waiting
for the current coroutine to be suspended so that they get a chance to resume).

.. note::

    In the Python standard library and all third-party async libraries that I
    am aware of, the kinds of low-level operations that one can ultimately
    suspend execution waiting for are almost exclusively I/O-related.  If
    you're seeking to add concurrency to CPU-bound code (e.g., anything
    involving number crunching), you are likely to be better off using
    multiprocessing instead.

Specifically, whenever execution of a currently-running coroutine reaches an
``await`` expression, the coroutine may be suspended, and another
previously-suspended coroutine may resume execution if what it was suspended on
has since returned a value.  Suspension can also happen when an ``async for``
block requests the next value from an asynchronous iterator or when an ``async
with`` block is entered or exited, as these operations use ``await`` under the
hood.

Note that, although multiple coroutines can be processed at once, effectively
finishing in any order, operations within a single coroutine continue to be
executed in the order they're written.  For example, given the following code:

.. code:: python

    async def f():
        ...

    async def g():
        ...

    async def amain():
        await f()
        await g()

    asyncio.run(amain())

When ``await f()`` is reached, ``amain()`` will be suspended until ``f()`` is
finished, and only after that will execution proceed to the next line, starting
coroutine ``g()``.  If you want to execute ``f()`` and ``g()`` concurrently,
you need to use |asyncio.create_task|_, |asyncio.gather|_, or similar.  See
`this article <hynek_>`_ for more details.

.. |asyncio.create_task| replace:: ``asyncio.create_task()``
.. _asyncio.create_task:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task

.. |asyncio.gather| replace:: ``asyncio.gather()``
.. _asyncio.gather:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.gather

.. _hynek: https://hynek.me/articles/waiting-in-asyncio/

In general, coroutines can only be called or scheduled by other coroutines.  To
run a "top-level" coroutine from inside synchronous code (i.e., either inside a
non-coroutine function or at module level), the simplest & preferred way is to
use the |asyncio.run|_ function introduced in Python 3.7.  Code meant to run on
older Pythons must use the lower-level |loop.run_until_complete|_ instead,
along with other loop methods for cleanup.

.. |asyncio.run| replace:: ``asyncio.run()``
.. _asyncio.run: https://docs.python.org/3/library/asyncio-task.html#asyncio.run

.. |loop.run_until_complete| replace:: ``loop.run_until_complete()``
.. _loop.run_until_complete:
   https://docs.python.org/3/library/asyncio-eventloop.html
   #asyncio.loop.run_until_complete


Definitions
===========

*Asynchronous programming* features the execution of multiple tasks
concurrently, with one task being run while waiting for others to complete.
Asynchronous programming in Python is an example of *cooperative multitasking*
[wiki__], as it requires the running coroutines to cooperate and yield control
on their own; if the current coroutine goes for a long time without calling
``await``, execution will remain on that coroutine all the while, and all other
coroutines in the thread will remain in a suspended state.  This is contrast to
the *preemptive multitasking* [wiki__] of multithreaded and multiprocess
programs, where the Python interpreter or OS scheduler decides on its own when
to switch between running contexts, with the points at which switches can occur
being difficult or impossible to predict in general.

__ https://en.wikipedia.org/wiki/Cooperative_multitasking
__ https://en.wikipedia.org/wiki/Preemption_(computing)

.. _coroutines:

A *coroutine function* is a function defined with ``async def`` instead of just
``def``.  (In the context of asynchronous programming, a function defined with
just ``def`` is called a *synchronous function*.)  Only coroutine functions can
contain ``await``, ``async for``, and ``async with`` constructs, and, as of
Python 3.10, they cannot contain ``yield from`` constructs.

- Note that just calling a coroutine function does not cause it to start
  running; you need to either schedule it for concurrent execution with
  |asyncio.create_task|_ or similar or else ``await`` on it directly.

A *coroutine object* is the result of calling a coroutine function.  This is
not the value ``return``\ed (or ``raise``\d) by the function; rather, it is a
pending computation that can be suspended & resumed at any point that the
coroutine function uses ``await``, ``async for``, or ``async with``.  The
actual ``return`` value or exception is obtained either by awaiting on the
coroutine object (possibly wrapped in a task and/or something like
|asyncio.gather|_) from within another coroutine function or by running it as a
"top-level" entry point using ``asyncio.run()`` within synchronous code.

- Asynchronous generators — coroutine functions that use ``yield`` — are a bit
  of an exception.  You do not ``await`` the result of the function; instead,
  you iterate through it using either ``async for ... in ...:`` or ``await
  anext(...)``.

- Confusingly, both coroutine functions and coroutine objects can be referred
  to as just "coroutines."

The actual scheduling of coroutine execution is managed by an *event loop*.  An
event loop is created by |asyncio.run|_ or ``asyncio.new_event_loop()``, handed
one or more coroutines and/or synchronous callbacks, and then set off to run
either forever or until completion of a "top-level" coroutine.  It's the event
loop's job to execute the current coroutine until it suspends on an ``await``,
after which it looks to see if any suspended coroutines are now done with their
suspension and either picks one to resume or, if none are ready, waits until
one is.

.. _awaitable:

An *awaitable* is any value that the ``await`` keyword can be applied to; this
includes coroutine objects, futures, future-likes, and tasks (see below).
Awaiting on an awaitable causes the current coroutine to be suspended until the
awaitable is ready to provide a value or raise an exception.

A *future* (class |asyncio.Future|_) is a low-level container for the result of
a computation (a value or exception) that starts out empty and is assigned a
value or exception later.  Awaiting on a future will suspend the current
coroutine until something else either stores a result in the future or cancels
it.

- You may already be familiar with futures in the form of the ``Future`` class
  from the |concurrent.futures|_ module, which provides access to the results
  of operations evaluated in other threads or processes.  The
  |asyncio.Future|_ class is similar in spirit, but has a different API.

.. |asyncio.Future| replace:: ``asyncio.Future``
.. _asyncio.Future:
   https://docs.python.org/3/library/asyncio-future.html#asyncio.Future

.. |concurrent.futures| replace:: ``concurrent.futures``
.. _concurrent.futures:
   https://docs.python.org/3/library/concurrent.futures.html

A *future-like* is an object with an ``__await__()`` method, which must return
an iterator.  Awaiting on a future-like causes the current coroutine to be
suspended until the iterator is exhausted, at which point the ``value``
attribute of the terminating ``StopIteration`` exception is returned as the
result of the ``await`` expression.

A *task* (class |asyncio.Task|_) represents a running coroutine.  Creating a
task from a coroutine object with |asyncio.create_task|_ will cause the
coroutine to be scheduled for execution concurrently with other running
coroutines.  The task instance can later be awaited on to suspend the current
coroutine until the wrapped coroutine finishes executing, returning its result.

.. |asyncio.Task| replace:: ``asyncio.Task``
.. _asyncio.Task:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.Task

A running task can be *cancelled* by calling its |Task.cancel|_ method.  This
will cause the underlying coroutine to receive an ``asyncio.CancelledError``
exception the next time it ``await``\s, likely putting an end to the task's
execution.

.. |Task.cancel| replace:: ``Task.cancel()``
.. _Task.cancel:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancel


Syntax
======

Asynchronous programming in Python takes place inside coroutines_, functions
defined using ``async def`` instead of just ``def``.  Within a coroutine, the
``await`` keyword can be applied to any awaitable_ expression (such as a call
to another coroutine) to suspend execution of the coroutine until the awaitable
has a value or exception ready, at which point the coroutine is resumed and the
``await`` expression returns that value or raises that exception.

Here's a basic example you've seen in all the tutorials:

.. code:: python

    import asyncio

    async def waiter():
        print("Before sleep")
        await asyncio.sleep(5)
        print("After sleep")

    asyncio.run(waiter())

This code prints a message, waits for a five-second sleep to elapse, and then
prints another message.  As written, it's rather pointless; we're only running
one coroutine at once, so there's no advantage over using a synchronous
function with ``time.sleep()``.  Here's something slightly more involved:

.. code:: python

    import asyncio

    async def operate(time, result):
        print(f"Spending {time} seconds doing operations ...")
        await asyncio.sleep(time)
        print(f"Operations done after {time} seconds!")
        return result

    async def amain():
        x, y = await asyncio.gather(operate(5, 42), operate(2, 23))
        print(f"Got {x=}, {y=}")
        assert x == 42
        assert y == 23

    asyncio.run(amain())

This code mocks spending time on two blocking operations in parallel.  If you
run the script (Python 3.8+ required) and time it, you'll see that it only
takes about 5 seconds in total, and the 2-second task completes three seconds
before the 5-second one.  After both tasks are done, the final "Got x=42, y=23"
message is printed.

Besides ``await``, there are two other syntactical constructs specific to
coroutines: ``async for ... in ...:`` (for iterating over asynchronous
iterables) and ``async with ...:`` (for entering & exiting asynchronous context
managers).  These work the same way as their non-``async`` counterparts, except
that the iterables and context managers in question need to support
asynchronous usage; for example, an ``async for`` cannot iterate over a
``list``, and an ``async with`` cannot operate on an ordinary filehandle.
Similarly, a regular ``for`` cannot be applied to an asynchronous iterator, and
a regular ``with`` cannot be applied to, say, ``asyncio.Lock``.

Speaking of asynchronous iteration, this works pretty much how you'd expect: by
using ``yield`` inside a coroutine, it becomes an asynchronous generator that
can be iterated over with ``async for`` or ``await anext(...)``.  Note that, in
contrast to non-generator coroutines, you do not apply ``await`` to an
asynchronous generator.  For example, given this function:

.. code:: python

    async def aiterator():
        for i in range(5):
            await asyncio.sleep(i)
            yield i

you use it like this:

.. code:: python

    async for x in aiterator():
        print(x)

No ``await`` anywhere in the ``async for`` loop.

Note that there is no way to get a value out of a coroutine without awaiting on
it (either directly or via something like |asyncio.gather|_); if a coroutine is
never awaited and never converted into a task, ``asyncio`` will complain when
it is garbage-collected.  Moreover, ``await`` (and ``async for`` and ``async
with``) cannot be used outside of a coroutine; in order to start the awaiting
on a "top-level" coroutine, you need to use |asyncio.run|_.

Note that the body of a coroutine isn't required to contain any ``await``\s or
similar, though if it doesn't, there often isn't much point in making it a
coroutine in the first place.  An exception is the ``__aenter__()`` special
method of asynchronous context managers; usually, the body will just be
``return self``, but it's still required to define the method with ``async
def``.


Type Annotations
----------------

Adding type annotations to asynchronous code works the same way as for
synchronous code.  If an asynchronous ``func()`` take an integer ``x`` and
returns a string, you write its annotated signature as ``async def func(x: int)
-> str``.  However, if you pass around an unawaited coroutine object (not
always the best idea), you annotate it as ``Awaitable[T]``, where ``T`` is the
return type of the coroutine.

Async callables do not have their own type; they are instead annotated as
``Callable[..., Awaitable[T]]``, where ``T`` is the return type of the
coroutine function.

Asynchronous iterators, iterables, and context managers, though, do get their
own types: ``AsyncIterator``, ``AsyncIterable``, and
``typing.AsyncContextManager``/``contextlib.AbstractAsyncContextManager``.


Special Methods
---------------

.. rubric:: ``__aiter__()`` and ``__anext__()``

These methods are used to implement asynchronous iterator & iterable classes as
an alternative to writing asynchronous generator functions, analogously to how
a class can be defined with ``__iter__()`` and ``__next__()`` methods to
implement a synchronous iterator as an alternative to writing a generator
function.

``__aiter__()`` must be a synchronous function that returns an object with
``__aiter__()`` and ``__anext__()`` methods.  ``__anext__()`` must be a
coroutine that either returns a value or raises a ``StopAsyncIteration``
exception.

.. rubric:: ``__aenter__()`` and ``__aexit__()``

These methods are used to implement asynchronous context managers.  They are
defined the same way as the ``__enter__()`` and ``__exit__()`` methods of
synchronous context managers, except that the asynchronous versions must be
coroutines.

.. rubric:: ``__await__()``

This method is used to create a future-like class that can be awaited directly.
There is generally very little need to implement this, but we include it here
for completeness.

``__await__()`` must be a synchronous function that returns an iterator.  This
iterator will be advanced each time the event loop checks to see if the
future-like is ready to return a value.  If the future-like is not ready, the
iterator must yield a special value (see below).  If the future-like is ready,
it must either ``return`` a result or raise an exception; this result or
exception will then be the result of the ``await`` expression acting on the
future-like.

The values that the iterator yields depend on what async implementation the
code is running under (See "`Alternative Async Implementations`_" below).  When
using the Python standard library's ``asyncio``, you generally want to yield
``None``.  When using trio, you need to yield an instance of one of several
private classes internal to trio.  When using curio, you need to yield a
``("trap_name", *trap_args)`` tuple instructing the kernel to invoke a special
"trap" function; yielding ``("trap_sleep", 0)`` instructs the kernel to do
nothing special.

For example, if you want to implement your own ``Future`` class for use with
``asyncio``, you might start out writing it like so:

.. code:: python

    class MyFuture:
        def __init__(self):
            self.value = None
            self.is_set = False

        def set_value(self, value):
            self.value = valuse
            self.is_set = True

        def __await__(self):
            while not self.is_set:
                yield
            return self.value


Historical Note: Generator-Based Coroutines
-------------------------------------------

When ``asyncio`` was first introduced in Python 3.4, the ``async`` and
``await`` keywords were not yet present.  Instead, coroutine functions were
created by applying the ``@asyncio.coroutine`` decorator to a normal generator
function, and awaiting was done using ``yield from``.  There were no
asynchronous iterators or asynchronous context managers in 3.4, either.  Even
after ``async`` and ``await`` were introduced in Python 3.5, the older
generator-based coroutines could not use them.

This style of writing coroutines was deprecated in Python 3.8 and removed
entirely in Python 3.11.


Running More than One Coroutine at Once
=======================================

Now for the part you've been waiting for, and the part that makes asynchronous
programming worth it: actually running multiple functions concurrently.

The simplest way to start running another coroutine concurrently is to pass a
coroutine object to |asyncio.create_task|_; this schedules the coroutine for
execution, but it won't actually start running until the next time the current
coroutine calls ``await`` (and maybe not even then).  |asyncio.create_task|_
returns an |asyncio.Task|_ object that can be used to query the state of the
coroutine or cancel it; awaiting on the task object will cause the current
coroutine to be suspended until the task is complete, at which point the return
value of the task's underlying coroutine is returned.

If you create multiple tasks and then ``await`` on them one by one, a given
``await`` will not return a result until the task in question is done; if task
B finishes running while you're still awaiting on task A, the coroutine doing
the awaiting will continue to be suspended until A is done, and when it then
later awaits on B, it will get back B's return value immediately, because B is
already done.  For example, the following code:

.. code:: python

    import asyncio
    from time import strftime

    def hms():
        return strftime("%H:%M:%S")

    async def operate(time, result):
        print(f"{hms()}: Spending {time} seconds doing operations ...")
        await asyncio.sleep(time)
        print(f"{hms()}: Operations done after {time} seconds!")
        return result

    async def amain():
        task1 = asyncio.create_task(operate(5, 42))
        task2 = asyncio.create_task(operate(2, 23))
        r1 = await task1
        print(f"{hms()}: task1 returned {r1}")
        r2 = await task2
        print(f"{hms()}: task2 returned {r2}")

    asyncio.run(amain())

outputs something like the following::

    17:12:56: Spending 5 seconds doing operations ...
    17:12:56: Spending 2 seconds doing operations ...
    17:12:58: Operations done after 2 seconds!
    17:13:01: Operations done after 5 seconds!
    17:13:01: task1 returned 42
    17:13:01: task2 returned 23

If you need to await on multiple coroutines but don't care about the exact
order in which they finish, you can use |asyncio.gather|_,
|asyncio.as_completed|_, or |asyncio.wait|_ to await on them together; `this
article <hynek_>`_ gives a good overview and explanation of the differences
between the functions.

.. |asyncio.as_completed| replace:: ``asyncio.as_completed()``
.. _asyncio.as_completed:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.as_completed

.. |asyncio.wait| replace:: ``asyncio.wait()``
.. _asyncio.wait:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.wait

.. _bgerr:

You don't have to await on a task if you don't need its return value or don't
need to be assured that it ever finishes, but if such a "background task"
raises an uncaught exception, ``asyncio`` will complain.  One way to address
this is to attach a synchronous callback function to the task with
``Task.add_done_callback()`` that retrieves any uncaught exceptions with
``Task.exception()``, like so:

.. code:: python

    import asyncio
    from time import strftime

    def hms():
        return strftime("%H:%M:%S")

    async def bg_task():
        print(f"{hms()}: In the background")
        raise RuntimeError("Ouch")

    def done_callback(task):
        try:
            if e := task.exception():
                print(f"{hms()}: Task <{task.get_name()}> raised an error: {e}")
            else:
                print(f"{hms()}: Task <{task.get_name()}> finished successfully")
        except asyncio.CancelledError:
            print(f"{hms()}: Task <{task.get_name()}> was cancelled!")

    async def fg_task():
        task = asyncio.create_task(bg_task(), name="bg_task")
        task.add_done_callback(done_callback)
        print(f"{hms()}: Now we sleep and let bg_task do its thing")
        await asyncio.sleep(2)
        print(f"{hms()}: I'm awake!")

    asyncio.run(fg_task())

The output from the above will look like::

    17:16:33: Now we sleep and let bg_task do its thing
    17:16:33: In the background
    17:16:33: Task <bg_task> raised an error: Ouch
    17:16:35: I'm awake!


Exception Handling
==================

Whenever an exception occurs inside a coroutine, it propagates upwards to
whatever's awaiting on it; if unhandled, it will propagate all the way out
through the |asyncio.run|_ call, at which point all still-running tasks are
cancelled.  If there is no chain of ``await``\s leading to the "top-level"
coroutine (say, because you did ``asyncio.create_task()`` and then didn't await
on the result, letting it run in the background), ``asyncio`` will end up
complaining when the coroutine is eventually garbage-collected.  See `the
passage above <bgerr_>`_ on using ``Task.add_done_callback()`` to handle such
errors.

For the specific case of ``KeyboardInterrupt``, the exception is raised in
whatever coroutine the main thread is currently running at the time.


Example Code
============

`This gist`__ provides an example of using asynchronous programming in Python
to download assets for one or more releases of a GitHub repository in parallel.
Try it out with an invocation like::

    python download-assets.py --download-dir jq stedolan/jq jq-1.5 jq-1.6

The script requires Python 3.8 or higher and the ghrepo_ and httpx_ packages on
PyPI to run.

__ https://gist.github.com/jwodder/c0ad1a5a0b6fda18c15dbdb405e1e549

.. _ghrepo: https://github.com/jwodder/ghrepo
.. _httpx: https://www.python-httpx.org


Asynchronous Programming vs. Threads
====================================

Asynchronous programming does not use threads; by default, all coroutines and
their operations are run in whichever thread called |asyncio.run|_.  The
exception is when |asyncio.to_thread|_ or |loop.run_in_executor|_ is used to
run a synchronous function in a separate thread (or, with the latter function,
even a separate process), returning an object that can be awaited on to receive
the function's result.

.. |asyncio.to_thread| replace:: ``asyncio.to_thread()``
.. _asyncio.to_thread:
   https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread

.. |loop.run_in_executor| replace:: ``loop.run_in_executor()``
.. _loop.run_in_executor:
   https://docs.python.org/3/library/asyncio-eventloop.html
   #asyncio.loop.run_in_executor

If multiple threads call |asyncio.run|_ separately, each thread will get its
own event loop and collection of coroutines.

Note that each thread in a Python process has at most one event loop at a time,
and an event loop can only belong to one thread.  An important consequence of
this is that, if you have a synchronous function ``foo()`` that calls
|asyncio.run|_ on some coroutine, then ``foo()`` cannot be called by another
coroutine, because that would lead to two event loops in the same thread, which
doesn't work.

Compared to threads, asynchronous programming provides the following
advantages:

- In asynchronous programming, the coroutine being executed can only change
  when the current coroutine uses ``await`` or similar.  This allows the
  programmer to be assured that, between ``await``\s in the same coroutine,
  operations will not be interfered with and data will not be modified by other
  coroutines.

  When using threads, on the other hand, the running thread [#gil]_ can change
  at almost any point as chosen by the interpreter, which necessitates careful
  programming and copious use of locks in order to ensure that variables are
  not modified by one thread "behind the back of" another thread that's also
  using them.

- If you've done serious work with threads, you've likely encountered the fact
  that you cannot "kill" a thread in the middle of its execution unless the
  "killable" thread is deliberately programmed to allow for this by, say,
  regularly checking some flag and exiting if it's true.  Asynchronous
  programming, on the other hand, makes it possible to *cancel* a running
  coroutine via the ``asyncio.Task.cancel()`` method; once a coroutine is
  cancelled, the next time the event loop checks on it while it's suspended on
  an ``await`` or similar, the coroutine will be resumed, but instead of
  receiving the value it was awaiting for, an ``asyncio.CancelledError`` will
  be raised at the ``await`` expression, likely putting an end to the
  coroutine's execution.

.. [#gil] Recall that, due to Python's global interpreter lock (GIL),
   regardless of how many threads a Python program uses or how many cores your
   machine has, only one thread will be executing Python bytecode at any
   moment.


Async Version History
=====================

Here follows a list of the notable developments & changes in asynchronous
programming across Python versions.

.. rubric:: Python 3.4

The ``asyncio`` module is added, implementing :pep:`3156`.  This enables the
creation of coroutines via the ``@asyncio.coroutine`` decorator; within a
coroutine, awaiting is performed with ``yield from``.  (Support for creating
coroutines in this way would later be deprecated in Python 3.8 and removed in
Python 3.11.)

Most of the functionality added in this version is now categorized as the "low
level" part of ``asyncio``.

.. rubric:: Python 3.5

:pep:`492` implemented:

- It is now possible to define coroutines via ``async def`` and await with
  ``await``.

  - In Python 3.5, ``yield`` cannot be used inside the body of an ``async def``
    coroutine function.

- Asynchronous iteration with ``async for`` is now possible.

- Asynchronous context managers are now supported via ``async with``.

- ``__await__()``, ``__aiter__()``, ``__anext__()``, ``__aenter__()``, and
  ``__aexit__()`` special methods added

- Originally, ``__aiter__()`` methods were expected to be coroutines (or
  anything else returning an awaitable) resolving to asynchronous iterators.
  This was changed in 3.5.2 to have ``__aiter__()`` instead return an
  asynchronous iterator directly.  Returning an awaitable from ``__aiter__()``
  produces a ``PendingDeprecationWarning`` starting in 3.5.2, a
  ``DeprecationWarning`` starting in 3.6, and a ``RuntimeError`` starting in
  3.7.

.. rubric:: Python 3.6

- ``yield`` can now be used in the body of an ``async def`` coroutine function,
  thereby enabling asynchronous generators (:pep:`525`).  (``yield from``
  remains prohibited, though.)

- ``async for`` can now be used in list, set, & dict comprehensions and in
  generator expressions

- ``await`` expressions can now be used in any comprehension

- Using ``async`` or ``await`` as an identifier now generates a
  ``DeprecationWarning``

.. rubric:: Python 3.7

- ``async`` and ``await`` are now reserved keywords

- ``asyncio.run()`` added

- ``asyncio.create_task()`` added

.. rubric:: Python 3.8

- Running ``python -m asyncio`` now starts an async REPL

- ``@asyncio.coroutine()`` is now deprecated

- Passing a ``loop`` parameter is now deprecated for most of ``asyncio``'s
  high-level API

- ``asyncio.CancelledError`` now inherits directly from ``BaseException``
  instead of ``Exception``

.. rubric:: Python 3.9

- ``asyncio.to_thread()`` added

.. rubric:: Python 3.10

- ``aiter()`` and ``anext()`` functions added

- The ``loop`` parameter (deprecated in Python 3.8) is now removed from most of
  ``asyncio``'s high-level API

.. rubric:: Python 3.11

- ``@asyncio.coroutine`` (deprecated in Python 3.8) is now removed


Alternative Async Implementations
=================================

While all the code we've shown so far uses the Python standard library's
``asyncio`` module, it's not required to use this to work with coroutines.
Alternative async library implementations exist that define their own event
loops and primitive operations.  The more notable implementations include:

- `trio <https://github.com/python-trio/trio>`_ seeks to enable *structured
  concurrency* [wiki__] in asynchronous code.  In trio, a collection of tasks
  are run concurrently by grouping them together under a *nursery* (also known
  as a *task group*); if one of the tasks in a nursery raises an error, all
  the other tasks in the same nursery are automatically cancelled.

  __ https://en.wikipedia.org/wiki/Structured_concurrency

- `curio <https://github.com/dabeaz/curio>`_ is an ``asyncio`` alternative
  featuring a more streamlined API and intended to be easier to reason about

In general, different async implementations are incompatible, and features from
different implementations cannot be used in the same code unless you make
careful use of whatever compatibility facilities they may provide.

In fact, just being able to use the same code unmodified regardless of whether
using implementation A or implementation B is tricky, as all implementations
use different primitives.  Libraries to help you with that include:

- `sniffio <https://github.com/python-trio/sniffio>`_ can be used to detect
  which async library is in use

- `anyio <https://github.com/agronholm/anyio>`_ provides a common API (based on
  trio) that can be used to run the same code under both asyncio and trio (and
  previously curio, until it & anyio `parted ways`_ in anyio 3.0)

  .. _parted ways: https://github.com/agronholm/anyio/issues/185
