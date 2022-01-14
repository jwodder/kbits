====================================
Creating Multi-Value Enums in Python
====================================

:Date: 2022-01-14
:Category: Programming
:Tags: Python, enum, mypy
:Summary:
    How to create an enum in Python where each member has a "main" value and a
    set of "extra" constant attributes

Say you're creating an enum type in Python and you want each enum member to
have one or more additional constant attributes alongside ``value``, but these
attributes can't be easily derived from ``value`` (and thus don't make for good
``@property``\ s).  The Python docs provide `an example involving planets`__
similar to what you want, but on closer inspection, you see it won't do — the
example code produces an enum whose members' ``value``\ s are tuples of the
other attributes, whereas you want or need ``value`` to be something else.  Is
there a way to define enum members with a combination of a "main" value and a
set of "extra" values?

__ https://docs.python.org/3.10/library/enum.html#planet

Yes.  Yes, there is.

For a specific example, let's say you want to define an enum for cardinal and
ordinal directions where the members' ``value``\ s are human-readable names
used in some data source you have to parse and each member should additionally
have ``x`` and ``y`` attributes giving the deltas to add to a coordinate's
components in order to move a step in the respective direction.  That is, you
want the following to evaluate as shown:

>>> Direction("north-west")
<Direction.NORTH_WEST: 'north-west'>
>>> Direction.NORTH_WEST.value
'north-west'
>>> Direction.NORTH_WEST.x
-1
>>> Direction.NORTH_WEST.y
1

The solution is to define each enum member with a tuple of the ``value`` and
extra attributes, and then write a ``__new__`` method that assigns the elements
of the tuple (which are passed as arguments to ``__new__``) appropriately, like
so:

.. code:: python

    from enum import Enum

    class Direction(Enum):
        NORTH      = ("north", 0, 1)
        NORTH_EAST = ("north-east", 1, 1)
        EAST       = ("east", 1, 0)
        SOUTH_EAST = ("south-east", 1, -1)
        SOUTH      = ("south", 0, -1)
        SOUTH_WEST = ("south-west", -1, -1)
        WEST       = ("west", -1, 0)
        NORTH_WEST = ("north-west", -1, 1)

        def __new__(cls, value, x, y):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.x = x
            obj.y = y
            return obj

    # Check that `value` and other attributes are what they're supposed to be:
    for d in Direction:
        print(f"{d!r} {d.name=} {d.value=} {d.x=} {d.y=}")

    # Member access by value uses only the "main" value:
    print(f"{Direction('north')=}")

Output from the above script::

    <Direction.NORTH: 'north'> d.name='NORTH' d.value='north' d.x=0 d.y=1
    <Direction.NORTH_EAST: 'north-east'> d.name='NORTH_EAST' d.value='north-east' d.x=1 d.y=1
    <Direction.EAST: 'east'> d.name='EAST' d.value='east' d.x=1 d.y=0
    <Direction.SOUTH_EAST: 'south-east'> d.name='SOUTH_EAST' d.value='south-east' d.x=1 d.y=-1
    <Direction.SOUTH: 'south'> d.name='SOUTH' d.value='south' d.x=0 d.y=-1
    <Direction.SOUTH_WEST: 'south-west'> d.name='SOUTH_WEST' d.value='south-west' d.x=-1 d.y=-1
    <Direction.WEST: 'west'> d.name='WEST' d.value='west' d.x=-1 d.y=0
    <Direction.NORTH_WEST: 'north-west'> d.name='NORTH_WEST' d.value='north-west' d.x=-1 d.y=1
    Direction('north')=<Direction.NORTH: 'north'>

.. note::

    If you're inheriting a concrete non-``Enum`` type in addition to ``Enum``
    (whether explicitly or via ``IntEnum`` or ``StrEnum``), you may need to
    replace the ``obj = object.__new__(cls)`` line in the ``__new__`` method
    with an invocation of the concrete type's ``__new__``.  For example, if
    inheriting from ``(str, Enum)`` or Python 3.11's ``StrEnum``, this line
    should become ``obj = str.__new__(cls, value)``.

Now, if you're type-checking with mypy_ (and you really should be), you'll
likely hit some errors on the above code, even after adding annotations to
``__new__``.  Specifically, as of mypy 0.931, there are two outstanding mypy
issues that affect the above snippet:

- `Issue #1021`_ means that mypy ignores attribute assignments in ``__new__``,
  so it won't recognize ``x`` and ``y`` as attributes of ``Direction``, leading
  to ``print(f"… {d.x=} {d.y=}")`` being seen as erroneous.  There are two ways
  to make mypy aware of the extra-value attributes: either add annotations for
  them in the main body of the class, like so:

  .. code:: python

    class Direction(Enum):
        NORTH      = ("north", 0, 1)
        # [snip]
        NORTH_WEST = ("north-west", -1, 1)

        # Add these two lines:
        x: int
        y: int

        def __new__(cls, value: str, x: int, y: int) -> Direction:
            ...

  ... or else move the extra-value assignments to an ``__init__`` method, like
  so:

  .. code:: python

    class Direction(Enum):
        NORTH      = ("north", 0, 1)
        # [snip]
        NORTH_WEST = ("north-west", -1, 1)

        def __new__(cls, value: str, x: int, y: int) -> Direction:
            obj = object.__new__(cls)
            obj._value_ = value
            return obj

        def __init__(self, value: str, x: int, y: int) -> None:
            self.x = x
            self.y = y

- The second mypy problem is `issue #10573`_: mypy is not aware of the ``Enum``
  class's trickery with its constructor, so when it sees ``Direction('north')``
  on the last line, having already seen a ``Direction.__new__`` that takes
  three arguments, it thinks there are two arguments missing from the
  ``Direction()`` call.  Unfortunately, at time of writing, there does not seem
  to be a way around this other than just slapping a "``# type:
  ignore[call-arg]``" comment on each call to a multi-value enum type.


.. _mypy: http://www.mypy-lang.org
.. _issue #1021: https://github.com/python/mypy/issues/1021
.. _issue #10573: https://github.com/python/mypy/issues/10573
