NAME=Gelatin
VERSION=`grep version setup.py | cut -d"'" -f2`
PACKAGE=$(NAME)-$(VERSION)-1
PREFIX=/usr/local/
DISTDIR=/pub/code/releases/$(NAME)

###################################################################
# Project-specific targets.
###################################################################

###################################################################
# Standard targets.
###################################################################
.PHONY : clean
clean:
	find . -name "*.pyc" -o -name "*.pyo" | xargs -n1 rm -f
	rm -Rf build

.PHONY : dist-clean
dist-clean: clean
	rm -Rf dist $(PACKAGE)* src/*.egg-info

.PHONY : doc
doc:
	cd doc; make

install:
	python setup.py install --prefix $(PREFIX)

uninstall:
	# Sorry, Python's distutils support no such action yet.

.PHONY : tests
tests:
	cd tests/$(NAME)/; ./run_suite.py 1

###################################################################
# Package builders.
###################################################################
targz:
	./version.sh
	python setup.py sdist --formats gztar
	./version.sh --reset

tarbz:
	./version.sh
	python setup.py sdist --formats bztar
	./version.sh --reset

deb:
	./version.sh
	#debuild -S -sa
	#cd ..; sudo pbuilder build $(NAME)_$(VERSION)-0ubuntu1.dsc; cd -
	./version.sh --reset

dist: targz tarbz deb

###################################################################
# Publishers.
###################################################################
dist-publish: dist
	python setup.py sdist register upload
	mkdir -p $(DISTDIR)/
	for i in dist/*; do \
		mv $$i $(DISTDIR)/`basename $$i | tr '[:upper:]' '[:lower:]'`; \
	done

.PHONY : doc-publish
doc-publish:
	cd doc; make publish

.PHONY : publish-local
publish-local:
	git push
