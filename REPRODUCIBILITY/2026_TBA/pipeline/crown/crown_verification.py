"""
pipeline.crown.crown_verification — shared alpha-beta-CROWN invocation logic.

Provides the core verification primitives used by all example scripts:
    normalize_status()      map raw CROWN status string to SAT / UNSAT / TIMEOUT
    build_crown_config()    construct an ABCrown ConfigBuilder result
    run_crown_verification() build spec and call CROWN for one lower/upper region

Example scripts (verify_acas_contracts.py, verify_grid_world_contracts.py) are
thin wrappers that construct the example-specific lower/upper arrays and call
run_crown_verification().  This module contains no example-specific logic.

Note on multiprocessing:
    This module imports abcrown at the module level.  When used in a spawned
    worker process (verify_acas_contracts_parallel.py), import this module
    lazily *inside* the worker function so that the main process never loads
    abcrown (avoiding multiprocessing/global-state conflicts).
"""

from __future__ import annotations

import functools
from typing import Any

import torch
from abcrown import ABCrownSolver, ConfigBuilder, VerificationSpec, input_vars, output_vars


# ---------------------------------------------------------------------------
# Status normalization
# ---------------------------------------------------------------------------

def normalize_status(raw: str) -> str:
    """Map CROWN result.status to SAT / UNSAT / TIMEOUT."""
    if raw in ("safe", "verified", "safe-incomplete"):
        return "SAT"
    if raw.startswith("unsafe"):
        return "UNSAT"
    return "TIMEOUT"


# ---------------------------------------------------------------------------
# CROWN configuration
# ---------------------------------------------------------------------------

def build_crown_config(
    timeout: float,
    pgd_order: str = "before",
    device: str = "cpu",
    pgd_restarts: int = 50,
    extra_settings: dict[str, Any] | None = None,
) -> Any:
    """
    Build an alpha-beta-CROWN solver configuration.

    Args:
        timeout:        BaB timeout in seconds.
        pgd_order:      "before" (PGD then BaB), "after", or "skip" (BaB only).
        device:         "cpu" or "cuda".
        pgd_restarts:   Number of PGD restarts (used only when pgd_order="before").
        extra_settings: Optional dict of additional ConfigBuilder .set() calls,
                        e.g. {"bab__cut__enabled": True, "bab__branching__method": "sb"}.
    """
    builder = (
        ConfigBuilder.from_defaults()
        .set(general__device=device)
        .set(attack__pgd_order=pgd_order)
        .set(bab__timeout=timeout)
    )
    if pgd_order == "before":
        builder = builder.set(attack__pgd_restarts=pgd_restarts)
    if extra_settings:
        for key, val in extra_settings.items():
            builder = builder.set(**{key: val})
    return builder()


# ---------------------------------------------------------------------------
# Core verification call
# ---------------------------------------------------------------------------

def run_crown_verification(
    onnx_path: str,
    lower: list[float],
    upper: list[float],
    forbidden_idx: int,
    num_classes: int,
    crown_config: Any,
) -> tuple[str, Any]:
    """
    Verify one input region with a single CROWN call.

    Input constraint:  lower[i] <= x[i] <= upper[i]  for i in range(len(lower))
    Output constraint: exists j != forbidden_idx such that y[j] > y[forbidden_idx]
                       (i.e. the forbidden class is not uniquely maximal)

    Returns:
        (status, result) where status is "SAT", "UNSAT", or "TIMEOUT" and
        result is the raw ABCrownSolver result object (for counterexample
        extraction or other example-specific post-processing).
    """
    n_inputs = len(lower)
    x = input_vars((n_inputs,))
    lower_t = torch.tensor(lower, dtype=torch.float32)
    upper_t = torch.tensor(upper, dtype=torch.float32)
    input_constraint = (x >= lower_t) & (x <= upper_t)

    y = output_vars(num_classes)
    others = [j for j in range(num_classes) if j != forbidden_idx]
    output_constraint = functools.reduce(
        lambda a, b: a | b,
        [y[j] > y[forbidden_idx] for j in others],
    )

    spec = VerificationSpec.build_spec(
        input_vars=x, output_vars=y,
        input_constraint=input_constraint, output_constraint=output_constraint,
    )
    result = ABCrownSolver(spec, onnx_path, config=crown_config).solve()
    return normalize_status(result.status), result
