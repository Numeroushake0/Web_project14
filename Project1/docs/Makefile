SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help clean html

help:
	@echo "make html      → створити HTML-документацію"
	@echo "make clean     → очистити папку build/"

clean:
	rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
