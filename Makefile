PYTHON := python3


.PHONY: build
build: clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint

.PHONY: clean
clean:
	@-$(PYTHON) setup.py clean --all

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@tox -e release
	@make clean

.PHONY: setup
setup:
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test] releasecmd tox
	@$(PYTHON) -m pip check
