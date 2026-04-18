"""
run_compositional_pipeline.py

End-to-end compositional verification pipeline for grid-world NSBTs.

Stages:
  1. [CONTRACTS]  Verify A/G contracts via alpha-beta-CROWN
  2. [SMV]        Convert .tree + contracts → contract-based nuXmv SMV
  3. [VERIFY]     Run nuXmv to check INVARSPEC and CTLSPEC
  4. [REPORT]     Write pipeline_report.json with per-step metrics and verdicts

Usage (from REPRODUCIBILITY/2026_TBA/examples/grid_world/):

  python run_compositional_pipeline.py \\
      --onnx    networks/1000__6_18_0__0200_1.onnx \\
      --output  results/compositional/continuous_goals/enabled_pgd/1000__0200 \\
      [--tree       path/to/counter.tree]
      [--config     grid_world_domain_config.yaml]
      [--nuxmv      ../../nuXmv_DL/bin/nuXmv]
      [--nuxmv-cmd  ../../commands/nuxmv_commands/command_combo_invar_ctl]
      [--metamodel  ../../metamodel/behaverify.tx]
      [--skip-contracts]
      [--contracts  path/to/contracts.json]

All defaults are read from pipeline_filepaths_config.yaml.
Individual flags override YAML values for one-off runs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import yaml

_HERE = Path(__file__).parent.resolve()
_TBA  = (_HERE / "../../").resolve()   # 2026_TBA/

# Add 2026_TBA/ to sys.path so that `import pipeline` finds 2026_TBA/pipeline/
if str(_TBA) not in sys.path:
    sys.path.insert(0, str(_TBA))

from pipeline.symbolic.nuxmv.run_nuxmv_verification import run_nuxmv
from pipeline.write_pipeline_report                import write_report
from pipeline.resolve_pipeline_paths               import setup
from convert_contracts_to_smv                      import run_smv_generation
import verify_grid_world_contracts as _vc


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def _load_pipeline_config(path: Path = _HERE / "pipeline_filepaths_config.yaml") -> dict:
    """Load pipeline_filepaths_config.yaml. Paths inside are relative to grid_world/."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


_pcfg = _load_pipeline_config()
_paths = _pcfg["paths"]
_smv   = _pcfg["smv"]

_DEFAULT_CONFIG    = (_HERE / _paths["contracts_config"]).resolve()
_DEFAULT_NUXMV     = (_HERE / _paths["nuxmv_bin"]).resolve()
_DEFAULT_NUXMV_CMD = (_HERE / _paths["nuxmv_cmd"]).resolve()
_DEFAULT_METAMODEL = (_HERE / _paths["metamodel"]).resolve()
_COUNTER_TEMPLATE  = (_HERE / _paths["counter_template"]).resolve()

# SMV converter arguments — passed through to convert_contracts_to_smv, not hardcoded there
_SMV_CFG = {
    "neural_var": _smv["neural_var"],
    "pos_x":      _smv["pos_x"],
    "pos_y":      _smv["pos_y"],
    "domain":     _smv["domain"],
    "src_dir":    str((_HERE / "../../src").resolve()),
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="End-to-end compositional verification pipeline for grid-world NSBTs."
    )
    p.add_argument("--onnx",      required=True,  help="Path to the ONNX network file")
    p.add_argument("--output",    required=True,  help="Output directory for all generated files")
    p.add_argument("--tree",      default=None,   help=".tree file; auto-generated from counter_template if omitted")
    p.add_argument("--config",    default=str(_DEFAULT_CONFIG),    help=f"grid_world_config YAML (default: {_DEFAULT_CONFIG})")
    p.add_argument("--nuxmv",     default=str(_DEFAULT_NUXMV),     help=f"nuXmv binary (default: {_DEFAULT_NUXMV})")
    p.add_argument("--nuxmv-cmd", default=str(_DEFAULT_NUXMV_CMD), dest="nuxmv_cmd",
                   help=f"nuXmv command file (default: {_DEFAULT_NUXMV_CMD})")
    p.add_argument("--metamodel", default=str(_DEFAULT_METAMODEL), help=f"behaverify.tx path (default: {_DEFAULT_METAMODEL})")
    p.add_argument("--skip-contracts", action="store_true", help="Skip Step 1 and use an existing contracts JSON")
    p.add_argument("--contracts", default=None, help="Explicit contracts JSON path (overrides default output_dir/contracts.json)")
    return p


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = _build_parser().parse_args()

    pipeline_start = time.perf_counter()

    ctx = setup(args, _COUNTER_TEMPLATE)

    if ctx["skip_contracts"]:
        print("\n[1/3] CONTRACT VERIFICATION — skipped (using existing JSON)")
        with open(ctx["contracts_path"], encoding="utf-8") as f:
            summary = json.load(f).get("summary", {})
        contracts_metrics = {
            "wall_sec": 0.0, "peak_rss_kb": 0, "peak_traced_bytes": 0,
            "sat":     summary.get("SAT", 0),
            "unsat":   summary.get("UNSAT", 0),
            "timeout": summary.get("TIMEOUT", 0),
            "total":   summary.get("total", 0),
            "skipped": True,
        }
    else:
        cfg = _vc.load_config(str(ctx["config_path"]))
        # CROWN concatenates paths with string ops — absolute paths produce
        # doubled slashes. Provide CWD-relative paths instead.
        cfg["onnx_path"]   = os.path.relpath(ctx["onnx_path"])
        cfg["output_path"] = os.path.relpath(ctx["contracts_path"])
        contracts_metrics = _vc.run_verification(cfg)

    smv_metrics   = run_smv_generation(ctx, _SMV_CFG)
    nuxmv_metrics = run_nuxmv(ctx)

    write_report(
        ctx["report_path"],
        steps={
            "contracts":          contracts_metrics,
            "smv_generation":     smv_metrics,
            "nuxmv_verification": nuxmv_metrics,
        },
        total_wall_sec=time.perf_counter() - pipeline_start,
        extra={
            "network":   ctx["network_name"],
            "onnx_path": str(ctx["onnx_path"]),
            "tree_path": str(ctx["tree_path"]),
        },
    )


if __name__ == "__main__":
    main()
