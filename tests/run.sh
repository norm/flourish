#!/bin/sh

flake8 . --exclude=build,dist
py.test "$@"
