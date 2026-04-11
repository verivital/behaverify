# 2026_TBA Refactoring Cleanup Report

**Date:** 2026-03-31

## Motivation

`2026_TBA` exists to document and reproduce the **compositional verification** approach
for neuro-symbolic behavior trees: CROWN-verified A/G contracts injected into a stripped
nuXmv SMV, verified by nuXmv.

Monolithic verification — full NN lookup tables embedded directly in nuXmv SMVs — belongs
in `2025_NEUS` (NeuS 2025 paper). When the paper compares monolithic and compositional
results, the monolithic baseline is drawn from `2025_NEUS`, not re-run from `2026_TBA`.
Keeping monolithic infrastructure in `2026_TBA` creates confusion about which approach
the folder represents and inflates the repository with hundreds of megabytes of generated
artifacts.

Per DESIGN-16 (No Dead Code): git history in `2025_NEUS` is the permanent record of
monolithic artifacts. They do not need to be duplicated here.

---

## What Was Deleted and Why

### `examples/` — monolithic artifacts

| Deleted | Reason |
|---|---|
| `grid_world/command.sh`, `make_smv.sh`, `make_tree.sh`, `run_smv.sh`, `run_smv_all.sh`, `time_make_smv.sh` | Monolithic SMV generation and execution scripts |
| `grid_world/smv/` (21 SMV files) | Generated monolithic SMV artifacts |
| `grid_world/tree/` (30 tree files) | Intermediate generated artifacts for monolithic pipeline |
| `grid_world/networks_all/` (25 ONNX files) | Extended NN set not used by compositional scripts |
| `grid_world/networks_pth/` (25 PTH files) | PyTorch checkpoints; CROWN uses ONNX only |
| `grid_world/images/` (6 PNGs) | Network visualizations; not part of pipeline |
| `grid_world/counter_1.smv`, `counter_2.smv`, `counter_template.tree` | Counter-example artifacts unrelated to compositional pipeline |
| `grid_world/ctl_counter.txt`, `invar_counter.txt`, `sim_small_20.txt` | Monolithic verification output |
| `grid_world/Example.tree` | Scratch example; unused |
| `AcasXu_closed_loop/command.sh`, `time_command.sh`, `translation_time.txt` | Monolithic SMV generation and its timing output |
| `AcasXu_closed_loop/acasxu_template_360_backup.tree`, `acasxu_template_360_FAST.tree`, `acasxu_template_720.tree`, `handle_360_backup.py` | Backup and unused variant files; git history is the backup |
| `AcasXu/` (entire folder, ~17 files) | Single-NN ACAS Xu exploration from before the closed-loop compositional pipeline; predates 2026_TBA work |
| `clean_all.sh`, `create_grid.py`, `draw_network.py`, `draw_output.py`, `draw_SIMPLE_output.py`, `parse_nuxmv_output.py`, `parse_SIMPLE_nuxmv_output_stage_FIRST.py`, `parse_SIMPLE_nuxmv_output_stage_LAST.py` | Top-level utility scripts serving only the monolithic pipeline |
| `grid_world_big/` (entire folder) | Monolithic experiments on a larger grid; no compositional work done here |

### `python_script/` — Docker infrastructure

Byte-for-byte copy of `2025_NEUS/python_script/`. Hardcoded to `VENUE = '2025_NEUS'` in
`docker_util.py`. Never updated for 2026_TBA. Entire folder deleted.

### `requirements/` — Docker requirements

Byte-for-byte copy of `2025_NEUS/requirements/`. Not referenced by any compositional
pipeline script. Entire folder deleted.

### `scripts/` — build, timing, and comparison scripts

All subdirectories (`build_scripts/`, `cabal_template_files/`, `comparison_scripts/`,
`encoding_timing_scripts/`, `full_script/`, `partial_timing_scripts/`,
`process_results_scripts/`, `test_scripts/`) were byte-for-byte copies of their
`2025_NEUS` counterparts. They reference ANSR/blueROV/light-controller experiments that
do not exist in `2026_TBA/examples/`. `clean_docker.sh` was also deleted (Docker is not
used).

