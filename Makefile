#!make
.PHONY: clean-pyc clean-build
.DEFAULT_GOAL := help

SHELL = /bin/bash

help:
	@echo ""
	@echo " +---------------------------------------+"
	@echo " | Janus Logging                         |"
	@echo " +---------------------------------------+"
	@echo "    clean"
	@echo "        Remove python and build artifacts"
	@echo "    install"
	@echo "        Install requirements for development and testing"
	@echo "    demo"
	@echo "        Run a simple demo"
	@echo ""
	@echo "    test"
	@echo "        Run unit tests"
	@echo "    test-all"
	@echo "        Run integration tests"
	@echo ""

clean-pyc:
	@echo $@
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~'    -exec rm --force {} +

clean-build:
	@echo $@
	rm --force --recursive .tox/
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info
	rm --force --recursive .pytest_cache/

clean-pycache:
	@echo $@
	find . -name '__pycache__' -exec rm -rf {} +

clean: clean-build clean-pyc clean-pycache

install: clean
	@echo $@
	pip install --no-cache-dir -U -r requirements.txt
	# flake8 --install-hook git
	# git config --local --bool flake8.strict true

demo: clean
	@echo $@
	python demo.py

flake: clean
	@echo $@
	flake8 --statistics --ignore E252 janus_logging tests scripts demo.py setup.py

bandit: clean
	@echo $@
	bandit -r  janus_logging/ tests/ demo.py setup.py

test-unit: flake bandit
	@echo $@
	python -m pytest -v -x tests/ --cov=janus_logging

test-tox: clean
	@echo $@
	tox

test: test-unit
	@echo $@

test-all: test-unit test-tox
	@echo $@


pypy-deps:
	@echo $@
	pip install -U twine

pypy-build: clean test-all pypy-deps
	@echo $@
	python setup.py sdist bdist_wheel
	# python3 setup.py bdist_egg --exclude-source-files
	# python setup.py bdist_wheel

pypy-upload-test: pypy-deps
	@echo $@
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypy-upload: pypy-deps
	@echo $@
	python -m twine upload dist/*
