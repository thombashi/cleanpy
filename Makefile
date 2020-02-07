PACKAGE := python_package_template


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint
	travis lint

.PHONY: clean
clean:
	@-python setup.py clean --all

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@tox -e release
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] tox
