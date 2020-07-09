#!/bin/sh

flake8 . --exclude=build,dist --extend-ignore=E251
py.test "$@"
