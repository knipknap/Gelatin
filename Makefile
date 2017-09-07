NAME=Gelatin
VERSION=`python3 setup.py --version | sed s/^v//`

###################################################################
# Standard targets.
###################################################################
.PHONY : clean
clean:
	find . -name "*.pyc" -o -name "*.pyo" | xargs -n1 rm -f
	rm -Rf build

.PHONY : dist-clean
dist-clean: clean
	rm -Rf dist src/*.egg-info

.PHONY : doc
doc:
	cd doc; make

uninstall:
	# Sorry, Python's distutils support no such action yet.

.PHONY : tests
tests:
	python3 setup.py test

###################################################################
# Package builders.
###################################################################
targz:
	./version.sh
	python3 setup.py sdist --formats gztar
	./version.sh --reset

tarbz:
	./version.sh
	python3 setup.py sdist --formats bztar
	./version.sh --reset

wheel:
	./version.sh
	python3 setup.py bdist_wheel --universal
	./version.sh --reset

deb:
	./version.sh
	DEBVERSION=`head -1 debian/changelog | sed 's/^\(.*\) (\(.*\)-0ubuntu1).*/\1_\2/'`; \
	    git archive HEAD | gzip >../$$DEBVERSION.orig.tar.gz
	debuild -S -sa -tc -i -I
	./version.sh --reset

dist: targz tarbz wheel

###################################################################
# Publishers.
###################################################################
dist-publish:
	./version.sh
	python3 setup.py bdist_wheel --universal register upload
	./version.sh --reset
