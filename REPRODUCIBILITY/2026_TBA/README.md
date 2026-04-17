# Compositional Verification of Neuro-Symbolic Behavior Trees (NSBTs)

This directory contains the compositional verification pipeline for NSBTs, extending
the monolithic BehaVerify approach with Assume-Guarantee (A/G) contracts verified via
alpha-beta-CROWN.

Two examples are included:
- **Grid world** — 1-NN, 7x7 grid, 18 obstacles, 38 contracts
- **ACAS Xu closed-loop** — 5-NN, 490 contracts (269 SAT / 221 UNSAT via PGD)

---

## Repository Layout

```
2026_TBA/
├── examples/
│   ├── grid_world/         # 1-NN grid world pipeline (see examples/grid_world/README.md)
│   └── AcasXu_closed_loop/ # 5-NN ACAS Xu pipeline  (see examples/AcasXu_closed_loop/README.md)
├── metamodel/              # Pinned BehaVerify TextX grammar
├── reports/                # Refactoring logs, session snapshots, and result summaries
├── commands/nuxmv_commands/ # nuXmv command files used by both pipelines
├── src/                    # BehaVerify source modules (compositional pipeline only)
└── nuXmv_DL/               # nuXmv binary (not committed, download separately)
```

---

## Prerequisites

### 1. BehaVerify

Install from the repository root:

```bash
pip install -e .
```

> **Note: this pipeline does NOT use the installed pip package at runtime.**
> `2026_TBA/src/` contains a local copy of the BehaVerify source, including
> `dsl_with_contracts_to_nuxmv.py` — a contract injection module that is not
> part of the published package. All pipeline scripts add `2026_TBA/src/` to
> `sys.path` and import from there directly. The pip install is only needed for
> dependencies (textX, py-trees, etc.). If you upgrade the `behaverify` package
> after cloning, this pipeline may still work, but is not guaranteed to — it was
> developed against a specific internal version.

### 2. nuXmv 2.1.0

nuXmv cannot be redistributed. Download and extract into `REPRODUCIBILITY/2026_TBA/`:

```bash
wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz -O nuXmv_DL.tar.xz
tar -xf nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
chmod +x nuXmv_DL/bin/nuXmv
```

The pipeline scripts default to `nuXmv_DL/bin/nuXmv` inside `REPRODUCIBILITY/2026_TBA/`.
Override with `--nuxmv` if your binary is elsewhere.

### 3. Extra Python dependencies

After the base `pip install -e .`, install the small set of extras this pipeline needs:

```bash
pip install -r REPRODUCIBILITY/2026_TBA/requirements.txt
```

Currently this adds only `gradio` (used by the interactive contract explorer app).
Everything else — `matplotlib`, `numpy`, `pandas`, `onnxruntime`, `PyYAML` — is
already pulled in by the base `behaverify` install.

### 4. alpha-beta-CROWN (only needed to re-verify contracts)

Pre-computed contracts are already committed. Only needed for re-running CROWN from scratch:

```bash
cd REPRODUCIBILITY/2026_TBA
git clone https://github.com/Verified-Intelligence/alpha-beta-CROWN alpha-beta-CROWN
pip install -r alpha-beta-CROWN/complete_verifier/requirements/requirements.txt
```

---

## Examples

| Example | Description | README |
|---|---|---|
| `examples/grid_world/` | 1-NN drone navigation; 38 A/G contracts; continuous mode (PGD reveals UNSAT on non-integer goals) and discrete mode (eps=0, replicates 2025_NEUS integer-point safety claim compositionally) | [README](examples/grid_world/README.md) |
| `examples/AcasXu_closed_loop/` | 5-NN closed-loop aircraft avoidance; 490 contracts; 221 TIMEOUT resolved as UNSAT via PGD | [README](examples/AcasXu_closed_loop/README.md) |
