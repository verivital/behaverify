"""
dsl_with_contracts_to_nuxmv.py

Replace the NEURAL variable's lookup table in a BehaVerify-generated nuXmv SMV
with verified A/G contracts, producing a contract-based SMV for compositional
verification.

Pipeline:
  1. Generate base SMV from .tree file via dsl_to_nuxmv (NN encoded as table).
  2. Patch the SMV:
       a. Remove the NEURAL variable's DEFINE case-statement block.
       b. Declare the variable as a free (non-deterministic) VAR.
       c. Inject INVAR constraints derived from the verified A/G contracts.

Soundness: the patched SMV over-approximates the original system.  If nuXmv
proves the safety property UNSAT under this over-approximation, the property
holds for the actual NN (the contracts are the formal link).

Usage (grid world, counter_1.tree style):
  python dsl_with_contracts_to_nuxmv.py \\
    --metamodel ../../../src/behaverify/data/metamodel/behaverify.tx \\
    --tree      counter_1.tree \\
    --contracts contract_results.json \\
    --output    counter_1_contracts.smv \\
    --neural-var network \\
    --pos-x drone_x \\
    --pos-y drone_y \\
    --domain left right up down no_action \\
    --dir-map '{"We":"left","Ea":"right","No":"up","So":"down","XX":"no_action"}'
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from typing import Any

# ---------------------------------------------------------------------------
# Path setup — import dsl_to_nuxmv from the same src/ directory.
# ---------------------------------------------------------------------------

_SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SRC)

import dsl_to_nuxmv as _base  # noqa: E402 (intentional late import)

# ---------------------------------------------------------------------------
# Default direction-label mapping
# (contract labels from verify_contracts.py → SMV enumeration labels used in
#  counter_N.tree files)
# ---------------------------------------------------------------------------

DEFAULT_DIR_MAP: dict[str, str] = {
    "We": "left",
    "Ea": "right",
    "No": "up",
    "So": "down",
    "XX": "no_action",
}

# ---------------------------------------------------------------------------
# Contract loading
# ---------------------------------------------------------------------------


def load_sat_contracts(path: str) -> list[dict[str, Any]]:
    """Return only SAT-verified contracts from contract_results.json."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    sat = [c for c in data["contracts"] if c["status"] == "SAT"]
    print(f"  {len(sat)} SAT contracts loaded (of {len(data['contracts'])} total)")
    return sat


# ---------------------------------------------------------------------------
# SMV patch helpers
# ---------------------------------------------------------------------------


def remove_neural_define(smv: str, neural_smv: str) -> str:
    """Remove the NN table DEFINE block (giant case statement) from the SMV."""
    pattern = (
        r"        " + re.escape(neural_smv) + r" :=\n"
        r"            case\n"
        r".*?"
        r"            esac;\n"
    )
    result, n = re.subn(pattern, "", smv, flags=re.DOTALL)
    if n == 0:
        raise ValueError(
            f"NEURAL DEFINE for '{neural_smv}' not found — check --neural-var."
        )
    removed = smv.count("\n") - result.count("\n")
    print(f"  Removed {n} DEFINE block(s) for '{neural_smv}' ({removed} lines)")
    return result


def add_neural_var(smv: str, neural_smv: str, domain: list[str]) -> str:
    """Insert a free VAR declaration for the NN output into the VAR section."""
    domain_str = "{" + ", ".join(domain) + "}"
    new_line = f"        {neural_smv} : {domain_str};\n"
    marker = "--START OF BLACKBOARD VARIABLES DECLARATION\n"
    if marker not in smv:
        raise ValueError("VAR-section marker '--START OF BLACKBOARD VARIABLES DECLARATION' not found.")
    return smv.replace(marker, marker + new_line, 1)


def build_invar_lines(
    contracts: list[dict[str, Any]],
    neural_smv: str,
    pos_x_smv: str,
    pos_y_smv: str,
    dir_map: dict[str, str],
) -> list[str]:
    """Generate INVAR constraint lines from the verified A/G contracts."""
    lines = []
    for c in contracts:
        cx, cy = c["source"]
        label = dir_map.get(c["forbidden_dir"], c["forbidden_dir"])
        lines.append(
            f"INVAR (system.{pos_x_smv} = {cx} & system.{pos_y_smv} = {cy})"
            f" -> system.{neural_smv} != {label};"
        )
    return lines


