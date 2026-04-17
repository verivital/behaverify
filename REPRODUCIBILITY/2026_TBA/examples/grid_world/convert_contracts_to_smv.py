"""
convert_contracts_to_smv — grid-world Step 2: .tree + contracts → contract-based nuXmv SMV.

run_smv_generation() calls dsl_with_contracts_to_nuxmv and records metrics.
The SMV converter arguments (neural_var, pos_x, pos_y, domain) are passed in
from run_compositional_pipeline.py rather than hardcoded here.

Kept in grid_world/ (not 2026_TBA/pipeline/) because it calls the grid-world-
specific dsl_with_contracts_to_nuxmv() function with grid-specific parameters.
"""

from __future__ import annotations

import json
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

from pipeline.resolve_pipeline_paths import self_rss_kb


def run_smv_generation(ctx: dict[str, Any], smv_cfg: dict[str, Any]) -> dict[str, Any]:
    """
    Convert .tree + contracts JSON into a contract-injected nuXmv SMV file.

    smv_cfg must contain:
        neural_var  — name of the neural network variable in the .tree model
        pos_x       — name of the x-position variable
        pos_y       — name of the y-position variable
        domain      — list of action labels in declaration order
        src_dir     — absolute path to the behaverify src/ directory
    """
    print("\n" + "=" * 60)
    print("[2/3] SMV GENERATION")
    print("=" * 60)

    src_dir = smv_cfg["src_dir"]
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    import dsl_with_contracts_to_nuxmv as _conv  # noqa: PLC0415

    tracemalloc.start()
    t0 = time.perf_counter()

    _conv.dsl_with_contracts_to_nuxmv(
        metamodel_file     = str(ctx["metamodel"]),
        tree_file          = str(ctx["tree_path"]),
        output_file        = str(ctx["smv_path"]),
        contracts_file     = str(ctx["contracts_path"]),
        neural_var         = smv_cfg["neural_var"],
        pos_x              = smv_cfg["pos_x"],
        pos_y              = smv_cfg["pos_y"],
        domain             = smv_cfg["domain"],
        dir_map            = _conv.DEFAULT_DIR_MAP,
        skip_grammar_check = True,
    )

    wall_sec = time.perf_counter() - t0
    rss_after = self_rss_kb()
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    sat_injected = _count_sat_contracts(ctx["contracts_path"])
    metrics = {
        "wall_sec":               round(wall_sec, 3),
        "peak_rss_kb":            rss_after,
        "peak_traced_bytes":      peak_traced,
        "sat_contracts_injected": sat_injected,
    }
    print(f"\n[smv] {wall_sec:.1f}s  |  peak RSS ≥{rss_after} KB  |  "
          f"{sat_injected} INVAR constraints injected")
    return metrics


def _count_sat_contracts(contracts_path: Path) -> int:
    with open(contracts_path, encoding="utf-8") as f:
        data = json.load(f)
    return sum(1 for c in data.get("contracts", []) if c["status"] == "SAT")
