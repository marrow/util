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

tests:
	python setup.py test

test: tests

#release:
#	python setup.py install
