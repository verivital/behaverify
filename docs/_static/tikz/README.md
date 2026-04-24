# TikZ sources for the BehaVerify docs

## `pipeline.tex`

Landing-page pipeline diagram. Produces `../img/pipeline.svg` (vector,
used by the HTML site) and `../img/pipeline.png` (raster fallback).

### Regenerate

From `docs/_static/tikz/`:

```bash
pdflatex -interaction=nonstopmode pipeline.tex
dvisvgm --pdf pipeline.pdf -o ../img/pipeline.svg
pdftoppm -r 180 -png pipeline.pdf ../img/pipeline
mv ../img/pipeline-1.png ../img/pipeline.png
```

Or, from `docs/`:

```bash
make tikz
```

### Requirements

- MiKTeX or TeX Live (`pdflatex`).
- `dvisvgm` (bundled with MiKTeX and most TeX Live installs).
- `pdftoppm` from poppler / MiKTeX for the PNG fallback.

### Notes

The PDF + SVG together are roughly 600 kB and are committed to the
repository to keep the Sphinx build free of LaTeX dependencies. Rebuild
and commit the rendered artefacts whenever the `.tex` source changes.
