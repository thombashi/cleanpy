.. contents:: **cleanpy**
   :backlinks: top
   :depth: 2

Summary
============================================
cleanpy is a CLI command to remove cache files and temporary files that related to Python.

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

Installation
============================================
::

    pip install cleanpy


Dependencies
============================================
Python 3.6+

- no external package dependencies.
- platform independent


Related project
============================================
pyclean/py3clean: remove cache files with a more conservative approach