def inject_invars(smv: str, invar_lines: list[str]) -> str:
    """Inject INVAR assumptions into the SPECIFICATIONS block of main MODULE."""
    marker = "--------------SPECIFICATIONS\n"
    if marker not in smv:
        raise ValueError("SPECIFICATIONS marker not found in SMV.")
    block = "\n-- A/G contract constraints (verified by alpha-beta-CROWN):\n"
    block += "\n".join(invar_lines) + "\n"
    return smv.replace(marker, marker + block, 1)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def patch_smv(
    base_smv_path: str,
    contracts: list[dict[str, Any]],
    neural_var: str,
    pos_x: str,
    pos_y: str,
    domain: list[str],
    dir_map: dict[str, str],
    output_path: str,
) -> None:
    """Apply all three patches to the base SMV and write the result."""
    with open(base_smv_path, encoding="utf-8") as f:
        smv = f.read()
    neural_smv = neural_var + "_stage_0"
    pos_x_smv  = pos_x + "_stage_0"
    pos_y_smv  = pos_y + "_stage_0"

    smv = remove_neural_define(smv, neural_smv)
    smv = add_neural_var(smv, neural_smv, domain)
    invars = build_invar_lines(contracts, neural_smv, pos_x_smv, pos_y_smv, dir_map)
    smv = inject_invars(smv, invars)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(smv)
    print(f"  Injected {len(invars)} INVAR constraints")
    print(f"  Output: {output_path}")


def dsl_with_contracts_to_nuxmv(
    metamodel_file: str,
    tree_file: str,
    output_file: str,
    contracts_file: str,
    neural_var: str,
    pos_x: str,
    pos_y: str,
    domain: list[str],
    dir_map: dict[str, str],
    keep_stage_0: bool = False,
    keep_last_stage: bool = False,
    do_not_trim: bool = False,
    behave_only: bool = False,
    recursion_limit: int = 0,
    skip_grammar_check: bool = False,
    record_times: str | None = None,
) -> None:
    """Full pipeline: .tree + contracts JSON → contract-based nuXmv SMV."""
    print(f"\n[1/3] Loading contracts from {contracts_file}")
    contracts = load_sat_contracts(contracts_file)

    print(f"\n[2/3] Generating base SMV from {tree_file}")
    tmp = tempfile.NamedTemporaryFile(suffix=".smv", delete=False, mode="w")
    tmp.close()
    try:
        _base.dsl_to_nuxmv(
            metamodel_file, tree_file, tmp.name,
            keep_stage_0, keep_last_stage, do_not_trim, behave_only,
            recursion_limit, False, skip_grammar_check, record_times,
        )
        print(f"\n[3/3] Patching SMV: replace NN table with A/G contracts")
        patch_smv(tmp.name, contracts, neural_var, pos_x, pos_y, domain, dir_map, output_file)
    finally:
        os.unlink(tmp.name)

    print("\nDone.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Replace the NEURAL network table in a BehaVerify nuXmv SMV with verified "
            "A/G contracts for compositional verification."
        )
    )
    p.add_argument("--metamodel",  required=True, help="Path to behaverify.tx")
    p.add_argument("--tree",       required=True, help="Path to .tree input file")
    p.add_argument("--contracts",  required=True, help="Path to contract_results.json")
    p.add_argument("--output",     required=True, help="Output .smv file path")
    p.add_argument("--neural-var", required=True,
                   help='NEURAL variable name in the .tree file (e.g., "network")')
    p.add_argument("--pos-x",      required=True,
                   help='Drone X variable name (e.g., "drone_x")')
    p.add_argument("--pos-y",      required=True,
                   help='Drone Y variable name (e.g., "drone_y")')
    p.add_argument("--domain",     nargs="+", required=True,
                   help="NN output domain labels (e.g., left right up down no_action)")
    p.add_argument("--dir-map",    default=None,
                   help="JSON dict mapping contract dir labels to SMV labels "
                        "(default: We→left Ea→right No→up So→down XX→no_action)")
    p.add_argument("--keep-last-stage",    action="store_true")
    p.add_argument("--do-not-trim",        action="store_true")
    p.add_argument("--skip-grammar-check", action="store_true")
    p.add_argument("--recursion-limit",    type=int, default=0)
    p.add_argument("--record-times",       default=None)
    args = p.parse_args()

    dir_map = json.loads(args.dir_map) if args.dir_map else DEFAULT_DIR_MAP

    dsl_with_contracts_to_nuxmv(
        metamodel_file  = args.metamodel,
        tree_file       = args.tree,
        output_file     = args.output,
        contracts_file  = args.contracts,
        neural_var      = args.neural_var,
        pos_x           = args.pos_x,
        pos_y           = args.pos_y,
        domain          = args.domain,
        dir_map         = dir_map,
        keep_last_stage   = args.keep_last_stage,
        do_not_trim       = args.do_not_trim,
        skip_grammar_check= args.skip_grammar_check,
        recursion_limit   = args.recursion_limit,
        record_times      = args.record_times,
    )


if __name__ == "__main__":
    main()
