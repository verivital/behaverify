"""
extract_acas_constants.py

Parse acas_template_360.tree and refresh the primitive constants in
acas_model_params.yaml.

Only values that exist in the .tree file are overwritten; manually maintained
sections (heading_int_degrees, safety_threshold, advisories, networks) are
left untouched.

Sections updated:
  physics.distance_modifier    ← constants { distance_modifier }
  physics.max_dist             ← constants { max_dist }
  physics.seconds_per_update   ← constants { seconds_per_update }
  physics.degree_multiplier    ← constants { degree_multiplier }
  physics.speed_own            ← variables { speed_own DEFINE INT result{<n>} }
  physics.speed_int            ← variables { speed_int DEFINE INT result{<n>} }
  nn_normalization.*           ← constants { distance_mean, distance_range, … }

Usage:
    python3 extract_acas_constants.py
    python3 extract_acas_constants.py --tree acas_template_360.tree \\
                                      --params acas_model_params.yaml
"""

import argparse
import re
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_tree_constants(tree_text: str) -> dict[str, int | float]:
    """Extract key := value pairs from the constants { } block."""
    m = re.search(r'\bconstants\s*\{([^}]*)\}', tree_text, re.DOTALL)
    if not m:
        raise ValueError("No 'constants { }' block found in .tree file")
    block = m.group(1)

    result: dict[str, int | float] = {}
    for match in re.finditer(r'\b(\w+)\s*:=\s*([0-9]+(?:\.[0-9]+)?)', block):
        key, val_str = match.group(1), match.group(2)
        result[key] = float(val_str) if '.' in val_str else int(val_str)
    return result


def parse_literal_speed(tree_text: str, name: str) -> int | None:
    """
    Extract the literal-integer speed_own / speed_int value from variables {}.

    The template defines both a formula-based DEFINE and a literal override:
      variable{env speed_own DEFINE INT assign{result{(mult, ...)}}}   ← formula
      variable{env speed_own DEFINE INT assign{result{20}}}            ← literal (active)

    Only the literal form (integer inside result{}) matches; formula forms do not.
    """
    matches = re.findall(
        rf'variable\{{env\s+{re.escape(name)}\s+DEFINE\s+INT\s+assign\{{result\{{(\d+)\}}\}}',
        tree_text,
    )
    return int(matches[-1]) if matches else None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    here = Path(__file__).parent
    parser = argparse.ArgumentParser(
        description="Refresh acas_model_params.yaml from acas_template_360.tree.",
    )
    parser.add_argument(
        "--tree", type=Path, default=here / "acas_template_360.tree",
        help="Path to the .tree template (default: acas_template_360.tree)",
    )
    parser.add_argument(
        "--params", type=Path, default=here / "acas_model_params.yaml",
        help="Path to the params YAML to update (default: acas_model_params.yaml)",
    )
    args = parser.parse_args()

    tree_text = args.tree.read_text(encoding="utf-8")
    consts    = parse_tree_constants(tree_text)

    with open(args.params, encoding="utf-8") as f:
        params = yaml.safe_load(f)

    # --- physics (tree-sourced fields only) ---
    p = params["physics"]
    for key in ("distance_modifier", "max_dist", "seconds_per_update", "degree_multiplier"):
        if key in consts:
            p[key] = consts[key]

    for name in ("speed_own", "speed_int"):
        val = parse_literal_speed(tree_text, name)
        if val is not None:
            p[name] = val

    # --- nn_normalization ---
    n = params["nn_normalization"]
    tree_to_yaml = {
        "distance_mean":   ("distance_mean",   float),
        "distance_range":  ("distance_range",  float),
        "speed_own_mean":  ("speed_own_mean",  float),
        "speed_own_range": ("speed_own_range", float),
        "speed_int_mean":  ("speed_int_mean",  float),
        "speed_int_range": ("speed_int_range", float),
    }
    for tree_key, (yaml_key, cast) in tree_to_yaml.items():
        if tree_key in consts:
            n[yaml_key] = cast(consts[tree_key])

    with open(args.params, "w", encoding="utf-8") as f:
        yaml.dump(params, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Updated {args.params} from {args.tree}")


if __name__ == "__main__":
    main()
