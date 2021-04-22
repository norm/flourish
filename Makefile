all: pypi

pypi:
	python setup.py sdist
	python setup.py bdist_wheel

test:
	./tests/run.sh
