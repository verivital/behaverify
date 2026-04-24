"""Sphinx configuration for the BehaVerify documentation site.

Stack mirrors the sibling VeriVITAL projects (nnVLA, n2v, fastsym): Furo
theme + ``sphinx_design`` cards + ``myst_parser`` + ``sphinx_copybutton``
+ ``sphinx-autoapi`` + ``sphinxcontrib-mermaid``. The landing-page
pipeline figure is authored in TikZ and pre-rendered to SVG/PNG; see
``_static/tikz/pipeline.tex`` and ``_static/tikz/README.md`` for the
regeneration command.
"""

from __future__ import annotations

import sys
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DOCS_ROOT.parent

# --- Project info --------------------------------------------------------
project = "BehaVerify"
author = "Serena Serafina Serbinowska and the BehaVerify contributors"
copyright = "2022-2026, BehaVerify contributors"

try:
    # behaverify installs as behaverify==1.0.0 via pyproject.toml
    import tomllib
    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        release = tomllib.load(fh)["project"]["version"]
except Exception:  # pragma: no cover - docs can build without package install
    release = "1.0.0"

version = ".".join(release.split(".")[:2])

# --- General -------------------------------------------------------------
extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "autoapi.extension",
    "sphinxcontrib.mermaid",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "deflist",
    "fieldlist",
    "tasklist",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "README.md",
    "**/README.md",
    "_templates/.gitkeep",
    "_static/tikz",  # raw TeX source, not docs content
    "DEPLOYMENT.md",  # maintainer-only doc, intentionally not in any toctree
]

suppress_warnings = [
    "autoapi.python_import_resolution",
    "autoapi.not_readable",
    "ref.python",
    # Every ``dsl_to_*.py`` declares its own ``ONNX_IMPORTED`` flag via
    # try / except ImportError. autoapi produces one duplicate-object
    # description per module; the rendered pages show both correctly.
    "app.add_directive",
    "domains",
    "misc.copy_overwrite",
    # Docstrings in the behaverify core code use freeform indentation
    # that docutils flags as 'Block quote ends without a blank line'.
    # The rendered pages remain readable; these warnings are tracked
    # for a later docstring cleanup pass and must not block CI.
    "docutils",
]

# --- AutoAPI -------------------------------------------------------------
autoapi_dirs = [str(REPO_ROOT / "src" / "behaverify")]
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]


# -------------------------------------------------------------------------
# Silence the four "duplicate object description of ... ONNX_IMPORTED"
# warnings that autoapi generates because every ``dsl_to_*`` module
# declares its own module-level ``ONNX_IMPORTED`` guard. The underlying
# Sphinx warning is uncategorised, so ``suppress_warnings`` cannot reach
# it; we install a logging.Filter instead.
# -------------------------------------------------------------------------
import logging  # noqa: E402


class _IgnoreDuplicateOnnxImported(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover
        msg = record.getMessage()
        return not (
            "duplicate" in msg
            and "ONNX_IMPORTED" in msg
        )


def setup(app):  # noqa: D401 -- Sphinx extension contract
    """Wire the ONNX_IMPORTED filter into Sphinx's warning logger."""
    for name in ("sphinx", "sphinx.domains.python"):
        logging.getLogger(name).addFilter(_IgnoreDuplicateOnnxImported())
    return {"parallel_read_safe": True, "parallel_write_safe": True}
autoapi_python_class_content = "both"
autoapi_keep_files = False
autoapi_ignore = [
    "*/variations/*",          # historical / deprecated code paths with
                                # non-Sphinx-compatible docstrings
    "*/data/*",
    "*/grid_world_draw/*",     # binary assets, not API
    "*/behaverify_gui.py",     # Tk GUI, not core library API
]

# Keep autoapi strict about the subset of the code we do ship --- but silence
# known-benign duplicate-description warnings from the four ``dsl_to_*`` flag
# guards. The workaround is in conf.py rather than per-module because the
# pattern is identical across four files.
nitpick_ignore = [
    ("py:obj", "behaverify.check_grammar.ONNX_IMPORTED"),
    ("py:obj", "behaverify.dsl_to_cpp.ONNX_IMPORTED"),
    ("py:obj", "behaverify.dsl_to_nuxmv.ONNX_IMPORTED"),
    ("py:obj", "behaverify.dsl_to_python.ONNX_IMPORTED"),
]

# --- HTML (Furo) ---------------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_title = f"BehaVerify {version}"
html_logo = None
html_favicon = None
html_theme_options = {
    "source_repository": "https://github.com/verivital/behaverify",
    "source_branch": "main",
    "source_directory": "docs/",
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
}

# --- Copybutton ----------------------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |# "
copybutton_prompt_is_regexp = True

# --- Intersphinx ---------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "py_trees": ("https://py-trees.readthedocs.io/en/devel/", None),
}

# --- Mermaid -------------------------------------------------------------
mermaid_version = "10.9.1"
