"""
Shared fixtures, helpers, and mock AST builders for multi-agent tests.

Imported automatically by pytest for all files in this package.
"""

import sys
import pytest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).parent.parent.parent
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

MULTI_AGENT_DIR = REPO_ROOT / "test_examples" / "multi_agent"
TWOROBOT1D_MULTIAGENT = MULTI_AGENT_DIR / "TwoRobot1D_multiagent.tree"
TWOROBOT1D_ORIGINAL = REPO_ROOT / "examples" / "MultiAgent" / "TwoRobot1D.tree"
TWOD_LIVELOCK = MULTI_AGENT_DIR / "2DLivelock_multiagent.tree"
THREE_IN_RING = MULTI_AGENT_DIR / "ThreeInRing_multiagent.tree"
FIVE_IN_RING = MULTI_AGENT_DIR / "FiveInRing_multiagent.tree"


# ---------------------------------------------------------------------------
# Import helpers
# ---------------------------------------------------------------------------

def _import_expander():
    try:
        import behaverify.agent_expander as ae
        return ae
    except ImportError:
        pytest.skip("behaverify.agent_expander not importable")


def load_metamodel():
    try:
        from textx import metamodel_from_file
    except ImportError:
        pytest.skip("textx not installed")
    try:
        from importlib.resources import files
        tx_file = files("behaverify").joinpath("data", "metamodel", "behaverify.tx")
    except Exception:
        tx_file = SRC_PATH / "behaverify" / "data" / "metamodel" / "behaverify.tx"
    if not Path(str(tx_file)).exists():
        pytest.skip("behaverify.tx metamodel not found")
    return metamodel_from_file(str(tx_file))


def require_textx():
    """Skip the calling test if textx is not importable."""
    try:
        import textx  # noqa: F401
    except ImportError:
        pytest.skip("textx not installed")


def parse_tree_file(path):
    mm = load_metamodel()
    return mm.model_from_file(str(path))


def parse_and_expand(path):
    ae = _import_expander()
    model = parse_tree_file(path)
    return ae.expand_agents(model)


# ---------------------------------------------------------------------------
# Mock AST builder helpers (no textX required)
# ---------------------------------------------------------------------------
# These replicate the attribute shapes that _cs_to_text, _func_to_text, etc.
# expect from a TextX-parsed model. SimpleNamespace is used so attribute
# access works identically to real TextX objects.

NS = SimpleNamespace


def _cs_ref(name):
    """code_statement that is an atom.reference (variable name)."""
    atom = NS(constant=None, reference=name)
    return NS(
        agent_param_ref=None, agent_param_index=None, agent_param_name=None,
        indexed_var=None, indexed_var_index=None, read_at_idx=None,
        function_call=None, code_statement=None,
        atom=atom, node_name=None, read_at=None, trace_num=None,
    )


def _cs_int(val):
    """code_statement that is an atom.constant integer."""
    atom = NS(constant=NS(val=val), reference=None)
    return NS(
        agent_param_ref=None, agent_param_index=None, agent_param_name=None,
        indexed_var=None, indexed_var_index=None, read_at_idx=None,
        function_call=None, code_statement=None,
        atom=atom, node_name=None, read_at=None, trace_num=None,
    )


def _cs_str(val):
    """code_statement that is an atom.constant string (enum value)."""
    atom = NS(constant=NS(val=val), reference=None)
    return NS(
        agent_param_ref=None, agent_param_index=None, agent_param_name=None,
        indexed_var=None, indexed_var_index=None, read_at_idx=None,
        function_call=None, code_statement=None,
        atom=atom, node_name=None, read_at=None, trace_num=None,
    )


def _cs_indexed(var_name, idx, read_at_idx=None):
    """code_statement that is an indexed_var (x_pos[i])."""
    return NS(
        agent_param_ref=None, agent_param_index=None, agent_param_name=None,
        indexed_var=var_name, indexed_var_index=idx, read_at_idx=read_at_idx,
        function_call=None, code_statement=None,
        atom=None, node_name=None, read_at=None, trace_num=None,
    )


def _cs_agent_param(index_var, param_name):
    """code_statement that is an agent_param_ref (agents[i].param_name)."""
    return NS(
        agent_param_ref='agents', agent_param_index=index_var,
        agent_param_name=param_name,
        indexed_var=None, indexed_var_index=None, read_at_idx=None,
        function_call=None, code_statement=None,
        atom=None, node_name=None, read_at=None, trace_num=None,
    )


def _cs_func(fname, *values):
    """code_statement wrapping a regular function call."""
    func = NS(
        function_name=fname,
        values=list(values),
        loop_variable=None, loop_condition=None, loop_variable_domain=None,
        min_val=None, max_val=None, reverse=False,
        bound=None, to_index=None, constant_index=None,
        node_name=None, read_at=None, trace_num=None,
        cond_value=None, default_value=None,
    )
    return NS(
        agent_param_ref=None, agent_param_index=None, agent_param_name=None,
        indexed_var=None, indexed_var_index=None, read_at_idx=None,
        function_call=func, code_statement=None,
        atom=None, node_name=None, read_at=None, trace_num=None,
    )


def _cs_status(fname, node_name_cs):
    """code_statement wrapping a status function (success/failure/running/active)."""
    func = NS(
        function_name=fname,
        values=[],
        loop_variable=None, loop_condition=None, loop_variable_domain=None,
        min_val=None, max_val=None, reverse=False,
        bound=None, to_index=None, constant_index=None,
        node_name=node_name_cs, read_at=None, trace_num=None,
        cond_value=None, default_value=None,
    )
    return NS(
        agent_param_ref=None, indexed_var=None, read_at_idx=None,
        function_call=func, code_statement=None,
        atom=None, node_name=None, read_at=None, trace_num=None,
    )


def _make_assign(default_values=None, cases=None):
    """Minimal assign_value mock for _assign_to_text."""
    case_results = []
    for cond_cs, val_cs_list in (cases or []):
        case_results.append(NS(condition=cond_cs, values=val_cs_list))
    default_result = None
    if default_values is not None:
        default_result = NS(values=default_values)
    return NS(case_results=case_results, default_result=default_result)


def _make_domain_range(min_cs, max_cs):
    return NS(boolean=False, true_int=False, true_real=False,
              min_val=min_cs, max_val=max_cs, domain_codes=None)


def _make_domain_bool():
    return NS(boolean=True, true_int=False, true_real=False,
              min_val=None, max_val=None, domain_codes=None)


def _make_domain_int():
    return NS(boolean=False, true_int=True, true_real=False,
              min_val=None, max_val=None, domain_codes=None)


def _make_domain_enum(*codes):
    return NS(boolean=False, true_int=False, true_real=False,
              min_val=None, max_val=None, domain_codes=list(codes))


def _make_constant(name, val):
    """Single constant like 'min_val := 0'."""
    return NS(name=name, val=NS(val=val))


def _make_mock_model_constants(**kwargs):
    """Minimal BehaviorModel mock with just constants and no other attrs."""
    consts = [_make_constant(k, v) for k, v in kwargs.items()]
    return NS(constants=consts)
