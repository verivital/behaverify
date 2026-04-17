"""
run_acas_compositional_pipeline.py

End-to-end compositional verification pipeline for the ACAS Xu 5-NN closed-loop NSBT.

Stages:
  1. [TREE]     Generate acas_360.tree from acas_template_360.tree via generate_acas_tree.py
  2. [SMV]      Convert .tree → base nuXmv SMV via dsl_to_nuxmv.py
  3. [PATCH]    Replace 5 NN lookup-table DEFINE blocks with non-deterministic VAR +
                INVAR constraints derived from the verified A/G contracts JSON
  4. [VERIFY]   Run nuXmv to check INVARSPEC (distance >= 200)
                Delegates to pipeline/symbolic/nuxmv/run_nuxmv_verification.py
  5. [REPORT]   Write JSON report with per-step timing and verdicts
                Delegates to pipeline/write_pipeline_report.py

SMV variable names are read from verify_acas_contracts_config.yaml (smv_variables section)
rather than hardcoded in this script.

SMV file locations:
  Base SMV  : symbolic/smv/acas_360.smv   (generated once, reused with --skip-smv)
  Patched SMV: <output_dir>/acas_360_contracts.smv

Usage (from AcasXu_closed_loop/):
  python run_acas_compositional_pipeline.py \\
      --contracts contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \\
      --output    results/compositional/continuous_goals/enabled_pgd/aprev_clear \\
      [--nuxmv    ../../nuXmv_DL/bin/nuXmv] \\
      [--nuxmv-cmd ../../commands/nuxmv_commands/command_invar] \\
      [--skip-tree]   # reuse existing tree/acas_360.tree
      [--skip-smv]    # reuse existing symbolic/smv/acas_360.smv
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import tracemalloc
from pathlib import Path

import yaml

_HERE = Path(__file__).parent.resolve()
_TBA  = (_HERE / "../../").resolve()

if str(_TBA) not in sys.path:
    sys.path.insert(0, str(_TBA))

from pipeline.symbolic.nuxmv.run_nuxmv_verification import run_nuxmv
from pipeline.write_pipeline_report                import write_report
from pipeline.resolve_pipeline_paths               import self_rss_kb, children_rss_kb

try:
    import resource as _resource
except ImportError:
    _resource = None  # Windows

DEFAULT_NUXMV     = _HERE / "../../nuXmv_DL/bin/nuXmv"
DEFAULT_NUXMV_CMD = _HERE / "../../commands/nuxmv_commands/command_invar"
DEFAULT_METAMODEL = _HERE / "../../metamodel/behaverify.tx"
DEFAULT_SRC       = _HERE / "../../src"
DEFAULT_CONFIG    = _HERE / "verify_acas_contracts_config.yaml"

ADVISORIES = ['clear', 'weak_left', 'weak_right', 'strong_left', 'strong_right']


# ---------------------------------------------------------------------------
# SMV variable names (read from config)
# ---------------------------------------------------------------------------

def _load_smv_vars(config_path: Path = DEFAULT_CONFIG) -> dict[str, str]:
    """Load SMV variable names from verify_acas_contracts_config.yaml."""
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    smv = cfg.get("smv_variables", {})
    return {
        "command_prev":  smv.get("command_prev",  "command_stage_0"),
        "command_final": smv.get("command_final", "command_stage_5"),
        "x_var":         smv.get("x_var",         "x_var_stage_0"),
        "y_var":         smv.get("y_var",          "y_var_stage_0"),
        "x_mult":        smv.get("x_mult",        "x_mult_stage_0"),
        "y_mult":        smv.get("y_mult",        "y_mult_stage_0"),
        "heading":       smv.get("heading",       "heading_own_var_stage_0"),
    }


# ---------------------------------------------------------------------------
# Step 1 — Tree generation
# ---------------------------------------------------------------------------

def run_tree_generation(ctx: dict) -> dict:
    import subprocess
    print("\n" + "=" * 60)
    print("[1/4] TREE GENERATION")
    print("=" * 60)

    if ctx["skip_tree"] and ctx["tree_path"].exists():
        print(f"  Skipped — reusing {ctx['tree_path']}")
        return {"wall_sec": 0.0, "skipped": True}

    t0 = time.perf_counter()
    result = subprocess.run(
        [sys.executable, str(_HERE / "generate_acas_tree.py")],
        cwd=str(_HERE), capture_output=True, text=True, check=False,
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

    _orig_cwd = os.getcwd()
    os.chdir(str(ctx["tree_path"].parent))
    try:
        _dsl.dsl_to_nuxmv(
            str(ctx["metamodel"]),
            str(ctx["tree_path"]),
            str(ctx["base_smv_path"]),
            False, False, False, False,
            10000, False, True, None,
        )
    finally:
        os.chdir(_orig_cwd)

    wall_sec = time.perf_counter() - t0
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss = self_rss_kb()

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
    with open(verified_path, encoding="utf-8") as f:
        verified = json.load(f)
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)

    spec_by_id = {c["id"]: c for c in spec["contracts"]}
    sat = []
    for c in verified["contracts"]:
        if c["status"] != "SAT":
            continue
        merged = {**spec_by_id[c["id"]], **c}
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

    Declares  nn_output_free : {advisory domain}  in the VAR section, then
    replaces each TRUE branch with nn_output_free.  A single shared free
    variable is sound — at most one NN runs per tick.
    """
    domain = "{" + ", ".join(ADVISORIES) + "}"
    new_var = f"        nn_output_free : {domain};\n"
    marker = "--START OF BLACKBOARD VARIABLES DECLARATION\n"
    if marker not in smv:
        raise ValueError("VAR-section marker '--START OF BLACKBOARD VARIABLES DECLARATION' not found.")
    smv = smv.replace(marker, marker + new_var, 1)

    for k in range(1, 6):
        old = f"                TRUE : network_{k}_1_stage_0;"
        new = f"                TRUE : nn_output_free;"
        if old not in smv:
            raise ValueError(f"Expected staging assignment for network_{k}_1_stage_0 not found.")
        smv = smv.replace(old, new, 1)

    return smv


