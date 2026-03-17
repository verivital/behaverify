"""
run_compositional_pipeline.py

End-to-end compositional verification pipeline for grid-world NSBTs.

Given an ONNX network (and optionally a .tree file), runs all four stages and
records timing and memory for each step:

  1. [CONTRACTS]  Verify A/G contracts via alpha-beta-CROWN
  2. [SMV]        Convert .tree + contracts → contract-based nuXmv SMV
  3. [VERIFY]     Run nuXmv to check INVARSPEC and CTLSPEC
  4. [REPORT]     Write JSON report with per-step timing, memory, and verdicts

Usage (from REPRODUCIBILITY/2025_NEUS/examples/grid_world/):

  python run_compositional_pipeline.py \\
      --onnx  networks/1000__6_18_0__0200_1.onnx \\
      --output results/compositional/1000__0200 \\
      [--tree  tree/counter_1.tree]          # optional; auto-generated if absent
      [--config verify_contracts.yaml]       # base grid/obstacle YAML
      [--nuxmv ../../nuXmv_DL/bin/nuXmv]    # nuXmv binary path
      [--nuxmv-cmd ../../scripts/nuxmv_commands/command_combo_invar_ctl]
      [--metamodel ../../metamodel/behaverify.tx]
      [--skip-contracts]                     # skip Step 1, use existing JSON
      [--contracts PATH]                     # explicit contracts JSON path
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import resource
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Defaults (relative to this script's directory)
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()

DEFAULT_CONFIG   = _HERE / "verify_contracts.yaml"
DEFAULT_NUXMV    = _HERE / "../../nuXmv_DL/bin/nuXmv"
DEFAULT_NUXMV_CMD = _HERE / "../../scripts/nuxmv_commands/command_combo_invar_ctl"
DEFAULT_METAMODEL = _HERE / "../../metamodel/behaverify.tx"
COUNTER_TEMPLATE  = _HERE / "counter_template.tree"

# Fixed grid-world SMV converter arguments (counter_N.tree convention)
NEURAL_VAR = "network"
POS_X      = "drone_x"
POS_Y      = "drone_y"
DOMAIN     = ["left", "right", "up", "down", "no_action"]

# ---------------------------------------------------------------------------
# Memory helpers
# ---------------------------------------------------------------------------

def _self_rss_kb() -> int:
    """Current process peak RSS in KB (Linux: ru_maxrss is KB)."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def _children_rss_kb() -> int:
    """Peak RSS of all waited child processes in KB."""
    return resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss


# ---------------------------------------------------------------------------
# Step 0 — Setup
# ---------------------------------------------------------------------------

def setup(args: argparse.Namespace) -> dict[str, Any]:
    """Resolve paths, create output directory, generate tree if needed."""
    onnx_path    = Path(args.onnx).resolve()
    output_dir   = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    network_name = onnx_path.stem  # e.g. "1000__6_18_0__0200_1"

    # Tree: use provided or auto-generate from counter_template
    if args.tree:
        tree_path = Path(args.tree).resolve()
    else:
        tree_path = output_dir / f"{network_name}.tree"
        template_text = COUNTER_TEMPLATE.read_text(encoding="utf-8")
        # dsl_to_nuxmv.py resolves the ONNX source as:
        #   file_prefix + '/' + source   (string concat, not os.path.join)
        # where file_prefix = tree_file.rsplit('/', 1)[0].
        # Use a relative path from the tree file's directory so the concat
        # produces a valid (un-canonicalized) path that the OS will resolve.
        onnx_rel = os.path.relpath(onnx_path, tree_path.parent)
        tree_text = template_text.replace("REPLACE_SOURCE", onnx_rel)
        tree_path.write_text(tree_text, encoding="utf-8")
        print(f"[setup] Auto-generated tree: {tree_path}")

    # Derived paths
    contracts_path = Path(args.contracts).resolve() if args.contracts else output_dir / "contracts.json"
    smv_path       = output_dir / f"{network_name}_contracts.smv"
    nuxmv_out_path = output_dir / "nuxmv_output.txt"
    report_path    = output_dir / "pipeline_report.json"

    return {
        "network_name":   network_name,
        "onnx_path":      onnx_path,
        "tree_path":      tree_path,
        "contracts_path": contracts_path,
        "smv_path":       smv_path,
        "nuxmv_out_path": nuxmv_out_path,
        "report_path":    report_path,
        "output_dir":     output_dir,
        "config_path":    Path(args.config).resolve(),
        "nuxmv_bin":      Path(args.nuxmv).resolve(),
        "nuxmv_cmd":      Path(args.nuxmv_cmd).resolve(),
        "metamodel":      Path(args.metamodel).resolve(),
        "skip_contracts": args.skip_contracts,
    }


