#!/bin/sh

flake8 --extend-ignore=E251 flourish/
flake8 --extend-ignore=E251,E501 tests/

py.test "$@"
