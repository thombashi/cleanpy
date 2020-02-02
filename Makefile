PACKAGE := python_package_template


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint
	-travis lint

.PHONY: clean
clean:
	@-python setup.py clean --all
	@rm -rf $(PACKAGE)-*.*.*/ \
		dist/ \
		pip-wheel-metadata/ \
		.eggs/ \
		.pytest_cache/ \
		.tox/ \
		*.egg-info/
	@-find . -name "__pycache__" -type d -exec rm -rf "{}" \;
	@-find . -name "*.pyc" -delete
	@-find . -not -path '*/\.*' -type f | grep -E .+\.py\.[a-z0-9]{32,}\.py$ | xargs -r rm

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@tox -e release
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e . tox