# ---------------------------------------------------------------------------
# Step 1 — Contract verification
# ---------------------------------------------------------------------------

def run_contracts(ctx: dict[str, Any]) -> dict[str, Any]:
    """Verify A/G contracts via alpha-beta-CROWN. Returns step metrics."""
    print("\n" + "=" * 60)
    print("[1/3] CONTRACT VERIFICATION")
    print("=" * 60)

    # verify_contracts.py uses module-level load_config() with a default
    # path of "verify_contracts.yaml" relative to CWD.  We must be in the
    # grid_world directory (which is the case when called from there), then
    # override onnx_path and output_path in the cfg dict before calling
    # run_verification.
    import verify_contracts as _vc  # noqa: PLC0415 (intentional late import)

    cfg = _vc.load_config(str(ctx["config_path"]))
    # CROWN joins its output dir with the model path via string concatenation,
    # so absolute paths produce doubled slashes.  Use CWD-relative paths instead
    # (the pipeline must be run from grid_world/ so CWD is always grid_world/).
    cfg["onnx_path"]   = os.path.relpath(ctx["onnx_path"])
    cfg["output_path"] = os.path.relpath(ctx["contracts_path"])

    tracemalloc.start()
    rss_before = _self_rss_kb()
    t0 = time.perf_counter()

    _vc.run_verification(cfg)

    wall_sec = time.perf_counter() - t0
    rss_after = _self_rss_kb()
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Parse summary from the written JSON
    with open(ctx["contracts_path"], encoding="utf-8") as f:
        report = json.load(f)
    summary = report.get("summary", {})

    metrics = {
        "wall_sec":    round(wall_sec, 3),
        "peak_rss_kb": rss_after,          # monotonically increasing; "at least this much"
        "peak_traced_bytes": peak_traced,
        "sat":         summary.get("SAT", 0),
        "unsat":       summary.get("UNSAT", 0),
        "timeout":     summary.get("TIMEOUT", 0),
        "total":       summary.get("total", 0),
        "skipped":     False,
    }
    print(f"\n[contracts] {wall_sec:.1f}s  |  peak RSS ≥{rss_after} KB  |  "
          f"SAT={metrics['sat']} UNSAT={metrics['unsat']} TIMEOUT={metrics['timeout']}")
    return metrics


def skip_contracts(ctx: dict[str, Any]) -> dict[str, Any]:
    """Load existing contracts JSON and return skipped-step metrics."""
    print("\n[1/3] CONTRACT VERIFICATION — skipped (using existing JSON)")
    with open(ctx["contracts_path"], encoding="utf-8") as f:
        report = json.load(f)
    summary = report.get("summary", {})
    return {
        "wall_sec":    0.0,
        "peak_rss_kb": 0,
        "peak_traced_bytes": 0,
        "sat":         summary.get("SAT", 0),
        "unsat":       summary.get("UNSAT", 0),
        "timeout":     summary.get("TIMEOUT", 0),
        "total":       summary.get("total", 0),
        "skipped":     True,
    }


