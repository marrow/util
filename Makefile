.PHONY: update install develop devel docs tests test release

update:
	git pull origin master

install:
	python setup.py install

develop:
	python setup.py develop

devel: develop

#docs:
#	python setup.py install

.testing-deps:
	pip install -q nose coverage
	@touch .testing-deps

tests: .testing-deps
	python setup.py nosetests

test: tests

#release:
#	python setup.py install
