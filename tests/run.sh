#!/bin/sh

test_flags=''
[ "$1" = "-v" ] && test_flags='-svv'

flake8 . --exclude=build,dist
py.test ${test_flags} "$@"
