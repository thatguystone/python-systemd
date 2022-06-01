PYTHON = python
SED = sed
ETAGS = etags
INCLUDE_DIR := $(shell pkg-config --variable=includedir libsystemd)
INCLUDE_FLAGS := $(shell pkg-config --cflags libsystemd)
VERSION := $(shell $(PYTHON) setup.py --version)
TESTFLAGS = -v

define buildscript
import sys,sysconfig
print("build/lib.{}-{}.{}".format(sysconfig.get_platform(), *sys.version_info[:2]))
endef

builddir := $(shell $(PYTHON) -c '$(buildscript)')

all: build

.PHONY: update-constants
update-constants: update-constants.py $(INCLUDE_DIR)/systemd/sd-messages.h
	$(PYTHON) $+ systemd/id128-defines.h

build:
	$(PYTHON) setup.py build_ext $(INCLUDE_FLAGS)
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install --skip-build $(if $(DESTDIR),--root $(DESTDIR))

dist:
	$(PYTHON) setup.py sdist

sign: dist/systemd-python-$(VERSION).tar.gz
	gpg --detach-sign -a dist/systemd-python-$(VERSION).tar.gz

clean:
	rm -rf build systemd/*.so systemd/*.py[co] *.py[co] systemd/__pycache__

distclean: clean
	rm -rf dist MANIFEST

SPHINXOPTS = -D version=$(VERSION) -D release=$(VERSION)
sphinx-%: build
	cd build && \
	  PYTHONPATH=../$(builddir) $(PYTHON) -m sphinx -b $* $(SPHINXOPTS) ../docs $*
	@echo Output has been generated in build/$*

doc: sphinx-html

check: build
	(cd $(builddir) && $(PYTHON) -m pytest . ../../docs $(TESTFLAGS))

www_target = www.freedesktop.org:/srv/www.freedesktop.org/www/software/systemd/python-systemd
doc-sync:
	rsync -rlv --delete --omit-dir-times build/html/ $(www_target)/

upload: dist/systemd-python-$(VERSION).tar.gz dist/systemd-python-$(VERSION).tar.gz.asc
	twine-3 upload $+

TAGS: $(shell git ls-files systemd/*.[ch])
	$(ETAGS) $+

shell:
# we change the directory because python insists on adding $CWD to path
	(cd $(builddir) && $(PYTHON))

.PHONY: build install dist sign upload clean distclean TAGS doc doc-sync shell
