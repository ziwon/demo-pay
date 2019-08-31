.DEFAULT_GOAL := build
.PHONY: build publish package coverage test lint docs venv
PROJ_SLUG = pay
CLI_NAME = pay
PY_VERSION = 3.7

GREEN = 2
RED = 1

define colorecho
        @tput bold
        @tput setaf $1
        @echo $2
        @tput sgr0
endef

build:
	pip install --editable .

lint:
	pylint $(PROJ_SLUG)

test:
	py.test --cov-report term --cov=$(PROJ_SLUG) tests/ -v -s

quicktest:
	py.test --cov-report term --cov=$(PROJ_SLUG) tests/

coverage: lint
	py.test --cov-report html --cov=$(PROJ_SLUG) tests/

package: clean
	python setup.py sdist

clean :
	rm -rf dist \
	rm -rf *.egg-info
	coverage erase

venv :
	virtualenv --python python$(PY_VERSION) venv
	@echo
	@echo To activate the environment, use the following command:
	@echo
	$(call colorecho, $(GREEN), "source venv/bin/activate")
	@echo
	@echo Once activated, you can use the 'install' target to install dependencies:
	@echo
	$(call colorecho, $(GREEN), "make install")

install:
	pip install -r requirements.txt

licenses:
	pip-licenses --with-url --format=rst \
	--ignore-packages $(shell cat .pip-license-ignore | awk '{$$1=$$1};1')
