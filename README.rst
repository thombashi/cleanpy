.. contents:: **cleanpy**
   :backlinks: top
   :depth: 2

Summary
============================================
cleanpy is a CLI command to remove cache files and temporary files that related to Python.

.. image:: https://badge.fury.io/py/cleanpy.svg
    :target: https://badge.fury.io/py/cleanpy
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/cleanpy.svg
    :target: https://pypi.org/project/cleanpy
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/cleanpy.svg
    :target: https://pypi.org/project/cleanpy
    :alt: Supported Python implementations

.. image:: https://img.shields.io/travis/thombashi/cleanpy/master.svg?label=Linux/macOS%20CI
    :target: https://travis-ci.org/thombashi/cleanpy
    :alt: Linux/macOS CI status


Usage
============================================
::

    cleanpy DIR_PATH [DIR_PATH ...]

``cleanpy`` will remove cache files and temporaly files under the DIR_PATH

Reove files/directories are as follows:

- files:
    - ``.coverage``
    - ``coverage.xml``
    - ``nosetests.xml``
    - ``*.manifest``
    - ``*.spec``
    - ``*.pyc``
    - ``*.pyo``

- directories:
    - ``__pycache__``
    - ``.cache``
    - ``.eggs``
    - ``.mypy_cache``
    - ``.nox``
    - ``.pyre``
    - ``.pytest_cache``
    - ``.pytype``
    - ``.tox``
    - ``.venv``
    - ``*.egg-info``

If ``--include-build-cache`` option is specified, also remove the following directories:

- ``build``
- ``dist``
- ``docs/_build``

Following directories are excluded from the search:

- ``.git``
- ``.hg``
- ``.svn``
- ``node_modules``

Command help
--------------------------------------------
::

    usage: cleanpy [-h] [-V] [--follow-symlinks] [--include-build-cache] [--exclude PATTERN] [--dry-run] [-v | --debug | --quiet]
                DIR_PATH [DIR_PATH ...]

    Remove cache files and temporary files that related to Python.

    Skip directories from recursive search: .git, .hg, .svn, node_modules

    positional arguments:
    DIR_PATH              path to a root directory to search

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    --follow-symlinks     follow symlinks
    --include-build-cache
                            remove build cache directories: build, dist, docs/_build
    --exclude PATTERN     a regular expression that matches files and directories that should be excluded on recursive searches.
    --dry-run             do no harm.
    -v, --verbose         shows verbose output.
    --debug               for debug print.
    --quiet               suppress execution log messages.

    Issue tracker: https://github.com/thombashi/cleanpy/issues


Installation
============================================
::

    pip install cleanpy


Dependencies
============================================
Python 3.6+

- no external package dependencies.
- platform independent