Of the 17 nuXmv command files, 14 were deleted. Kept: `command_invar` (ACAS Xu pipeline
default), `command_combo_invar_ctl` (grid world pipeline default), `command_all_invar`
(referenced in `AcasXu_closed_loop/README.md` for manual runs). The deleted command files
cover simulation, LTL, state-counting, and silent timing variants that neither pipeline
references.

### `src/` — code generators and utilities

The compositional pipeline's full import chain was traced from the two entry points
(`run_acas_pipeline.py` → `dsl_to_nuxmv`; `run_compositional_pipeline.py` →
`dsl_with_contracts_to_nuxmv` → `dsl_to_nuxmv`) and found to require exactly 8 modules:

```
dsl_with_contracts_to_nuxmv  (grid world only)
dsl_to_nuxmv
  ├─ behaverify_to_smv → node_creator → behaverify_common
  ├─ serene_functions
  ├─ serene_functions_neural
  └─ check_grammar → (serene_functions, serene_functions_neural, behaverify_common)
```

Everything outside this chain was deleted:

| Deleted | Reason |
|---|---|
| `dsl_to_python.py` + `tick_overwrite/` | Python code generation; not used by either pipeline |
| `dsl_to_haskell.py` + `haskell_file/` | Haskell code generation; not used |
| `dsl_to_latex.py` + `tikz_files/` | LaTeX diagram generation; not used |
| `behaverify_gui.py` | GUI interface; not used |
| `counter_trace.py` | Counter-example trace visualization; not used |
| `create_c_monitor.py`, `create_dsl_monitor.py`, `create_python_monitor.py` | Monitor generation; not used |
| `model_to_dsl.py` | Only referenced by `create_dsl_monitor.py` (also deleted) |
| `testing_repeat.py` | Testing utility; not used |
| `alternative_printing/` (3 files) | Alternative py-trees printing modes; not used |

### `BehaVerify_2025_NEUS.sh`

The monolithic batch runner. Calls `clean_all.sh`, `make_tree.sh`, `time_make_smv.sh`,
`run_smv_all.sh`, and `draw_network.py` — all deleted in the examples refactor. The
filename itself reflects that this was a 2025_NEUS artifact placed here by mistake.

### `Dockerfile`

Hardcoded to `VENUE=2025_NEUS`. Docker is not used in the compositional pipeline.

---

## What Was Kept

| Path | Reason |
|---|---|
| `examples/grid_world/verify_contracts.py` + `.yaml` | CROWN contract verification (core compositional tool) |
| `examples/grid_world/run_pgd_1000_contracts.sh` | Batch PGD runner for five 100%-accurate NNs |
| `examples/grid_world/run_compositional_pipeline.py` | End-to-end grid world pipeline |
| `examples/grid_world/template.tree`, `obstacles_6_18_0.txt` | Pipeline inputs |
| `examples/grid_world/networks/` (7 ONNX files) | Networks used by CROWN |
| `examples/grid_world/contracts/` | BaB-only and PGD contract results |
| `examples/grid_world/results/` | Timing results and PGD analysis report |
| `examples/AcasXu_closed_loop/` (all compositional files) | Full 5-NN closed-loop pipeline |
| `examples/AcasXu_closed_loop/invar.txt` | Monolithic INVAR=true baseline (Serena, `serenegrace`, 49s, 9.6 GB); kept as paper comparison point — see `README.md` note |
| `metamodel/behaverify.tx` + `README.md` | Pinned grammar version for reproducibility |
| `scripts/nuxmv_commands/command_invar` | ACAS Xu pipeline default |
| `scripts/nuxmv_commands/command_combo_invar_ctl` | Grid world pipeline default |
| `scripts/nuxmv_commands/command_all_invar` | Manual nuXmv run (README) |
| `src/` (8 modules) | Full import chain for compositional SMV generation |

---

## Baseline Comparison Policy

When the paper presents a monolithic vs. compositional comparison:

- **Monolithic results** come from `2025_NEUS` (or cite Serena's `invar.txt` directly).
- **Compositional results** come from `2026_TBA/examples/`.

`2026_TBA` does not re-implement monolithic verification. If a monolithic re-run is
needed for a new experiment, it should be added to `2025_NEUS`, not here.
