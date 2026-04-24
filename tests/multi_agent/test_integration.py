"""
Integration tests for the multi-agent expander (textX required).

All tests skip gracefully when textX is not installed.

Tests: TestExpanderVariableExpansion, TestExpanderEnvUpdate,
       TestExpanderChecksActions, TestExpanderTree, TestExpanderSpecs,
       TestMultiAgentScenarios, TestMaybeExpand
"""

from pathlib import Path
import pytest

from .conftest import (
    _import_expander, load_metamodel, require_textx, parse_tree_file,
    parse_and_expand,
    TWOROBOT1D_MULTIAGENT, TWOROBOT1D_ORIGINAL,
    TWOD_LIVELOCK, THREE_IN_RING, FIVE_IN_RING,
)


class TestExpanderVariableExpansion:

    @pytest.fixture(autouse=True)
    def setup_expanded(self):
        self._expanded = parse_and_expand(TWOROBOT1D_MULTIAGENT)

    def test_total_variable_count(self):
        # 2 env (x_pos_r0, x_pos_r1) + 2 bl (act_r0, act_r1) = 4
        assert len(self._expanded.variables) == 4

    def test_two_env_vars_exist(self):
        env_names = {v.name for v in self._expanded.variables if v.scope == "env"}
        assert len(env_names) == 2

    def test_env_var_names_are_x_pos_r0_and_r1(self):
        env_names = {v.name for v in self._expanded.variables if v.scope == "env"}
        assert "x_pos_r0" in env_names
        assert "x_pos_r1" in env_names

    def test_two_bl_vars_exist(self):
        bl_names = {v.name for v in self._expanded.variables if v.scope == "bl"}
        assert len(bl_names) == 2

    def test_bl_var_names_are_act_r0_and_r1(self):
        bl_names = {v.name for v in self._expanded.variables if v.scope == "bl"}
        assert "act_r0" in bl_names
        assert "act_r1" in bl_names

    def test_x_pos_r0_initial_value_is_zero(self):
        env_map = {v.name: v for v in self._expanded.variables if v.scope == "env"}
        assert env_map["x_pos_r0"].initial_value == 0

    def test_x_pos_r1_initial_value_is_four(self):
        env_map = {v.name: v for v in self._expanded.variables if v.scope == "env"}
        assert env_map["x_pos_r1"].initial_value == 4

    def test_env_var_domain_is_range(self):
        # Domain text is a range like [min_val, max_val] or [0, 4]
        env_map = {v.name: v for v in self._expanded.variables if v.scope == "env"}
        domain = env_map["x_pos_r0"].domain_text
        assert domain.startswith("[")
        assert domain.endswith("]")

    def test_bl_var_has_initial_text_not_value(self):
        bl_map = {v.name: v for v in self._expanded.variables if v.scope == "bl"}
        assert bl_map["act_r0"].initial_text is not None
        assert len(bl_map["act_r0"].initial_text) > 0

    def test_bl_var_initial_text_contains_assign(self):
        bl_map = {v.name: v for v in self._expanded.variables if v.scope == "bl"}
        assert "assign" in bl_map["act_r0"].initial_text

    def test_no_agent_types_remain(self):
        assert len(self._expanded.agent_types) == 0

    def test_no_array_syntax_in_var_names(self):
        for v in self._expanded.variables:
            assert "[" not in v.name
            assert "]" not in v.name


class TestExpanderEnvUpdate:

    @pytest.fixture(autouse=True)
    def setup_expanded(self):
        self._expanded = parse_and_expand(TWOROBOT1D_MULTIAGENT)

    def test_env_update_not_empty(self):
        assert len(self._expanded.environment_update_text.strip()) > 0

    def test_env_update_has_x_pos_r0(self):
        assert "x_pos_r0" in self._expanded.environment_update_text

    def test_env_update_has_x_pos_r1(self):
        assert "x_pos_r1" in self._expanded.environment_update_text

    def test_env_update_no_index_loop_x_pos(self):
        assert "x_pos[i]" not in self._expanded.environment_update_text

    def test_env_update_no_index_loop_act(self):
        assert "act[i]" not in self._expanded.environment_update_text

    def test_env_update_r0_section_references_act_r0(self):
        text = self._expanded.environment_update_text
        r0_idx = text.find("x_pos_r0")
        r1_idx = text.find("x_pos_r1")
        assert r0_idx != -1 and r1_idx != -1
        r0_segment = text[r0_idx:r1_idx]
        assert "act_r0" in r0_segment

    def test_env_update_preserves_direction_constants(self):
        text = self._expanded.environment_update_text
        assert "'We'" in text
        assert "'Ea'" in text

    def test_env_update_has_two_variable_statements(self):
        count = self._expanded.environment_update_text.count("variable_statement")
        assert count == 2

    def test_env_update_has_case_expressions(self):
        assert "case {" in self._expanded.environment_update_text


