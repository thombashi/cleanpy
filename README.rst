.. contents:: **cleanpy**
   :backlinks: top
   :depth: 2

Summary
============================================
``cleanpy`` is a CLI tool to remove caches and temporary files related to Python.

.. image:: https://badge.fury.io/py/cleanpy.svg
    :target: https://badge.fury.io/py/cleanpy
    :alt: PyPI package version

.. image:: https://github.com/thombashi/cleanpy/actions/workflows/lint_and_test.yml/badge.svg
    :target: https://github.com/thombashi/cleanpy/actions/workflows/lint_and_test.yml
    :alt: CI status of Linux/macOS/Windows

.. image:: https://github.com/thombashi/cleanpy/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/thombashi/cleanpy/actions/workflows/codeql-analysis.yml
    :alt: CodeQL


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

``cleanpy`` will remove cache files and temporary files under the DIR_PATH

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
    - ``.nox``
    - ``.tox``
- ``--include-metadata``:
    - ``.eggs``
    - ``*.egg-info``
    - ``.pyre/``
    - ``.pytype/``
    - ``pip-wheel-metadata``
- ``--include-testing``:
    - ``.coverage``
    - ``coverage.xml``
    - ``nosetests.xml``

All the above options are specified if you use the ``--all`` option.

The following directories are excluded from the remove:

- ``.git``
- ``.hg``
- ``.svn``
- ``node_modules``

Execution example
--------------------------------------------

Clean the current directory except for virtual environments:

::

    cleanpy --all --exclude-envs .

Command help
--------------------------------------------
::

    usage: cleanpy [-h] [-V] [--list] [--follow-symlinks] [--dry-run] [-a] [--include-builds] [--include-envs] [--include-metadata] [--include-testing] [--exclude PATTERN] [--exclude-envs] [-i | -f] [-v | --debug | --quiet] DIR_PATH [DIR_PATH ...]

    Remove cache files and temporary files that are related to Python.

    Skip directories from recursive search: .git, .hg, .svn, node_modules

    positional arguments:
      DIR_PATH            path to a root directory to search.

    options:
      -h, --help          show this help message and exit
      -V, --version       show program's version number and exit
      --list              print target directories/files. this does not actually remove directories/files.
      --follow-symlinks   follow symlinks.
      --dry-run           do no harm.
      -i, --interactive   prompt on each file/directory delete.
      -f, --force         delete file/directory without prompt.
      -v, --verbose       shows the verbose output.
      --debug             for debug print.
      --quiet             suppress execution log messages.

    Remove Target:
      -a, --all           remove all of the caches and temporary files.
      --include-builds    remove files/directories that are related to build: build, dist, docs/_build
      --include-envs      remove virtual environment caches.
      --include-metadata  remove metadata.
      --include-testing   remove test results and coverage files.
      --exclude PATTERN   a regular expression for files and directories to be excluded from the removes.
      --exclude-envs      exclude virtual environments from deletion.

    Issue tracker: https://github.com/thombashi/cleanpy/issues


Dependencies
============================================
Python 3.7+

- no external package dependencies
- platform independent
