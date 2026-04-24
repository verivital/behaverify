"""
Tests for the multi-agent DSL extension (agent_types / agents).

Test groups:
  TestBackwardCompatibility  — existing single-agent files still work (pass now, must keep passing)
  TestMultiAgentSyntaxParsing — grammar accepts agent_types/agents syntax (FAILS until Phase 1)
  TestAgentExpander           — expander module exists and runs (FAILS until Phase 2)
  TestExpanderEquivalence     — expanded output matches hand-written TwoRobot1D (FAILS until Phase 2)

Run with:
  python3 -m pytest tests/test_multi_agent.py -v
  python3 -m pytest tests/test_multi_agent.py -v -k "Backward"  # only backward-compat tests
"""

import sys
import pytest
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

ORIG_MULTI_AGENT_DIR = REPO_ROOT / "examples" / "MultiAgent"
MULTI_AGENT_DIR = REPO_ROOT / "test_examples" / "multi_agent"

TWOROBOT1D_ORIGINAL = ORIG_MULTI_AGENT_DIR / "TwoRobot1D.tree"
TWOROBOT1D_MULTIAGENT = MULTI_AGENT_DIR / "TwoRobot1D_multiagent.tree"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_metamodel():
    """Load the BehaVerify TextX metamodel. Skip test if unavailable."""
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


def parse_tree_file(path):
    """Parse a .tree file and return the model, or skip if textx unavailable."""
    mm = load_metamodel()
    return mm.model_from_file(str(path))


# ---------------------------------------------------------------------------
# Group 1: Backward compatibility — must pass now and after implementation
# ---------------------------------------------------------------------------

class TestBackwardCompatibility:
    """Existing single-agent files are unaffected by the extension."""

    def test_original_tworobot1d_file_exists(self):
        assert TWOROBOT1D_ORIGINAL.exists(), (
            f"Reference file missing: {TWOROBOT1D_ORIGINAL}"
        )

    def test_original_tworobot1d_is_readable(self):
        content = TWOROBOT1D_ORIGINAL.read_text()
        assert len(content) > 0
        assert "tree {" in content
        assert "parallel" in content

    def test_original_tworobot1d_has_expected_variables(self):
        content = TWOROBOT1D_ORIGINAL.read_text()
        # The hand-written file must have both robot variables
        assert "act1" in content
        assert "act2" in content
        assert "x_d1" in content
        assert "x_d2" in content

    def test_original_tworobot1d_has_expected_checks(self):
        content = TWOROBOT1D_ORIGINAL.read_text()
        assert "AtGoal1" in content
        assert "AtGoal2" in content

    def test_original_tworobot1d_has_expected_actions(self):
        content = TWOROBOT1D_ORIGINAL.read_text()
        assert "Move1" in content
        assert "Move2" in content

    def test_original_tworobot1d_has_three_specs(self):
        content = TWOROBOT1D_ORIGINAL.read_text()
        # One INVARSPEC + two CTLSPECs
        assert content.count("INVARSPEC") == 1
        assert content.count("CTLSPEC") == 2

    def test_original_tworobot1d_parses_with_current_grammar(self):
        """The existing file must continue to parse after the grammar extension."""
        model = parse_tree_file(TWOROBOT1D_ORIGINAL)
        assert model is not None

    def test_original_tworobot1d_generates_nuxmv(self):
        """The existing pipeline must continue to generate SMV without errors."""
        try:
            from behaverify.behaverify import main
        except ImportError:
            pytest.skip("behaverify package not importable")

        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir)
            try:
                main(["nuxmv", str(TWOROBOT1D_ORIGINAL), str(out),
                      "--generate", "--overwrite"])
                smv_files = list(out.rglob("*.smv"))
                assert len(smv_files) == 1, (
                    f"Expected 1 .smv file, got {len(smv_files)}"
                )
            except SystemExit as e:
                if e.code != 0:
                    pytest.fail(f"behaverify exited with code {e.code}")


# ---------------------------------------------------------------------------
# Group 2: Multi-agent syntax parsing — FAILS until Phase 1 (grammar extension)
# ---------------------------------------------------------------------------

