# Deploying the BehaVerify Documentation

This page explains how to enable the GitHub Pages deployment for the
Sphinx site that lives in `docs/`. It is written for a maintainer of
`verivital/behaverify` who is merging the PR that adds this
documentation for the first time.

## tl;dr — two one-time steps before the docs go live

1. **Enable GitHub Pages with "GitHub Actions" as the source.** (See
   below; takes 30 seconds.)
2. **Merge the PR.** The `Documentation` workflow then runs on every
   push to `main`, on every pull request (for preview), and on a
   manual `Run workflow` click from the Actions tab.

That is the whole setup. The workflow itself is at
`.github/workflows/docs.yml`; it uses the official GitHub Pages
actions (`configure-pages@v5`, `upload-pages-artifact@v3`,
`deploy-pages@v4`) so there are no third-party tokens to configure.

## Step-by-step: enable GitHub Pages *before* merging

1. Go to https://github.com/verivital/behaverify/settings/pages.
2. Under **Build and deployment** → **Source**, select **GitHub
   Actions**. Leave everything else at its default.
3. Save. No branch selection is required with this source — the
   workflow itself supplies the content.
4. (Optional but recommended) Protect the `gh-pages`-equivalent
   environment. Go to
   https://github.com/verivital/behaverify/settings/environments and
   add a new environment named `github-pages`. Under
   **Deployment branches**, pick "Selected branches and tags" and
   add `main` (and `master` if still used). This prevents anyone
   with write access from publishing from a random branch.

That is it on the UI side. Now you can merge the PR.

## What the workflow does

`Documentation` (`.github/workflows/docs.yml`) has two jobs:

### `build`

Runs on every push to `main`, every pull request that touches
`docs/**` or `src/behaverify/**`, and every manual trigger. Steps:

1. Check out the repo.
2. Set up Python 3.12.
3. Install graphviz (system) and the Python deps declared in
   `docs/requirements.txt` plus BehaVerify in editable mode (so
   `sphinx-autoapi` can import the package).
4. Build the HTML: `sphinx-build -b html -W --keep-going -n docs docs/_build/html`.
   The `-W` flag turns warnings into errors, so the build is
   strict — any drift in `refs.bib`, a broken `:doc:` cross-reference,
   a missing image, or a bad ReST directive fails the pipeline.
5. For pushes / manual triggers: upload the built HTML as a
   Pages-flavoured artifact.
6. For pull requests: upload a regular `docs-preview-<PR#>` artifact
   (retention 14 days) that reviewers can download and open
   locally.

### `deploy`

Runs only for non-PR events, takes the Pages artifact from `build`,
and calls `actions/deploy-pages@v4`. The resulting URL is written
into the environment summary in the Actions run.

## Triggering a rebuild manually

Maintainers sometimes need to rebuild the docs without pushing a new
commit (e.g. to pick up a fix in the TikZ source regenerated
out-of-band, or after enabling a new external link). To do that:

1. Open https://github.com/verivital/behaverify/actions/workflows/docs.yml
2. Click **Run workflow** (top-right).
3. Choose `main` as the branch and click the green **Run workflow**
   button.

This uses the `workflow_dispatch` trigger declared in the workflow.

## Local preview

If you want to preview the docs on your laptop before merging:

```bash
pip install -e .
pip install -r docs/requirements.txt
make -C docs html
python -m http.server --directory docs/_build/html
# then browse http://localhost:8000/
```

`sphinx-build` will emit the same warnings the CI uses; if your
local build is clean, the CI build will be too.

## Re-rendering the TikZ pipeline + theory figures

The landing pipeline figure and the theory diagrams are pre-rendered
from the `.tex` sources in `docs/_static/tikz/`; the rendered SVG /
PNG are committed to the repo so the Sphinx build does not need a
LaTeX toolchain.

To regenerate everything after editing any `.tex` source:

```bash
make -C docs tikz     # requires pdflatex + dvisvgm (ships with MiKTeX / TeX Live)
```

Commit the updated SVG / PNG files alongside the `.tex` changes.

## Troubleshooting

**The workflow runs but the site is not updated.**
Check that Pages is set to "GitHub Actions" as the source under
`Settings → Pages`. The other modes (deploy from a branch) are
mutually exclusive with this workflow.

**`sphinx-autoapi` warnings break the build.**
`conf.py` already installs a logging filter that silences the four
duplicate `ONNX_IMPORTED` descriptions autoapi emits. If new
duplicates appear after a major autoapi release, extend the filter
in `conf.py` rather than disabling `-W`.

**The GitHub-hosted runner has no `pdflatex`.**
That is on purpose: the TikZ figures are committed pre-rendered so
the CI doesn't need a TeX distribution. If you *want* CI to rebuild
the figures, add a step that installs `texlive-latex-base
texlive-latex-extra texlive-pictures` + `dvisvgm` and calls
`make -C docs tikz`. Budget ~3 minutes for the TeX install.