class TestExpanderChecksActions:

    @pytest.fixture(autouse=True)
    def setup_expanded(self):
        self._expanded = parse_and_expand(TWOROBOT1D_MULTIAGENT)

    def test_two_checks_created(self):
        assert len(self._expanded.environment_checks) == 2

    def test_check_names_suffixed_r0(self):
        names = {ck.name for ck in self._expanded.environment_checks}
        assert "AtGoal_r0" in names

    def test_check_names_suffixed_r1(self):
        names = {ck.name for ck in self._expanded.environment_checks}
        assert "AtGoal_r1" in names

    def test_check_r0_condition_has_x_pos_r0(self):
        ck_map = {ck.name: ck for ck in self._expanded.environment_checks}
        assert "x_pos_r0" in ck_map["AtGoal_r0"].condition_text

    def test_check_r0_condition_no_self_reference(self):
        ck_map = {ck.name: ck for ck in self._expanded.environment_checks}
        assert "[self]" not in ck_map["AtGoal_r0"].condition_text

    def test_check_r0_goal_x_resolved_to_4(self):
        ck_map = {ck.name: ck for ck in self._expanded.environment_checks}
        assert "4" in ck_map["AtGoal_r0"].condition_text
        assert "goal_x" not in ck_map["AtGoal_r0"].condition_text

    def test_check_r1_goal_x_resolved_to_0(self):
        ck_map = {ck.name: ck for ck in self._expanded.environment_checks}
        assert "0" in ck_map["AtGoal_r1"].condition_text
        assert "goal_x" not in ck_map["AtGoal_r1"].condition_text

    def test_check_r0_read_vars_use_flat_name(self):
        ck_map = {ck.name: ck for ck in self._expanded.environment_checks}
        assert any("x_pos_r0" in rv for rv in ck_map["AtGoal_r0"].read_vars)

    def test_check_r1_read_vars_use_flat_name(self):
        ck_map = {ck.name: ck for ck in self._expanded.environment_checks}
        assert any("x_pos_r1" in rv for rv in ck_map["AtGoal_r1"].read_vars)

    def test_two_actions_created(self):
        assert len(self._expanded.action_nodes) == 2

    def test_action_names_suffixed_r0(self):
        names = {a.name for a in self._expanded.action_nodes}
        assert "Move_r0" in names

    def test_action_names_suffixed_r1(self):
        names = {a.name for a in self._expanded.action_nodes}
        assert "Move_r1" in names

    def test_action_r0_write_vars_is_act_r0(self):
        act_map = {a.name: a for a in self._expanded.action_nodes}
        assert "act_r0" in act_map["Move_r0"].write_vars

    def test_action_r1_write_vars_is_act_r1(self):
        act_map = {a.name: a for a in self._expanded.action_nodes}
        assert "act_r1" in act_map["Move_r1"].write_vars

    def test_action_update_text_no_bare_act_token(self):
        for act in self._expanded.action_nodes:
            tokens = act.update_text.split()
            assert "act" not in tokens


