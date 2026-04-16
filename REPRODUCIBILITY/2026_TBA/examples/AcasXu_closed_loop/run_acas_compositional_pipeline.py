"""
run_acas_compositional_pipeline.py

End-to-end compositional verification pipeline for the ACAS Xu 5-NN closed-loop NSBT.

Stages:
  1. [TREE]     Generate acas_360.tree from acas_template_360.tree via generate_acas_tree.py
  2. [SMV]      Convert .tree → base nuXmv SMV via dsl_to_nuxmv.py
  3. [PATCH]    Replace 5 NN lookup-table DEFINE blocks with non-deterministic VAR +
                INVAR constraints derived from the verified A/G contracts JSON
  4. [VERIFY]   Run nuXmv to check INVARSPEC (distance >= 200)
  5. [REPORT]   Write JSON report with per-step timing and verdicts

SMV variable structure (from acas_360.smv):
  command_stage_0          -- a_prev (blackboard VAR; which NN was last chosen)
  command_stage_5          -- final NN output after tree execution
  network_k_1_stage_0      -- NN_k lookup-table DEFINE (k = 1..5)
  x_var_stage_0            -- ownship x position (env VAR, [0..10])
  y_var_stage_0            -- ownship y position (env VAR, [0..10])
  x_mult_stage_0           -- x sign (env VAR, {-1, 1})
  y_mult_stage_0           -- y sign (env VAR, {-1, 1})
  heading_own_var_stage_0  -- heading index (env VAR, [0..39])

INVAR format (one per dangerous (state, advisory) pair in each SAT contract):
  INVAR (system.command_stage_0 = <a_prev>
       & system.heading_own_var_stage_0 = <h>
       & system.x_mult_stage_0 = <xm>
       & system.y_mult_stage_0 = <ym>
       & system.x_var_stage_0 = <xv>
       & system.y_var_stage_0 = <yv>)
       -> system.command_stage_5 != <forbidden>;

Usage (from AcasXu_closed_loop/):
  python run_acas_compositional_pipeline.py \\
      --contracts contracts/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \\
      --output    results/compositional/continuous_goals/enabled_pgd/nn1 \\
      [--nuxmv    ../../nuXmv_DL/bin/nuXmv] \\
      [--nuxmv-cmd ../../scripts/nuxmv_commands/command_invar] \\
      [--skip-tree]   # reuse existing tree/acas_360.tree
      [--skip-smv]    # reuse existing smv/acas_360.smv
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
try:
    import resource
except ImportError:
    resource = None  # Windows: resource module not available
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path

_HERE     = Path(__file__).parent.resolve()
_REPO     = (_HERE / "../../../../").resolve()

DEFAULT_NUXMV     = _HERE / "../../nuXmv_DL/bin/nuXmv"
DEFAULT_NUXMV_CMD = _HERE / "../../scripts/nuxmv_commands/command_invar"
DEFAULT_METAMODEL = _HERE / "../../metamodel/behaverify.tx"
DEFAULT_SRC       = _HERE / "../../src"

ADVISORIES = ['clear', 'weak_left', 'weak_right', 'strong_left', 'strong_right']

# SMV variable names (from inspecting acas_360.smv)
SMV_COMMAND_PREV  = "command_stage_0"    # a_prev
SMV_COMMAND_FINAL = "command_stage_5"    # NN output after tree
SMV_X_VAR         = "x_var_stage_0"
SMV_Y_VAR         = "y_var_stage_0"
SMV_X_MULT        = "x_mult_stage_0"
SMV_Y_MULT        = "y_mult_stage_0"
SMV_HEADING       = "heading_own_var_stage_0"


# ---------------------------------------------------------------------------
# Memory helpers
# ---------------------------------------------------------------------------

def _self_rss_kb() -> int:
    if resource is None:
        return 0
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

def _children_rss_kb() -> int:
    if resource is None:
        return 0
    return resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss


# ---------------------------------------------------------------------------
# Step 1 — Tree generation
# ---------------------------------------------------------------------------

def run_tree_generation(ctx: dict) -> dict:
    print("\n" + "=" * 60)
    print("[1/4] TREE GENERATION")
    print("=" * 60)

    if ctx["skip_tree"] and ctx["tree_path"].exists():
        print(f"  Skipped — reusing {ctx['tree_path']}")
        return {"wall_sec": 0.0, "skipped": True}

    t0 = time.perf_counter()

    # Run as subprocess so the module-level write logic executes cleanly
    # (generate_acas_tree.py writes directly to ./tree/acas_360.tree).
    result = subprocess.run(
        [sys.executable, str(_HERE / "generate_acas_tree.py")],
        cwd=str(_HERE),
        capture_output=True,
        text=True,
        check=False,
    )
    wall_sec = time.perf_counter() - t0

    if result.returncode != 0:
        print(f"  ERROR: generate_acas_tree.py failed:\n{result.stderr}")
        raise RuntimeError("Tree generation failed")

    print(f"  Generated {ctx['tree_path']}  ({wall_sec:.1f}s)")
    return {"wall_sec": round(wall_sec, 3), "skipped": False}


# ---------------------------------------------------------------------------
# Step 2 — Base SMV generation
# ---------------------------------------------------------------------------

def run_smv_generation(ctx: dict) -> dict:
    print("\n" + "=" * 60)
    print("[2/4] BASE SMV GENERATION")
    print("=" * 60)

    if ctx["skip_smv"] and ctx["base_smv_path"].exists():
        print(f"  Skipped — reusing {ctx['base_smv_path']}")
        return {"wall_sec": 0.0, "skipped": True}

    src_dir = str(DEFAULT_SRC.resolve())
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    import dsl_to_nuxmv as _dsl  # noqa: PLC0415

    tracemalloc.start()
    t0 = time.perf_counter()

    # ONNX paths in the tree are relative to tree/, so chdir there for parsing
    _orig_cwd = os.getcwd()
    os.chdir(str(ctx["tree_path"].parent))
    try:
        _dsl.dsl_to_nuxmv(
            str(ctx["metamodel"]),
            str(ctx["tree_path"]),
            str(ctx["base_smv_path"]),
            False, False, False, False,
            10000,       # recursion_limit
            False,       # keep_stage_0
            True,        # skip_grammar_check (--no_checks)
            None,        # record_times
        )
    finally:
        os.chdir(_orig_cwd)

    wall_sec = time.perf_counter() - t0
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss = _self_rss_kb()

    smv_lines = ctx["base_smv_path"].read_text().count("\n")
    print(f"  Generated {ctx['base_smv_path']}  ({wall_sec:.1f}s, {smv_lines} lines)")
    return {
        "wall_sec":          round(wall_sec, 3),
        "peak_rss_kb":       rss,
        "peak_traced_bytes": peak_traced,
        "smv_lines":         smv_lines,
        "skipped":           False,
    }


# ---------------------------------------------------------------------------
# Step 3 — SMV patching: replace NN tables with non-det VAR + INVAR contracts
# ---------------------------------------------------------------------------

def _load_sat_contracts(verified_path: Path, spec_path: Path) -> list[dict]:
    """
    Load SAT contracts, joining the verified-results JSON with the original
    spec JSON to recover fields (like a_prev) that verify_acas_contracts.py
    did not copy through.
    """
    with open(verified_path, encoding="utf-8") as f:
        verified = json.load(f)
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)

    spec_by_id = {c["id"]: c for c in spec["contracts"]}
    sat = []
    for c in verified["contracts"]:
        if c["status"] != "SAT":
            continue
        merged = {**spec_by_id[c["id"]], **c}   # spec fields + status/wall_sec from verified
        sat.append(merged)

    print(f"  {len(sat)} SAT contracts loaded (of {len(verified['contracts'])} total)")
    return sat


def _remove_nn_defines(smv: str) -> tuple[str, int]:
    """Remove all 5 network_k_1_stage_0 DEFINE case blocks."""
    total_removed = 0
    for k in range(1, 6):
        var = f"network_{k}_1_stage_0"
        pattern = (
            r" +" + re.escape(var) + r" :=\s+"
            r"case\s+"
            r".*?"
            r"esac;\n"
        )
        before = smv.count("\n")
        smv, n = re.subn(pattern, "", smv, flags=re.DOTALL)
        if n == 0:
            raise ValueError(f"DEFINE block for '{var}' not found in SMV.")
        total_removed += before - smv.count("\n")
    return smv, total_removed


def _add_command_free_var(smv: str) -> str:
    """
    Replace the 5 TRUE-branch NN-table references with a single fresh free VAR.

    Original staging (after NN DEFINE removed):
        command_stage_k :=
            case
                !(call_k_1.active) : command_stage_{k-1};
                TRUE               : network_k_1_stage_0;  ← undefined now
            esac;

    Fix: declare  nn_output_free : {advisory domain}  as a free VAR in the
    VAR section, then replace each TRUE branch with nn_output_free.  Since at
    most one NN runs per tick, a single shared free variable is sound — and it
    avoids the symbolic-set vs. symbolic-enum type error that would arise from
    using an inline {a,b,c,...} literal in a DEFINE case expression.
    """
    domain = "{" + ", ".join(ADVISORIES) + "}"
    # 1. Add the free VAR declaration
    new_var = f"        nn_output_free : {domain};\n"
    marker = "--START OF BLACKBOARD VARIABLES DECLARATION\n"
    if marker not in smv:
        raise ValueError("VAR-section marker '--START OF BLACKBOARD VARIABLES DECLARATION' not found.")
    smv = smv.replace(marker, marker + new_var, 1)

    # 2. Point every NN stage's TRUE branch at nn_output_free
    for k in range(1, 6):
        old = f"                TRUE : network_{k}_1_stage_0;"
        new = f"                TRUE : nn_output_free;"
        if old not in smv:
            raise ValueError(f"Expected staging assignment for network_{k}_1_stage_0 not found.")
        smv = smv.replace(old, new, 1)

    return smv


def _build_invar_lines(contracts: list[dict]) -> list[str]:
    """
    For each SAT contract, enumerate its dangerous (x_mag, y_mag) states and
    emit one INVAR per state (point constraints — exact state match).

    Sound because: CROWN verified the property over the bounding box in NN input
    space, and each dangerous state's inputs are within that box by construction.
    Using exact state conditions rather than bounding-box ranges avoids including
    non-dangerous states that could be on the wrong side of the NN's decision boundary.
    """
    lines = []
    for c in contracts:
        h   = c["heading_own_var"]
        xm  = c["x_sign"]
        ym  = c["y_sign"]
        ap  = c["a_prev"]
        fbd = c["forbidden_advisory"]

        for x_mag, y_mag in c["dangerous_xy"]:
            cond = (
                f"system.{SMV_COMMAND_PREV} = {ap} & "
                f"system.{SMV_HEADING} = {h} & "
                f"system.{SMV_X_MULT} = {xm} & "
                f"system.{SMV_Y_MULT} = {ym} & "
                f"system.{SMV_X_VAR} = {x_mag} & "
                f"system.{SMV_Y_VAR} = {y_mag}"
            )
            lines.append(f"INVAR ({cond}) -> system.{SMV_COMMAND_FINAL} != {fbd};")
    return lines


def _inject_invars(smv: str, invar_lines: list[str]) -> str:
    marker = "--------------SPECIFICATIONS\n"
    if marker not in smv:
        raise ValueError("SPECIFICATIONS marker not found in SMV.")
    block = "-- A/G contract constraints (verified by alpha-beta-CROWN):\n"
    block += "\n".join(invar_lines) + "\n"
    return smv.replace(marker, marker + block, 1)


def run_smv_patch(ctx: dict) -> dict:
    print("\n" + "=" * 60)
    print("[3/4] SMV PATCHING (contract injection)")
    print("=" * 60)

    contracts = _load_sat_contracts(ctx["contracts_path"], ctx["spec_path"])

    t0 = time.perf_counter()
    smv = ctx["base_smv_path"].read_text(encoding="utf-8").replace("\r\n", "\n")

    smv, lines_removed = _remove_nn_defines(smv)
    print(f"  Removed 5 NN DEFINE blocks ({lines_removed} lines)")

    smv = _add_command_free_var(smv)
    print(f"  Replaced NN table outputs with non-deterministic advisory domain")

    invar_lines = _build_invar_lines(contracts)
    smv = _inject_invars(smv, invar_lines)
    print(f"  Injected {len(invar_lines)} INVAR constraints from {len(contracts)} SAT contracts")

    ctx["patched_smv_path"].write_text(smv, encoding="utf-8")
    wall_sec = time.perf_counter() - t0

    print(f"  Patched SMV: {ctx['patched_smv_path']}  ({wall_sec:.1f}s)")
    return {
        "wall_sec":            round(wall_sec, 3),
        "sat_contracts":       len(contracts),
        "invar_lines":         len(invar_lines),
        "nn_lines_removed":    lines_removed,
    }


# ---------------------------------------------------------------------------
# Step 4 — nuXmv verification
# ---------------------------------------------------------------------------

def _parse_verdicts(text: str) -> dict:
    invar = re.search(r"-- invariant .+ is (true|false)", text)
    return {"invarspec": invar.group(1) if invar else None}


def run_nuxmv(ctx: dict) -> dict:
    print("\n" + "=" * 60)
    print("[4/4] NUXMV VERIFICATION")
    print("=" * 60)

    cmd = [str(ctx["nuxmv_bin"]), "-source", str(ctx["nuxmv_cmd"]), str(ctx["patched_smv_path"])]
    print(f"  Command: {' '.join(cmd)}")

    rss_before = _children_rss_kb()
    t0 = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    wall_sec = time.perf_counter() - t0
    rss_after = _children_rss_kb()

    output = result.stdout + result.stderr
    ctx["nuxmv_out_path"].write_text(output, encoding="utf-8")

    verdicts = _parse_verdicts(output)
    print(f"\n  [nuxmv] {wall_sec:.1f}s  |  INVARSPEC={verdicts['invarspec']}")
    print(f"  Output: {ctx['nuxmv_out_path']}")
    return {
        "wall_sec":    round(wall_sec, 3),
        "peak_rss_kb": rss_after - rss_before,
        "returncode":  result.returncode,
        **verdicts,
    }


# ---------------------------------------------------------------------------
# Step 5 — Report
# ---------------------------------------------------------------------------

def write_report(ctx: dict, steps: dict, total_wall_sec: float) -> None:
    invar = steps["nuxmv"]["invarspec"]
    report = {
        "timestamp":      datetime.datetime.now().isoformat(),
        "contracts_path": str(ctx["contracts_path"]),
        "steps":          steps,
        "total_wall_sec": round(total_wall_sec, 3),
        "verdict":        f"INVAR={invar}",
    }
    ctx["report_path"].write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    sp = steps["smv_patch"]
    print(f"  Contracts : {sp['sat_contracts']} SAT → {sp['invar_lines']} INVARs injected")
    print(f"  NN tables : {sp['nn_lines_removed']} lines removed from SMV")
    print(f"  nuXmv     : INVARSPEC={invar}")
    print(f"  Timing    : tree={steps['tree']['wall_sec']:.1f}s  "
          f"smv={steps['smv']['wall_sec']:.1f}s  "
          f"patch={steps['smv_patch']['wall_sec']:.1f}s  "
          f"nuxmv={steps['nuxmv']['wall_sec']:.1f}s  "
          f"total={total_wall_sec:.1f}s")
    print(f"  Report    : {ctx['report_path']}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        description="End-to-end compositional verification pipeline for ACAS Xu 5-NN NSBT."
    )
    p.add_argument("--contracts",  required=True,
                   help="Path to verified contracts JSON (e.g. contracts/continuous_goals/enabled_pgd/aprev_clear_crown_results.json)")
    p.add_argument("--spec",       default="contracts/continuous_goals/contract_specs_eps1e4.json",
                   help="Path to original contract spec JSON (default: contracts/continuous_goals/contract_specs_eps1e4.json)")
    p.add_argument("--output",     required=True,
                   help="Output directory for patched SMV, nuXmv output, and report")
    p.add_argument("--nuxmv",      default=str(DEFAULT_NUXMV),
                   help=f"nuXmv binary path (default: {DEFAULT_NUXMV})")
    p.add_argument("--nuxmv-cmd",  default=str(DEFAULT_NUXMV_CMD), dest="nuxmv_cmd",
                   help=f"nuXmv command file (default: {DEFAULT_NUXMV_CMD})")
    p.add_argument("--metamodel",  default=str(DEFAULT_METAMODEL),
                   help=f"behaverify.tx path (default: {DEFAULT_METAMODEL})")
    p.add_argument("--skip-tree",  action="store_true",
                   help="Skip tree generation; reuse tree/acas_360.tree if it exists")
    p.add_argument("--skip-smv",   action="store_true",
                   help="Skip base SMV generation; reuse smv/acas_360.smv if it exists")
    args = p.parse_args()

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    ctx = {
        "contracts_path":  Path(args.contracts).resolve(),
        "spec_path":       Path(args.spec).resolve(),
        "tree_path":       _HERE / "tree" / "acas_360.tree",
        "base_smv_path":   _HERE / "smv"  / "acas_360.smv",
        "patched_smv_path": output_dir / "acas_360_contracts.smv",
        "nuxmv_out_path":  output_dir / "nuxmv_output.txt",
        "report_path":     output_dir / "pipeline_report.json",
        "metamodel":       Path(args.metamodel).resolve(),
        "nuxmv_bin":       Path(args.nuxmv).resolve(),
        "nuxmv_cmd":       Path(args.nuxmv_cmd).resolve(),
        "skip_tree":       args.skip_tree,
        "skip_smv":        args.skip_smv,
    }

    # Ensure tree/ and smv/ dirs exist
    ((_HERE / "tree")).mkdir(exist_ok=True)
    ((_HERE / "smv")).mkdir(exist_ok=True)

    t_start = time.perf_counter()

    tree_metrics  = run_tree_generation(ctx)
    smv_metrics   = run_smv_generation(ctx)
    patch_metrics = run_smv_patch(ctx)
    nuxmv_metrics = run_nuxmv(ctx)

    total = time.perf_counter() - t_start

    write_report(ctx, {
        "tree":      tree_metrics,
        "smv":       smv_metrics,
        "smv_patch": patch_metrics,
        "nuxmv":     nuxmv_metrics,
    }, total)


if __name__ == "__main__":
    main()
