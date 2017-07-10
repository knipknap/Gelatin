NAME=Gelatin
VERSION=`python setup.py --version | sed s/^v//`
PREFIX=/usr/local/
BIN_DIR=$(PREFIX)/bin
SITE_DIR=$(PREFIX)`python -c "import sys; from distutils.sysconfig import get_python_lib; print get_python_lib()[len(sys.prefix):]"`
DISTDIR=/pub/code/releases/$(NAME)

###################################################################
# Project-specific targets.
###################################################################
apidocs:
	./version.sh
	epydoc --name $(NAME) \
		--exclude ^Gelatin\.parser \
		--exclude ^Gelatin\.compiler \
		--html \
		--no-private \
		--introspect-only \
		--no-source \
		--no-frames \
		--inheritance=included \
		-v \
		-o docs \
		$(NAME)
	./version.sh --reset

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

install:
	mkdir -p $(SITE_DIR)
	./version.sh
	export PYTHONPATH=$(SITE_DIR):$(PYTHONPATH); \
	python setup.py install --prefix $(PREFIX) \
	                        --install-scripts $(BIN_DIR) \
	                        --install-lib $(SITE_DIR)
	./version.sh --reset

uninstall:
	# Sorry, Python's distutils support no such action yet.

.PHONY : tests
tests:
	cd tests/; ./run_suite.py 1

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
	DEBVERSION=`head -1 debian/changelog | sed 's/^\(.*\) (\(.*\)-0ubuntu1).*/\1_\2/'`; \
	    git archive HEAD | gzip >../$$DEBVERSION.orig.tar.gz
	debuild -S -sa -tc -i -I
	./version.sh --reset

dist: targz tarbz deb

###################################################################
# Publishers.
###################################################################
dist-publish:
	./version.sh
	python setup.py bdist_wheel --universal register upload
	./version.sh --reset