class TestExpanderTree:

    @pytest.fixture(autouse=True)
    def setup_expanded(self):
        self._expanded = parse_and_expand(TWOROBOT1D_MULTIAGENT)

    def test_root_node_type_is_parallel(self):
        assert self._expanded.tree.node_type == "parallel"

    def test_root_name_is_root(self):
        assert self._expanded.tree.name == "Root"

    def test_root_has_two_children(self):
        assert len(self._expanded.tree.children) == 2

    def test_r0_subtree_present(self):
        child_names = {c.name for c in self._expanded.tree.children}
        assert "RobotRoot_r0" in child_names

    def test_r1_subtree_present(self):
        child_names = {c.name for c in self._expanded.tree.children}
        assert "RobotRoot_r1" in child_names

    def test_r0_subtree_is_selector(self):
        child_map = {c.name: c for c in self._expanded.tree.children}
        assert child_map["RobotRoot_r0"].node_type == "selector"

    def test_r0_subtree_contains_atgoal_r0_leaf(self):
        def collect_leaves(node):
            if node.node_type == 'leaf':
                return {node.leaf_name}
            names = set()
            for c in node.children:
                names |= collect_leaves(c)
            return names

        child_map = {c.name: c for c in self._expanded.tree.children}
        leaves = collect_leaves(child_map["RobotRoot_r0"])
        assert "AtGoal_r0" in leaves

    def test_r0_subtree_contains_move_r0_leaf(self):
        def collect_leaves(node):
            if node.node_type == 'leaf':
                return {node.leaf_name}
            names = set()
            for c in node.children:
                names |= collect_leaves(c)
            return names

        child_map = {c.name: c for c in self._expanded.tree.children}
        leaves = collect_leaves(child_map["RobotRoot_r0"])
        assert "Move_r0" in leaves

    def test_r0_subtree_has_no_r1_leaves(self):
        def collect_leaves(node):
            if node.node_type == 'leaf':
                return {node.leaf_name}
            names = set()
            for c in node.children:
                names |= collect_leaves(c)
            return names

        child_map = {c.name: c for c in self._expanded.tree.children}
        leaves_r0 = collect_leaves(child_map["RobotRoot_r0"])
        assert "AtGoal_r1" not in leaves_r0
        assert "Move_r1" not in leaves_r0

    def test_tree_text_has_parallel(self):
        text = self._expanded.tree.to_tree_text(4)
        assert "parallel" in text

    def test_tree_text_contains_both_agent_subtrees(self):
        text = self._expanded.tree.to_tree_text(4)
        assert "RobotRoot_r0" in text
        assert "RobotRoot_r1" in text

    def test_tree_text_contains_leaf_references(self):
        text = self._expanded.tree.to_tree_text(4)
        assert "AtGoal_r0 {}" in text
        assert "AtGoal_r1 {}" in text


class TestExpanderSpecs:

    @pytest.fixture(autouse=True)
    def setup_expanded(self):
        self._expanded = parse_and_expand(TWOROBOT1D_MULTIAGENT)

    def test_total_spec_count_is_three(self):
        # 1 INVARSPEC (inline) + 2 CTLSPECs (forall splits to one per agent)
        assert len(self._expanded.specifications) == 3

    def test_one_invarspec(self):
        invars = [s for s in self._expanded.specifications if s.spec_type == "INVARSPEC"]
        assert len(invars) == 1

    def test_two_ctlspecs(self):
        ctls = [s for s in self._expanded.specifications if s.spec_type == "CTLSPEC"]
        assert len(ctls) == 2

    def test_invarspec_no_forall_over_agents(self):
        invars = [s for s in self._expanded.specifications if s.spec_type == "INVARSPEC"]
        body = invars[0].body_text
        assert "forall" not in body
        assert "agents" not in body

    def test_invarspec_contains_x_pos_r0(self):
        invars = [s for s in self._expanded.specifications if s.spec_type == "INVARSPEC"]
        assert "x_pos_r0" in invars[0].body_text

    def test_invarspec_contains_x_pos_r1(self):
        invars = [s for s in self._expanded.specifications if s.spec_type == "INVARSPEC"]
        assert "x_pos_r1" in invars[0].body_text

    def test_ctlspec_no_forall_over_agents(self):
        for spec in self._expanded.specifications:
            if spec.spec_type == "CTLSPEC":
                assert "forall, i, agents" not in spec.body_text

    def test_ctlspec_one_has_x_pos_r0(self):
        ctls = [s for s in self._expanded.specifications if s.spec_type == "CTLSPEC"]
        assert any("x_pos_r0" in s.body_text for s in ctls)

    def test_ctlspec_one_has_x_pos_r1(self):
        ctls = [s for s in self._expanded.specifications if s.spec_type == "CTLSPEC"]
        assert any("x_pos_r1" in s.body_text for s in ctls)

    def test_ctlspec_goal_x_not_literal(self):
        for spec in self._expanded.specifications:
            if spec.spec_type == "CTLSPEC":
                assert "goal_x" not in spec.body_text

    def test_ctlspec_contains_at_minus_one(self):
        ctls = [s for s in self._expanded.specifications if s.spec_type == "CTLSPEC"]
        assert any("at -1" in s.body_text for s in ctls)