def _build_invar_lines(contracts: list[dict], smv_vars: dict[str, str]) -> list[str]:
    """
    Emit one INVAR per dangerous (state, advisory) pair in each SAT contract.

    Uses smv_vars to look up SMV variable names so they don't need to be
    hardcoded in this function.
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
                f"system.{smv_vars['command_prev']} = {ap} & "
                f"system.{smv_vars['heading']} = {h} & "
                f"system.{smv_vars['x_mult']} = {xm} & "
                f"system.{smv_vars['y_mult']} = {ym} & "
                f"system.{smv_vars['x_var']} = {x_mag} & "
                f"system.{smv_vars['y_var']} = {y_mag}"
            )
            lines.append(
                f"INVAR ({cond}) -> system.{smv_vars['command_final']} != {fbd};"
            )
    return lines


def _inject_invars(smv: str, invar_lines: list[str]) -> str:
    marker = "--------------SPECIFICATIONS\n"
    if marker not in smv:
        raise ValueError("SPECIFICATIONS marker not found in SMV.")
    block = "-- A/G contract constraints (verified by alpha-beta-CROWN):\n"
    block += "\n".join(invar_lines) + "\n"
    return smv.replace(marker, marker + block, 1)


def run_smv_patch(ctx: dict, smv_vars: dict[str, str]) -> dict:
    print("\n" + "=" * 60)
    print("[3/4] SMV PATCHING (contract injection)")
    print("=" * 60)

    contracts = _load_sat_contracts(ctx["contracts_path"], ctx["spec_path"])

    t0 = time.perf_counter()
    smv = ctx["base_smv_path"].read_text(encoding="utf-8").replace("\r\n", "\n")

    smv, lines_removed = _remove_nn_defines(smv)
    print(f"  Removed 5 NN DEFINE blocks ({lines_removed} lines)")

    smv = _add_command_free_var(smv)
    print("  Replaced NN table outputs with non-deterministic advisory domain")

    invar_lines = _build_invar_lines(contracts, smv_vars)
    smv = _inject_invars(smv, invar_lines)
    print(f"  Injected {len(invar_lines)} INVAR constraints from {len(contracts)} SAT contracts")

    ctx["smv_path"].write_text(smv, encoding="utf-8")
    wall_sec = time.perf_counter() - t0

    print(f"  Patched SMV: {ctx['smv_path']}  ({wall_sec:.1f}s)")
    return {
        "wall_sec":         round(wall_sec, 3),
        "sat_contracts":    len(contracts),
        "invar_lines":      len(invar_lines),
        "nn_lines_removed": lines_removed,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        description="End-to-end compositional verification pipeline for ACAS Xu 5-NN NSBT."
    )
    p.add_argument("--contracts",  required=True,
                   help="Path to verified contracts JSON (e.g. contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json)")
    p.add_argument("--spec",       default="contracts/crown/continuous_goals/contract_specs_eps1e4.json",
                   help="Path to original contract spec JSON (default: contracts/crown/continuous_goals/contract_specs_eps1e4.json)")
    p.add_argument("--output",     required=True,
                   help="Output directory for patched SMV, nuXmv output, and report")
    p.add_argument("--nuxmv",      default=str(DEFAULT_NUXMV),
                   help=f"nuXmv binary path (default: {DEFAULT_NUXMV})")
    p.add_argument("--nuxmv-cmd",  default=str(DEFAULT_NUXMV_CMD), dest="nuxmv_cmd",
                   help=f"nuXmv command file (default: {DEFAULT_NUXMV_CMD})")
    p.add_argument("--metamodel",  default=str(DEFAULT_METAMODEL),
                   help=f"behaverify.tx path (default: {DEFAULT_METAMODEL})")
    p.add_argument("--config",     default=str(DEFAULT_CONFIG),
                   help=f"Config YAML for SMV variable names (default: {DEFAULT_CONFIG})")
    p.add_argument("--skip-tree",  action="store_true",
                   help="Skip tree generation; reuse tree/acas_360.tree if it exists")
    p.add_argument("--skip-smv",   action="store_true",
                   help="Skip base SMV generation; reuse symbolic/smv/acas_360.smv if it exists")
    args = p.parse_args()

    smv_vars   = _load_smv_vars(Path(args.config))
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Ensure tree/ and symbolic/smv/ dirs exist
    (_HERE / "tree").mkdir(exist_ok=True)
    (_HERE / "symbolic" / "smv").mkdir(parents=True, exist_ok=True)

    ctx = {
        "contracts_path":  Path(args.contracts).resolve(),
        "spec_path":       Path(args.spec).resolve(),
        "tree_path":       _HERE / "tree" / "acas_360.tree",
        "base_smv_path":   _HERE / "symbolic" / "smv" / "acas_360.smv",
        "smv_path":        output_dir / "acas_360_contracts.smv",   # patched SMV
        "nuxmv_out_path":  output_dir / "nuxmv_output.txt",
        "report_path":     output_dir / "pipeline_report.json",
        "metamodel":       Path(args.metamodel).resolve(),
        "nuxmv_bin":       Path(args.nuxmv).resolve(),
        "nuxmv_cmd":       Path(args.nuxmv_cmd).resolve(),
        "skip_tree":       args.skip_tree,
        "skip_smv":        args.skip_smv,
    }

    t_start = time.perf_counter()

    tree_metrics  = run_tree_generation(ctx)
    smv_metrics   = run_smv_generation(ctx)
    patch_metrics = run_smv_patch(ctx, smv_vars)
    nuxmv_metrics = run_nuxmv(ctx)

    total = time.perf_counter() - t_start

    write_report(
        ctx["report_path"],
        steps={
            "tree":      tree_metrics,
            "smv":       smv_metrics,
            "smv_patch": patch_metrics,
            "nuxmv":     nuxmv_metrics,
        },
        total_wall_sec=total,
        extra={"contracts_path": str(ctx["contracts_path"])},
    )


if __name__ == "__main__":
    main()
