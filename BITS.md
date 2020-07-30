- `python.bh`
- Sending e-mail with curl
- `which` vs. `type` vs. `whereis` etc.
- comparison of daemonization tools
- Python: encodings and interacting with the outside world:
    - Python stdio encodings?
    - PYTHONIOENCODING and related I/O encoding issues?
    - notes on decoding `sys.argv` in both Python 2 and Python 3?
- getting output from a SQL SELECT statement as CSV
- math encountered while working on Project Euler problems
    - #15
    - #28
    - #94
    - #115
    - #145
    - #323?
    - #329?
    - #371
    - #381
- IRC protocol notes?
- Gopher protocol?
- `underpy.md`?
- apt & dpkg invocations
- GPG invocations
- how to ensure an Upstart service is stopped: `status $SERVICE | grep stop ||
  stop $SERVICE`
- using Certbot / my Certbot setup?
- setting up Postfix?
    - setting up `luser_relay` with each recipient address getting its own
      mailbox?
- SQLALchemy: Creating a one-to-many relationship with cascading deletes (See
  notes in `sqlalchemy.md`)
- Known best (or at least decent) algorithms for notable NP-Complete problems
  and other things that are well-suited to dynamic programming
    - knapsack problem
    - subset-sum problem
    - eight queens problem
    - permutations & combinations?
    - strings of balanced parentheses?
    - decomposing a permutation into a minimum product of transpositions?
    - ???
- URL templates for downloading Git references (and subtrees of references?)
  from GitHub as zip files
- raytracing notes
- "Python for Programmers"?

- Python packaging:
    - including & accessing non-Python files in Python packages
    - advice for structuring a Python package?
    - integrating a Python package with Travis and Codecov?
    - including LICENSE files in sdists and wheels?
    - common packaging mistakes people make (top-level tests/examples/docs,
      top-level README/LICENSE, strings around values in setup.cfg, etc.)
    - Opinions:
        - Why tests shouldn't be included in built distributions
            - Why top-level `test{,s}/` directories should absolutely not be
              included in built distributions
                - Why they are often accidentally included and how to avoid
                  this
        - Why test & doc dependencies shouldn't be declared as packages' extra
          dependencies