class TestMultiAgentSyntaxParsing:
    """
    The multi-agent .tree file uses syntax not yet in the grammar.
    These tests will FAIL until behaverify.tx is extended (Phase 1).
    """

    def test_multiagent_tree_file_exists(self):
        """The test fixture file must exist regardless of grammar support."""
        assert TWOROBOT1D_MULTIAGENT.exists(), (
            f"Multi-agent test file missing: {TWOROBOT1D_MULTIAGENT}\n"
            "Create it at test_examples/multi_agent/TwoRobot1D_multiagent.tree"
        )

    def test_multiagent_file_contains_agent_types_section(self):
        content = TWOROBOT1D_MULTIAGENT.read_text()
        assert "agent_types" in content, "File must contain agent_types section"
        assert "agent_type" in content

    def test_multiagent_file_contains_agents_section(self):
        content = TWOROBOT1D_MULTIAGENT.read_text()
        assert "agents {" in content, "File must contain agents section"

    def test_multiagent_file_contains_parameters_block(self):
        content = TWOROBOT1D_MULTIAGENT.read_text()
        assert "parameters {" in content, "agent_type must declare parameters"
        assert "goal_x" in content
        assert "start_x" in content

    def test_multiagent_file_contains_agent_instances_with_parameters(self):
        content = TWOROBOT1D_MULTIAGENT.read_text()
        assert "agent { r0 Robot" in content
        assert "agent { r1 Robot" in content
        assert "start_x :=" in content
        assert "goal_x :=" in content

    def test_multiagent_file_uses_env_array_syntax(self):
        content = TWOROBOT1D_MULTIAGENT.read_text()
        assert "x_pos[self]" in content, "Template should use x_pos[self] for own position"
        assert "x_pos[i]" in content, "environment_update should use x_pos[i] iteration"

    def test_multiagent_file_uses_forall_in_specs(self):
        content = TWOROBOT1D_MULTIAGENT.read_text()
        assert "forall" in content, "Specs should use forall quantifier over agents"

    def test_grammar_accepts_agent_types_syntax(self):
        """
        After Phase 1 grammar extension: the grammar accepts agent_types/agents syntax.
        """
        mm = load_metamodel()
        model = mm.model_from_file(str(TWOROBOT1D_MULTIAGENT))
        assert model is not None
        assert len(model.agent_types) > 0, "Parsed model should have agent_types"
        assert len(model.agents) > 0, "Parsed model should have agents"

    def test_extended_grammar_accepts_agent_types_syntax(self):
        """
        AFTER Phase 1: the extended grammar should parse the file without error.
        Currently expected to fail.
        """
        # This will fail until behaverify.tx is extended
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        assert model is not None
        assert hasattr(model, "agent_types"), (
            "Parsed model should have agent_types attribute"
        )
        assert hasattr(model, "agents"), (
            "Parsed model should have agents attribute"
        )

    def test_extended_grammar_parses_agent_parameters(self):
        """After Phase 1: agent_type must expose its parameters."""
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        assert len(model.agent_types) == 1
        robot_type = model.agent_types[0]
        param_names = [p.name for p in robot_type.parameters]
        assert "start_x" in param_names
        assert "goal_x" in param_names

    def test_extended_grammar_parses_agent_instances(self):
        """After Phase 1: agents block exposes two instances with parameter values."""
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        assert len(model.agents) == 2
        names = [a.name for a in model.agents]
        assert "r0" in names
        assert "r1" in names


# ---------------------------------------------------------------------------
# Group 3: Expander module — FAILS until Phase 2 (agent_expander.py created)
# ---------------------------------------------------------------------------

class TestAgentExpander:
    """
    Tests for src/behaverify/agent_expander.py.
    All will FAIL with ImportError until Phase 2 is implemented.
    """

    def test_agent_expander_module_importable(self):
        """Phase 2 must create src/behaverify/agent_expander.py."""
        from behaverify.agent_expander import expand_agents  # noqa: F401

    def test_expander_accepts_parsed_model(self):
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)
        assert expanded is not None

    def test_expander_produces_two_bl_variables(self):
        """act_r0 and act_r1 must appear in expanded variables."""
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        bl_names = [v.name for v in expanded.variables if v.scope == "bl"]
        assert "act_r0" in bl_names, f"act_r0 missing from bl vars: {bl_names}"
        assert "act_r1" in bl_names, f"act_r1 missing from bl vars: {bl_names}"

    def test_expander_produces_two_env_variables(self):
        """x_pos_r0 and x_pos_r1 must appear in expanded env variables."""
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        env_names = [v.name for v in expanded.variables if v.scope == "env"]
        assert "x_pos_r0" in env_names, f"x_pos_r0 missing from env vars: {env_names}"
        assert "x_pos_r1" in env_names, f"x_pos_r1 missing from env vars: {env_names}"

    def test_expander_initialises_env_vars_from_parameters(self):
        """x_pos_r0 initial value must match r0.start_x (= min_val = 0)."""
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        env_map = {v.name: v for v in expanded.variables if v.scope == "env"}
        # r0.start_x = min_val = 0, r1.start_x = max_val = 4
        assert env_map["x_pos_r0"].initial_value == 0, (
            "x_pos_r0 should initialise to 0 (r0.start_x = min_val)"
        )
        assert env_map["x_pos_r1"].initial_value == 4, (
            "x_pos_r1 should initialise to 4 (r1.start_x = max_val)"
        )

    def test_expander_produces_atgoal_checks_with_substituted_goals(self):
        """AtGoal_r0 condition must use max_val (r0.goal_x); AtGoal_r1 must use min_val."""
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        check_names = [c.name for c in expanded.environment_checks]
        assert "AtGoal_r0" in check_names
        assert "AtGoal_r1" in check_names

    def test_expander_produces_move_actions_per_agent(self):
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        action_names = [a.name for a in expanded.action_nodes]
        assert "Move_r0" in action_names
        assert "Move_r1" in action_names

    def test_expander_produces_parallel_root(self):
        """Expanded tree root must be a parallel node."""
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        root = expanded.tree
        assert root.node_type == "parallel", (
            f"Root should be parallel, got {root.node_type}"
        )

    def test_expander_produces_two_subtrees_under_parallel_root(self):
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        assert len(expanded.tree.children) == 2, (
            f"Expected 2 agent subtrees, got {len(expanded.tree.children)}"
        )

    def test_expander_expands_forall_specs_to_concrete_agents(self):
        """After expansion, no spec should contain a forall quantifier over agents."""
        from behaverify.agent_expander import expand_agents
        import re
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        # Serialize specs to string and check no unresolved forall remains
        # (exact serialisation depends on implementation; adapt as needed)
        for spec in expanded.specifications:
            spec_str = str(spec)
            assert "forall" not in spec_str or "agents" not in spec_str, (
                f"Spec still contains unresolved forall: {spec_str}"
            )

    def test_expander_produces_no_agent_types_in_expanded_model(self):
        """Expanded model should have no agent_types — they are consumed by the expander."""
        from behaverify.agent_expander import expand_agents
        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        agent_types = getattr(expanded, "agent_types", [])
        assert len(agent_types) == 0, (
            "Expanded model should have no agent_types remaining"
        )


