.. contents:: **cleanpy**
   :backlinks: top
   :depth: 2

Summary
============================================
cleanpy is a CLI tool to remove caches and temporary files that related to Python.

.. image:: https://badge.fury.io/py/cleanpy.svg
    :target: https://badge.fury.io/py/cleanpy
    :alt: PyPI package version

.. image:: https://img.shields.io/travis/thombashi/cleanpy/master.svg?label=Linux/macOS%20CI
    :target: https://travis-ci.org/thombashi/cleanpy
    :alt: Linux/macOS CI status


Installation
============================================

Installation: pip
--------------------------------------------
::

    pip install cleanpy

.. image:: https://img.shields.io/pypi/pyversions/cleanpy.svg
    :target: https://pypi.org/project/cleanpy
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/cleanpy.svg
    :target: https://pypi.org/project/cleanpy
    :alt: Supported Python implementations

Installation: snap
--------------------------------------------
::

    sudo snap install cleanpy

.. image:: https://snapcraft.io//cleanpy/badge.svg
    :target: https://snapcraft.io/cleanpy
    :alt: snapcraft status


Usage
============================================
::

    cleanpy DIR_PATH [DIR_PATH ...]

``cleanpy`` will remove cache files and temporaly files under the DIR_PATH

Remove files/directories are as follows:

- files:
    - ``*.pyc``
    - ``*.pyo``

- directories:
    - ``__pycache__``
    - ``.cache``
    - ``.mypy_cache``
    - ``.pytest_cache``

You can also remove additional files/directories if the following options are specified:

- ``--include-builds``:
    - ``build``
    - ``dist``
    - ``docs/_build``: ``[sphinx]``
    - ``*.manifest``: ``[pyinstaller]``
    - ``*.spec``: ``[pyinstaller]``
- ``--include-envs``:
    - ``.venv``
- ``--include-metadata``:
    - ``.eggs``
    - ``*.egg-info``
    - ``.pyre/``
    - ``.pytype/``
    - ``pip-wheel-metadata``
- ``--include-testing``:
    - ``.nox``
    - ``.tox``
    - ``.coverage``
    - ``coverage.xml``
    - ``nosetests.xml``

All of the above options are specified if set the ``--all`` option to the command.

Following directories are excluded from the search:

- ``.git``
- ``.hg``
- ``.svn``
- ``node_modules``

Execution example
--------------------------------------------
::

    $ cleanpy -av --exclude-envs .
    [INFO] remove directory [cache - Python]: ./test/__pycache__
    [INFO] remove directory [cache - pytest]: ./.pytest_cache
    [INFO] remove directory [testing - manager]: ./.tox
    [INFO] remove directory [build - Python]: ./dist
    [INFO] remove directory [cache - mypy]: ./.mypy_cache
    [INFO] remove directory [metadata - type checker]: ./.pytype
    [INFO] remove directory [build - Python]: ./build
    [INFO] remove directory [metadata - Python]: ./cleanpy.egg-info
    [INFO] removed 8 directories

Command help
--------------------------------------------
::

    usage: cleanpy [-h] [-V] [--follow-symlinks] [--dry-run] [-a]
                [--include-builds] [--include-envs] [--include-metadata]
                [--include-testing] [--exclude PATTERN] [--exclude-envs]
                [-v | --debug | --quiet]
                DIR_PATH [DIR_PATH ...]

    Remove cache files and temporary files that related to Python.

    Skip directories from recursive search: .git, .hg, .svn, node_modules

    positional arguments:
    DIR_PATH            path to a root directory to search

    optional arguments:
    -h, --help          show this help message and exit
    -V, --version       show program's version number and exit
    --follow-symlinks   follow symlinks
    --dry-run           do no harm.
    -v, --verbose       shows verbose output.
    --debug             for debug print.
    --quiet             suppress execution log messages.

    Remove Target:
    -a, --all           remove all of the caches and teporary files.
    --include-builds    remove files/directories that related build: build,
                        dist, docs/_build
    --include-envs      remove virtual environments.
    --include-metadata  remove metadata.
    --include-testing   remove test results and coverage files.
    --exclude PATTERN   a regular expression that matches files and directories
                        that should be excluded on recursive searches.
    --exclude-envs      exclude virtual environments.

    Issue tracker: https://github.com/thombashi/cleanpy/issues


Dependencies
============================================
Python 3.6+

- no external package dependencies
- platform independent
