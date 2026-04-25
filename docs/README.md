# BehaVerify documentation

Sphinx site. Built with Furo + `sphinx_design` + `myst_parser` +
`sphinx_copybutton` + `sphinx-autoapi` + `sphinxcontrib-mermaid` to
match the sibling VeriVITAL projects (nnVLA, n2v, fastsym).

## Build

```bash
pip install -r requirements.txt
pip install -e ..              # so sphinx-autoapi can import behaverify
make -C docs html              # produces _build/html/index.html
```

On Windows from the repo root:

```powershell
pip install -r docs\requirements.txt
pip install -e .
docs\make.bat html
```

## Landing-page pipeline figure

Authored in TikZ at `_static/tikz/pipeline.tex`; rendered artefacts
(`_static/img/pipeline.png`) are committed so the Sphinx build
does not require a TeX installation. To regenerate after editing the
`.tex` source, run `make -C docs tikz`.

## Layout

```
docs/
├── conf.py                # Sphinx configuration
├── index.rst              # landing page + pipeline hero
├── getting-started/       # installation, quickstart, first-model
├── user-guide/            # DSL, modes, components, specs, strategies
├── developer/             # architecture, adding modes/checks
├── examples/              # worked examples from examples/
├── reference/             # CLI, glossary, file formats
├── _static/
│   ├── css/custom.css
│   ├── img/pipeline.{svg,png}
│   └── tikz/pipeline.tex
└── requirements.txt
```

Developer docs live under `developer/`; contributors adding a new
generation mode or monitor template should start from
`developer/adding-a-mode.rst`.
