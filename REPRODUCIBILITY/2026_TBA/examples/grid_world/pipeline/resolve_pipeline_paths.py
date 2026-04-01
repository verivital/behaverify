"""
pipeline.resolve_pipeline_paths — shared memory helpers and pipeline context setup.

setup() resolves all paths, creates the output directory, and optionally
auto-generates a .tree file from the counter template. It returns a context
dict that every downstream stage reads from.
"""

from __future__ import annotations

import argparse
import os
import resource
from pathlib import Path
from typing import Any


def self_rss_kb() -> int:
    """Peak RSS of this process so far (KB). Monotonically increasing on Linux."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def children_rss_kb() -> int:
    """Peak RSS of all waited child processes (KB)."""
    return resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss


def setup(args: argparse.Namespace, counter_template: Path) -> dict[str, Any]:
    """
    Resolve all pipeline paths and prepare the output directory.

    If --tree is not provided, auto-generates a .tree file by substituting
    the ONNX path into counter_template.tree.

    Returns a context dict consumed by all pipeline stages.
    """
    onnx_path  = Path(args.onnx).resolve()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    network_name = onnx_path.stem

    if args.tree:
        tree_path = Path(args.tree).resolve()
    else:
        tree_path    = output_dir / f"{network_name}.tree"
        template_text = counter_template.read_text(encoding="utf-8")
        # dsl_to_nuxmv.py builds the ONNX path as:
        #   file_prefix + '/' + source   (string concat, not os.path.join)
        # where file_prefix = tree_file.rsplit('/', 1)[0].
        # Use a CWD-relative path so the concat resolves correctly.
        onnx_rel  = os.path.relpath(onnx_path, tree_path.parent)
        tree_text = template_text.replace("REPLACE_SOURCE", onnx_rel)
        tree_path.write_text(tree_text, encoding="utf-8")
        print(f"[setup] Auto-generated tree: {tree_path}")

    contracts_path = (
        Path(args.contracts).resolve() if args.contracts
        else output_dir / "contracts.json"
    )

    return {
        "network_name":   network_name,
        "onnx_path":      onnx_path,
        "tree_path":      tree_path,
        "contracts_path": contracts_path,
        "smv_path":       output_dir / f"{network_name}_contracts.smv",
        "nuxmv_out_path": output_dir / "nuxmv_output.txt",
        "report_path":    output_dir / "pipeline_report.json",
        "output_dir":     output_dir,
        "config_path":    Path(args.config).resolve(),
        "nuxmv_bin":      Path(args.nuxmv).resolve(),
        "nuxmv_cmd":      Path(args.nuxmv_cmd).resolve(),
        "metamodel":      Path(args.metamodel).resolve(),
        "skip_contracts": args.skip_contracts,
    }