# ---------------------------------------------------------------------------
# Group 4: Equivalence with hand-written TwoRobot1D — FAILS until Phase 2
# ---------------------------------------------------------------------------

class TestExpanderEquivalence:
    """
    The expanded multi-agent model should produce SMV equivalent to TwoRobot1D.tree.
    These tests run both files through the full pipeline and compare generated output.
    """

    @pytest.fixture
    def expanded_smv(self, tmp_path):
        """Generate SMV from the expanded multi-agent file."""
        from behaverify.agent_expander import expand_agents
        from behaverify.behaverify import main

        model = parse_tree_file(TWOROBOT1D_MULTIAGENT)
        expanded = expand_agents(model)

        # Write the expanded model to a temp .tree file and run the pipeline
        expanded_tree_path = tmp_path / "expanded.tree"
        from behaverify.agent_expander import model_to_tree_text
        expanded_tree_path.write_text(model_to_tree_text(expanded))

        out = tmp_path / "expanded_out"
        out.mkdir()
        main(["nuxmv", str(expanded_tree_path), str(out), "--generate", "--overwrite"])
        smv_files = list(out.rglob("*.smv"))
        assert len(smv_files) == 1
        return smv_files[0].read_text()

    @pytest.fixture
    def original_smv(self, tmp_path):
        """Generate SMV from the original hand-written TwoRobot1D.tree."""
        from behaverify.behaverify import main

        out = tmp_path / "original_out"
        out.mkdir()
        main(["nuxmv", str(TWOROBOT1D_ORIGINAL), str(out), "--generate", "--overwrite"])
        smv_files = list(out.rglob("*.smv"))
        assert len(smv_files) == 1
        return smv_files[0].read_text()

    def test_both_smv_files_generated(self, expanded_smv, original_smv):
        """Sanity check: both pipelines produce non-empty SMV output."""
        assert len(expanded_smv) > 0
        assert len(original_smv) > 0

    def test_expanded_smv_has_same_number_of_var_declarations(
        self, expanded_smv, original_smv
    ):
        """Both SMV files should declare the same number of VAR sections."""
        expanded_vars = expanded_smv.count("VAR")
        original_vars = original_smv.count("VAR")
        assert expanded_vars == original_vars, (
            f"VAR count differs: expanded={expanded_vars}, original={original_vars}"
        )

    def test_expanded_smv_has_same_number_of_specs(self, expanded_smv, original_smv):
        """Both SMV files should have the same number of INVARSPEC / CTLSPEC entries."""
        for spec_type in ("INVARSPEC", "CTLSPEC", "LTLSPEC"):
            exp_count = expanded_smv.count(spec_type)
            orig_count = original_smv.count(spec_type)
            assert exp_count == orig_count, (
                f"{spec_type} count differs: expanded={exp_count}, original={orig_count}"
            )

    def test_expanded_smv_has_parallel_module(self, expanded_smv, original_smv):
        """Both SMV files must contain a parallel composite module."""
        assert "parallel" in expanded_smv.lower()
        assert "parallel" in original_smv.lower()

    def test_expanded_smv_contains_two_agent_act_variables(self, expanded_smv):
        """The generated SMV must have action variables for both agents."""
        # Variable names will be act_r0/act_r1 in expanded vs act1/act2 in original
        assert "act_r0" in expanded_smv or "act_r1" in expanded_smv, (
            "Expanded SMV should reference agent action variables"
        )

    def test_original_smv_contains_original_variable_names(self, original_smv):
        """The original SMV must still use the hand-written variable names."""
        assert "act1" in original_smv
        assert "act2" in original_smv
        assert "x_d1" in original_smv
        assert "x_d2" in original_smv