# ---------------------------------------------------------------------------
# Step 2 — SMV generation
# ---------------------------------------------------------------------------

def run_smv_generation(ctx: dict[str, Any]) -> dict[str, Any]:
    """Convert .tree + contracts → contract-based nuXmv SMV. Returns metrics."""
    print("\n" + "=" * 60)
    print("[2/3] SMV GENERATION")
    print("=" * 60)

    src_dir = str((_HERE / "../../src").resolve())
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    import dsl_with_contracts_to_nuxmv as _conv  # noqa: PLC0415

    tracemalloc.start()
    rss_before = _self_rss_kb()
    t0 = time.perf_counter()

    _conv.dsl_with_contracts_to_nuxmv(
        metamodel_file   = str(ctx["metamodel"]),
        tree_file        = str(ctx["tree_path"]),
        output_file      = str(ctx["smv_path"]),
        contracts_file   = str(ctx["contracts_path"]),
        neural_var       = NEURAL_VAR,
        pos_x            = POS_X,
        pos_y            = POS_Y,
        domain           = DOMAIN,
        dir_map          = _conv.DEFAULT_DIR_MAP,
        skip_grammar_check = True,
    )

    wall_sec = time.perf_counter() - t0
    rss_after = _self_rss_kb()
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Count how many INVARs were injected (= SAT contracts loaded)
    with open(ctx["contracts_path"], encoding="utf-8") as f:
        contracts_data = json.load(f)
    sat_injected = sum(1 for c in contracts_data.get("contracts", []) if c["status"] == "SAT")

    metrics = {
        "wall_sec":              round(wall_sec, 3),
        "peak_rss_kb":           rss_after,
        "peak_traced_bytes":     peak_traced,
        "sat_contracts_injected": sat_injected,
    }
    print(f"\n[smv] {wall_sec:.1f}s  |  peak RSS ≥{rss_after} KB  |  "
          f"{sat_injected} INVAR constraints injected")
    return metrics


# ---------------------------------------------------------------------------
# Step 3 — nuXmv verification
# ---------------------------------------------------------------------------

def _parse_verdicts(output_text: str) -> dict[str, str | None]:
    """Extract INVARSPEC and CTLSPEC verdicts from nuXmv stdout."""
    invar_match = re.search(r"-- invariant .+ is (true|false)", output_text)
    ctl_match   = re.search(r"-- specification .+ is (true|false)", output_text)
    return {
        "invarspec": invar_match.group(1) if invar_match else None,
        "ctlspec":   ctl_match.group(1)   if ctl_match   else None,
    }


def run_nuxmv(ctx: dict[str, Any]) -> dict[str, Any]:
    """Run nuXmv on the contract-based SMV. Returns metrics + verdicts."""
    print("\n" + "=" * 60)
    print("[3/3] NUXMV VERIFICATION")
    print("=" * 60)

    cmd = [str(ctx["nuxmv_bin"]), "-source", str(ctx["nuxmv_cmd"]), str(ctx["smv_path"])]
    print(f"  Command: {' '.join(cmd)}")

    rss_children_before = _children_rss_kb()
    t0 = time.perf_counter()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    wall_sec = time.perf_counter() - t0
    rss_children_after = _children_rss_kb()

    output_text = result.stdout + result.stderr
    ctx["nuxmv_out_path"].write_text(output_text, encoding="utf-8")

    verdicts = _parse_verdicts(output_text)
    metrics = {
        "wall_sec":    round(wall_sec, 3),
        "peak_rss_kb": rss_children_after - rss_children_before,
        "returncode":  result.returncode,
        **verdicts,
    }
    print(f"\n[nuxmv] {wall_sec:.1f}s  |  "
          f"INVARSPEC={verdicts['invarspec']}  CTLSPEC={verdicts['ctlspec']}")
    print(f"  Output saved to: {ctx['nuxmv_out_path']}")
    return metrics


