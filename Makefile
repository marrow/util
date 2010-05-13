.PHONY: clean update install develop devel docs tests test release

test: tests

clean:
	rm -rvf *.egg-info
	rm -rvf build
	rm -rvf dist
	find . -iname \*.pyc -or -iname \*.pyo -exec rm -vf {} \;

update:
	git pull origin master

install:
	python setup.py install

develop:
	cp -f setup.cfg-devel setup.cfg
	python setup.py develop

devel: develop

#docs:
#	python setup.py install

.testing-deps:
	pip install -q nose coverage
	pip install git+git://github.com/exogen/nose-achievements.git
	@touch .testing-deps

tests: .testing-deps
	python setup.py nosetests

release: tests
	cp -f setup.cfg-release setup.cfg
	python setup.py register sdist bdist_egg upload
	cp -f setup.cfg-devel setup.cfg
