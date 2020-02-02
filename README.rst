.. contents:: **project_name**
   :backlinks: top
   :depth: 2


Python project template: TODO
============================================
- Click ``[Use this template]`` button to create a new repository
- Replace ``project_name`` within the repository to an arbitrary name
- Modify authorized information at ``<project_name>/__version__.py``


********************************************************

README

Summary
============================================

.. image:: https://img.shields.io/travis/thombashi/python-project-template/master.svg?label=Linux/macOS%20CI
    :target: https://travis-ci.org/thombashi/python-project-template
    :alt: Linux/macOS CI status

.. image:: https://img.shields.io/appveyor/ci/thombashi/python-project-template/master.svg?label=Windows%20CI
    :target: https://ci.appveyor.com/project/thombashi/python-project-template/branch/master
    :alt: Windows CI status

.. image:: https://coveralls.io/repos/github/thombashi/python-project-template/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/python-project-template?branch=master
    :alt: Test coverage: coveralls

.. image:: https://codecov.io/gh/thombashi/python-project-template/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/thombashi/python-project-template
    :alt: Test coverage: codecov


Usage
============================================

:Sample Code:
    .. code-block:: python

        # Sample code

:Output:
    .. code-block::

        # Output


Installation
============================================
::

    pip install <project_name>


Dependencies
============================================
Python 3.5+

********************************************************

Development
============================================

Setup
--------------------------------------------
::

    $ make setup

Running tests
--------------------------------------------
::

    $ tox

Code formatting
--------------------------------------------
::

    $ make fmt

Linting
--------------------------------------------
::

    $ make check

Release a package to PyPI
--------------------------------------------
::

    $ make build
    $ make release

- Prerequisites for release:
    - PyPI account
    - GPG key
