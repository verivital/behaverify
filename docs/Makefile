# Minimal Makefile for Sphinx documentation.

SPHINXOPTS    ?= -W --keep-going -n
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help html linkcheck clean tikz

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

html:
	@$(SPHINXBUILD) -b html $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)/html"

linkcheck:
	@$(SPHINXBUILD) -b linkcheck $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck"

clean:
	@rm -rf $(BUILDDIR)

# Re-render every TikZ source under _static/tikz/ into SVG + PNG in
# _static/img/. Requires pdflatex and dvisvgm (both shipped with
# MiKTeX / TeX Live).
TIKZ_SRCS := $(wildcard _static/tikz/*.tex)
TIKZ_NAMES := $(notdir $(basename $(TIKZ_SRCS)))

tikz:
	@for t in $(TIKZ_NAMES); do \
	  echo "==> rendering $$t"; \
	  (cd _static/tikz && pdflatex -interaction=nonstopmode $$t.tex >/dev/null) && \
	  (cd _static/tikz && dvisvgm --pdf $$t.pdf -o ../img/$$t.svg) && \
	  (cd _static/tikz && pdftoppm -r 180 -png $$t.pdf /tmp/$$t && \
	    mv /tmp/$$t-1.png ../img/$$t.png 2>/dev/null || true); \
	done