# ---------------------------------------------------------------------------
# Step 4 — Report
# ---------------------------------------------------------------------------

def write_report(ctx: dict[str, Any], steps: dict[str, dict], total_wall_sec: float) -> None:
    """Write pipeline_report.json and print final summary."""
    invar = steps["nuxmv_verification"].get("invarspec")
    ctl   = steps["nuxmv_verification"].get("ctlspec")
    verdict = f"INVAR={invar} CTL={ctl}"

    report = {
        "network":        ctx["network_name"],
        "onnx_path":      str(ctx["onnx_path"]),
        "tree_path":      str(ctx["tree_path"]),
        "timestamp":      datetime.datetime.now().isoformat(),
        "steps":          steps,
        "total_wall_sec": round(total_wall_sec, 3),
        "verdict":        verdict,
    }

    with open(ctx["report_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Network  : {ctx['network_name']}")
    print(f"  Contracts: SAT={steps['contracts']['sat']}  "
          f"UNSAT={steps['contracts']['unsat']}  "
          f"TIMEOUT={steps['contracts']['timeout']}  "
          f"(skipped={steps['contracts']['skipped']})")
    print(f"  SMV      : {steps['smv_generation']['sat_contracts_injected']} INVARs injected")
    print(f"  nuXmv    : INVARSPEC={invar}  CTLSPEC={ctl}")
    print(f"  Timing   : contracts={steps['contracts']['wall_sec']:.1f}s  "
          f"smv={steps['smv_generation']['wall_sec']:.1f}s  "
          f"nuxmv={steps['nuxmv_verification']['wall_sec']:.1f}s  "
          f"total={total_wall_sec:.1f}s")
    print(f"  Verdict  : {verdict}")
    print(f"  Report   : {ctx['report_path']}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        description="End-to-end compositional verification pipeline for grid-world NSBTs."
    )
    p.add_argument("--onnx",      required=True,
                   help="Path to the ONNX network file")
    p.add_argument("--output",    required=True,
                   help="Output directory for all generated files and the report")
    p.add_argument("--tree",      default=None,
                   help="Path to .tree file; auto-generated from counter_template if omitted")
    p.add_argument("--config",    default=str(DEFAULT_CONFIG),
                   help=f"verify_contracts YAML config (default: {DEFAULT_CONFIG})")
    p.add_argument("--nuxmv",     default=str(DEFAULT_NUXMV),
                   help=f"nuXmv binary path (default: {DEFAULT_NUXMV})")
    p.add_argument("--nuxmv-cmd", default=str(DEFAULT_NUXMV_CMD), dest="nuxmv_cmd",
                   help=f"nuXmv command file (default: {DEFAULT_NUXMV_CMD})")
    p.add_argument("--metamodel", default=str(DEFAULT_METAMODEL),
                   help=f"behaverify.tx path (default: {DEFAULT_METAMODEL})")
    p.add_argument("--skip-contracts", action="store_true",
                   help="Skip Step 1 and use an existing contracts JSON")
    p.add_argument("--contracts", default=None,
                   help="Explicit path to contracts JSON (overrides default output_dir/contracts.json)")
    args = p.parse_args()

    pipeline_start = time.perf_counter()

    ctx = setup(args)

    # Step 1
    if ctx["skip_contracts"]:
        contracts_metrics = skip_contracts(ctx)
    else:
        contracts_metrics = run_contracts(ctx)

    # Step 2
    smv_metrics = run_smv_generation(ctx)

    # Step 3
    nuxmv_metrics = run_nuxmv(ctx)

    total_wall_sec = time.perf_counter() - pipeline_start

    # Step 4
    steps = {
        "contracts":          contracts_metrics,
        "smv_generation":     smv_metrics,
        "nuxmv_verification": nuxmv_metrics,
    }
    write_report(ctx, steps, total_wall_sec)


if __name__ == "__main__":
    main()
