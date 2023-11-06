===============================================
Skipping Pytest Tests Unless an Option is Given
===============================================

:Date: 2021-12-05
:Category: Programming
:Tags: Python, pytest, testing
:Summary:
    When testing Python code with pytest_, you may occasionally write tests
    that you only want to run under special circumstances, such as long-running
    tests that should only be run under continuous integration and not when
    invoking ``pytest`` locally.  The naïve way to accomplish this is to
    decorate the tests in question with a pytest mark like
    ``@pytest.mark.slow`` and then specify ``-m "not slow"`` when running
    pytest locally, but then you have to remember to pass this option every
    time, and if you hardcode it into your ``tox.ini`` or pytest configuration,
    you'll need something else to remove it when testing under CI.
    Fortunately, there are better ways to make pytest skip tests by default.

When testing Python code with pytest_, you may occasionally write tests that
you only want to run under special circumstances, such as long-running tests
that should only be run under continuous integration and not when invoking
``pytest`` locally.  The naïve way to accomplish this is to decorate the tests
in question with a pytest mark like ``@pytest.mark.slow`` and then specify ``-m
"not slow"`` when running pytest locally, but then you have to remember to pass
this option every time, and if you hardcode it into your ``tox.ini`` or pytest
configuration, you'll need something else to remove it when testing under CI.
Fortunately, there are better ways to make pytest skip tests by default.

.. _pytest: https://docs.pytest.org

In this article, we will add a "``--run-slow``" option to pytest and configure
selected "slow" tests to be skipped unless this option is given on the command
line.


Option 1: Use a Hook to Attach a ``skip`` Marker to Marked Tests
================================================================

One way to disable selected tests by default is to give them all some mark and
then use the ``pytest_collection_modifyitems`` hook to add an additional
``pytest.mark.skip`` mark if a certain command-line option was not given.  We
do this by adding the following to our ``conftest.py`` file:

.. code:: python

    import pytest

    def pytest_addoption(parser):
        parser.addoption(
            "--run-slow",
            action="store_true",
            default=False,
            help="Run slow tests",
        )

    def pytest_collection_modifyitems(config, items):
        if not config.getoption("--run-slow"):
            skipper = pytest.mark.skip(reason="Only run when --run-slow is given")
            for item in items:
                if "slow" in item.keywords:
                    item.add_marker(skipper)

and then decorate all of our slow tests with ``@pytest.mark.slow``, like so:

.. code:: python

    import pytest

    @pytest.mark.slow
    def test_something_slow():
        ...

Now, when we run ``pytest``, the marked tests will be skipped unless the
``--run-slow`` option is passed on the command line.


Option 2: Use ``@pytest.mark.skipif``
=====================================

Did you know?  The condition passed to ``@pytest.mark.skipif`` doesn't have to
be a Python boolean expression; it can instead be a `condition string`__
containing a Python expression, and condition strings are evaluated in a
namespace that includes the pytest ``config`` object.  This lets us write
``skipif`` decorators that skip tests based on whether or not certain
command-line options were given.

__ https://docs.pytest.org/en/6.2.x/historical-notes.html#string-conditions

We start out by defining a command-line option in ``conftest.py`` that will be
used to tell pytest to run otherwise-skipped tests:

.. code:: python

    def pytest_addoption(parser):
        parser.addoption(
            "--run-slow",
            action="store_true",
            default=False,
            help="Run slow tests",
        )

We then decorate the tests we want to skip by default like so:

.. code:: python

    import pytest

    @pytest.mark.skipif(
        "not config.getoption('--run-slow')",
        reason="Only run when --run-slow is given",
    )
    def test_something_slow():
        ...

If there are multiple tests to apply this condition to, we can assign the
``skipif`` decorator to a variable that is then used to decorate each one, like
so:

.. code:: python

    import pytest

    slow_test = pytest.mark.skipif(
        "not config.getoption('--run-slow')",
        reason="Only run when --run-slow is given",
    )

    @slow_test
    def test_something_slow():
        ...

    @slow_test
    def test_something_very_slow():
        ...

.. warning::

    You may see some old guides on the internet that instead write the
    ``skipif`` decorator with an actual boolean condition defined in terms of
    ``pytest.config``, e.g.:

    .. code:: python

        import pytest

        # Outdated!
        @pytest.mark.skipif(
            not pytest.config.getoption("--run-slow"),
            reason="Only run when --run-slow is given",
        )
        def test_something_slow():
            ...

    However, this no longer works; the ``pytest.config`` global variable was
    removed from pytest in version 5.1.0.


Option 3: Use a Pre-Existing Plugin
===================================

As is the case for many, many things in Python, other people have already done
the job of generalizing the above and publishing it on PyPI.  I am aware of two
pytest plugin projects for skipping tests unless a command-line option is
given: pytest-explicit_ and pytest-optional-tests_.  I have not used either,
but if they work as advertised, they should prove helpful.

.. _pytest-explicit: https://pypi.org/project/pytest-explicit/
.. _pytest-optional-tests: https://pypi.org/project/pytest-optional-tests/