class TestMultiAgentScenarios:

    def test_threeinarring_parses(self):
        model = parse_tree_file(THREE_IN_RING)
        assert model is not None
        assert len(model.agent_types) == 1
        assert len(model.agents) == 3

    def test_threeinarring_expands_without_error(self):
        expanded = parse_and_expand(THREE_IN_RING)
        assert expanded is not None

    def test_threeinarring_three_bl_vars(self):
        expanded = parse_and_expand(THREE_IN_RING)
        bl_names = {v.name for v in expanded.variables if v.scope == "bl"}
        assert "act_r0" in bl_names
        assert "act_r1" in bl_names
        assert "act_r2" in bl_names

    def test_threeinarring_three_env_vars(self):
        expanded = parse_and_expand(THREE_IN_RING)
        env_names = {v.name for v in expanded.variables if v.scope == "env"}
        assert "x_pos_r0" in env_names
        assert "x_pos_r1" in env_names
        assert "x_pos_r2" in env_names

    def test_threeinarring_parallel_has_three_children(self):
        expanded = parse_and_expand(THREE_IN_RING)
        assert expanded.tree.node_type == "parallel"
        assert len(expanded.tree.children) == 3

    def test_threeinarring_env_update_has_all_three_agents(self):
        expanded = parse_and_expand(THREE_IN_RING)
        text = expanded.environment_update_text
        assert "x_pos_r0" in text
        assert "x_pos_r1" in text
        assert "x_pos_r2" in text

    def test_threeinarring_env_update_no_index_loop(self):
        expanded = parse_and_expand(THREE_IN_RING)
        assert "x_pos[i]" not in expanded.environment_update_text

    def test_threeinarring_invarspec_no_agent_names_as_tokens(self):
        expanded = parse_and_expand(THREE_IN_RING)
        invars = [s for s in expanded.specifications if s.spec_type == "INVARSPEC"]
        assert len(invars) >= 1
        body = invars[0].body_text
        assert "forall" not in body

    def test_threeinarring_ctlspecs_split_per_agent(self):
        # 2 CTLSPECs in template × 3 agents = 6 CTLSPECs
        expanded = parse_and_expand(THREE_IN_RING)
        ctls = [s for s in expanded.specifications if s.spec_type == "CTLSPEC"]
        assert len(ctls) == 6

    def test_twodlivelock_parses(self):
        model = parse_tree_file(TWOD_LIVELOCK)
        assert model is not None
        assert len(model.agents) == 2

    def test_twodlivelock_expands_without_error(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        assert expanded is not None

    def test_twodlivelock_four_env_vars(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        env_names = {v.name for v in expanded.variables if v.scope == "env"}
        assert "x_pos_r0" in env_names
        assert "x_pos_r1" in env_names
        assert "y_pos_r0" in env_names
        assert "y_pos_r1" in env_names

    def test_twodlivelock_two_bl_vars(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        bl_names = {v.name for v in expanded.variables if v.scope == "bl"}
        assert "act_r0" in bl_names
        assert "act_r1" in bl_names

    def test_twodlivelock_parallel_has_two_children(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        assert expanded.tree.node_type == "parallel"
        assert len(expanded.tree.children) == 2

    def test_twodlivelock_pathclear_checks_passed_through(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        check_names = {ck.name for ck in expanded.environment_checks}
        assert "PathClear_r0" in check_names
        assert "PathClear_r1" in check_names

    def test_twodlivelock_pathclear_condition_uses_flat_names(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        ck_map = {ck.name: ck for ck in expanded.environment_checks}
        cond = ck_map["PathClear_r0"].condition_text
        assert "x_pos_r0" in cond
        assert "x_pos_r1" in cond
        assert "[r0]" not in cond
        assert "[r1]" not in cond

    def test_twodlivelock_env_update_has_y_pos_statements(self):
        expanded = parse_and_expand(TWOD_LIVELOCK)
        text = expanded.environment_update_text
        assert "y_pos_r0" in text
        assert "y_pos_r1" in text

    def test_fiveinring_parses(self):
        model = parse_tree_file(FIVE_IN_RING)
        assert model is not None
        assert len(model.agents) == 5

    def test_fiveinring_expands_without_error(self):
        expanded = parse_and_expand(FIVE_IN_RING)
        assert expanded is not None

    def test_fiveinring_five_bl_vars(self):
        expanded = parse_and_expand(FIVE_IN_RING)
        bl_names = {v.name for v in expanded.variables if v.scope == "bl"}
        for agent in ["r0", "r1", "r2", "r3", "r4"]:
            assert f"act_{agent}" in bl_names

    def test_fiveinring_five_env_vars(self):
        expanded = parse_and_expand(FIVE_IN_RING)
        env_names = {v.name for v in expanded.variables if v.scope == "env"}
        for agent in ["r0", "r1", "r2", "r3", "r4"]:
            assert f"x_pos_{agent}" in env_names

    def test_fiveinring_parallel_has_five_children(self):
        expanded = parse_and_expand(FIVE_IN_RING)
        assert expanded.tree.node_type == "parallel"
        assert len(expanded.tree.children) == 5

    def test_fiveinring_env_initial_values_distinct(self):
        expanded = parse_and_expand(FIVE_IN_RING)
        env_map = {v.name: v for v in expanded.variables if v.scope == "env"}
        assert env_map["x_pos_r0"].initial_value == 0
        assert env_map["x_pos_r1"].initial_value == 1
        assert env_map["x_pos_r2"].initial_value == 2
        assert env_map["x_pos_r3"].initial_value == 3
        assert env_map["x_pos_r4"].initial_value == 4

    def test_fiveinring_ctlspecs_split_per_agent(self):
        # 2 CTLSPECs in template × 5 agents = 10 CTLSPECs
        expanded = parse_and_expand(FIVE_IN_RING)
        ctls = [s for s in expanded.specifications if s.spec_type == "CTLSPEC"]
        assert len(ctls) == 10

    def test_fiveinring_env_update_no_index_loop(self):
        expanded = parse_and_expand(FIVE_IN_RING)
        assert "x_pos[i]" not in expanded.environment_update_text


class TestMaybeExpand:

    def setup_method(self):
        self.ae = _import_expander()

    def test_returns_original_for_single_agent_file(self):
        path = str(TWOROBOT1D_ORIGINAL)
        result = self.ae.maybe_expand(path)
        assert result == path

    def test_returns_different_path_for_multiagent_file(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        assert result != path

    def test_temp_file_exists_after_expansion(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        assert Path(result).exists()

    def test_temp_file_has_tree_suffix(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        assert result.endswith(".tree")

    def test_temp_file_is_parseable_by_standard_grammar(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        mm = load_metamodel()
        model = mm.model_from_file(result)
        assert model is not None

    def test_temp_file_has_no_agent_types_section(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        content = Path(result).read_text()
        assert "agent_types {" not in content
        assert "agent_type {" not in content

    def test_temp_file_has_no_agents_block(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        content = Path(result).read_text()
        assert "\nagents {" not in content

    def test_temp_file_has_no_array_syntax(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        content = Path(result).read_text()
        assert "[agents]" not in content
        assert "[self]" not in content

    def test_temp_file_contains_expanded_var_names(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        content = Path(result).read_text()
        assert "x_pos_r0" in content
        assert "x_pos_r1" in content
        assert "act_r0" in content
        assert "act_r1" in content

    def test_fallback_on_nonexistent_file(self):
        path = "/nonexistent/does_not_exist.tree"
        result = self.ae.maybe_expand(path)
        assert result == path

    def test_threeinarring_temp_file_is_parseable(self):
        require_textx()
        path = str(THREE_IN_RING)
        result = self.ae.maybe_expand(path)
        mm = load_metamodel()
        model = mm.model_from_file(result)
        assert model is not None

    def test_fiveinring_temp_file_is_parseable(self):
        require_textx()
        path = str(FIVE_IN_RING)
        result = self.ae.maybe_expand(path)
        mm = load_metamodel()
        model = mm.model_from_file(result)
        assert model is not None

    def test_twodlivelock_temp_file_is_parseable(self):
        require_textx()
        path = str(TWOD_LIVELOCK)
        result = self.ae.maybe_expand(path)
        mm = load_metamodel()
        model = mm.model_from_file(result)
        assert model is not None

    def test_temp_file_standard_grammar_has_no_agent_types_attr(self):
        require_textx()
        path = str(TWOROBOT1D_MULTIAGENT)
        result = self.ae.maybe_expand(path)
        mm = load_metamodel()
        model = mm.model_from_file(result)
        agent_types = getattr(model, "agent_types", [])
        assert len(agent_types) == 0
