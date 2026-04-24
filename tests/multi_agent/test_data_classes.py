"""
Pure unit tests for ExpandedModel data classes and model_to_tree_text serialization.

Tests: ExpandedVariable, ExpandedCheck, ExpandedAction, ExpandedTreeNode,
       ExpandedSpec, ExpandedModel, model_to_tree_text
"""

from .conftest import _import_expander


class TestDataClasses:

    def setup_method(self):
        self.ae = _import_expander()

    def test_expanded_variable_numeric_initial(self):
        ev = self.ae.ExpandedVariable("x_pos_r0", "env", "[0, 4]", initial_value=0)
        text = ev.to_tree_text()
        assert "env" in text
        assert "x_pos_r0" in text
        assert "[0, 4]" in text
        assert "0" in text

    def test_expanded_variable_string_initial(self):
        ev = self.ae.ExpandedVariable("act_r0", "bl", "{'We','Ea','XX'}", initial_value="XX")
        text = ev.to_tree_text()
        assert "bl" in text
        assert "act_r0" in text
        assert "'XX'" in text

    def test_expanded_variable_initial_text_overrides(self):
        ev = self.ae.ExpandedVariable(
            "act_r0", "bl", "{'We','Ea','XX'}",
            initial_value=0,
            initial_text="assign{result{'XX'}}"
        )
        text = ev.to_tree_text()
        assert "assign{result{'XX'}}" in text

    def test_expanded_variable_format(self):
        ev = self.ae.ExpandedVariable("x_pos_r0", "env", "[0, 4]", initial_value=2)
        text = ev.to_tree_text()
        assert text.startswith("variable {")
        assert "VAR" in text
        assert "assign{" in text

    def test_expanded_check_to_text_content(self):
        ck = self.ae.ExpandedCheck(
            "AtGoal_r0", "(eq, x_pos_r0, 4)", read_vars=["x_pos_r0"]
        )
        text = ck.to_tree_text()
        assert "AtGoal_r0" in text
        assert "(eq, x_pos_r0, 4)" in text
        assert "x_pos_r0" in text

    def test_expanded_check_to_text_format(self):
        ck = self.ae.ExpandedCheck("C", "(True)")
        text = ck.to_tree_text()
        assert "environment_check {" in text
        assert "arguments {}" in text
        assert "condition {" in text

    def test_expanded_check_empty_read_vars(self):
        ck = self.ae.ExpandedCheck("MyCheck", "(True)")
        text = ck.to_tree_text()
        assert "MyCheck" in text
        assert "(True)" in text
        assert "read_variables {}" in text

    def test_expanded_action_to_text_content(self):
        act = self.ae.ExpandedAction(
            "Move_r0", ["act_r0"],
            "return_statement {result{success}}"
        )
        text = act.to_tree_text()
        assert "Move_r0" in text
        assert "act_r0" in text
        assert "write_variables" in text

    def test_expanded_action_to_text_format(self):
        act = self.ae.ExpandedAction("Move_r0", [], "return_statement {result{success}}")
        text = act.to_tree_text()
        assert "action {" in text
        assert "arguments {}" in text
        assert "update {" in text

    def test_expanded_tree_node_leaf(self):
        node = self.ae.ExpandedTreeNode(
            node_type='leaf', name='AtGoal_r0', leaf_name='AtGoal_r0'
        )
        text = node.to_tree_text(4)
        assert "AtGoal_r0 {}" in text

    def test_expanded_tree_node_leaf_indented(self):
        node = self.ae.ExpandedTreeNode(
            node_type='leaf', name='L', leaf_name='L'
        )
        text = node.to_tree_text(8)
        assert text.startswith("        ")  # 8 spaces

    def test_expanded_tree_node_parallel_content(self):
        child = self.ae.ExpandedTreeNode(
            node_type='leaf', name='L', leaf_name='L'
        )
        root = self.ae.ExpandedTreeNode(
            node_type='parallel', name='Root',
            children=[child], parallel_policy='success_on_all'
        )
        text = root.to_tree_text(4)
        assert "parallel" in text
        assert "success_on_all" in text
        assert "Root" in text
        assert "L {}" in text

    def test_expanded_tree_node_selector(self):
        child = self.ae.ExpandedTreeNode(node_type='leaf', name='L', leaf_name='L')
        node = self.ae.ExpandedTreeNode(
            node_type='selector', name='MySelector', children=[child]
        )
        text = node.to_tree_text(4)
        assert "selector" in text
        assert "MySelector" in text

    def test_expanded_tree_node_sequence(self):
        child = self.ae.ExpandedTreeNode(node_type='leaf', name='L', leaf_name='L')
        node = self.ae.ExpandedTreeNode(
            node_type='sequence', name='MySeq', children=[child]
        )
        text = node.to_tree_text(4)
        assert "sequence" in text
        assert "MySeq" in text

    def test_expanded_spec_invarspec(self):
        spec = self.ae.ExpandedSpec("INVARSPEC", "(eq, x, 0)")
        assert str(spec) == "INVARSPEC {(eq, x, 0)}"

    def test_expanded_spec_ctlspec(self):
        spec = self.ae.ExpandedSpec("CTLSPEC", "(always_globally, (eq, x, 0))")
        assert str(spec) == "CTLSPEC {(always_globally, (eq, x, 0))}"

    def test_expanded_spec_ltlspec(self):
        spec = self.ae.ExpandedSpec("LTLSPEC", "(globally, (eq, x, 0))")
        assert str(spec) == "LTLSPEC {(globally, (eq, x, 0))}"


class TestModelSerialization:

    def setup_method(self):
        self.ae = _import_expander()

    def _build_model(self):
        ae = self.ae
        expanded = ae.ExpandedModel()
        expanded.enumerations = ["We", "Ea"]
        expanded.constants_text = "max_val := 4"
        expanded.variables = [
            ae.ExpandedVariable("x_r0", "env", "[0, 4]", initial_value=0),
        ]
        expanded.environment_checks = [
            ae.ExpandedCheck("AtGoal_r0", "(eq, x_r0, 4)"),
        ]
        expanded.action_nodes = [
            ae.ExpandedAction("Move_r0", [], "return_statement {result{success}}"),
        ]
        leaf = ae.ExpandedTreeNode(node_type='leaf', name='Move_r0', leaf_name='Move_r0')
        expanded.tree = ae.ExpandedTreeNode(
            node_type='parallel', name='Root', children=[leaf]
        )
        expanded.tick_prerequisite_text = '(True)'
        expanded.specifications = [
            ae.ExpandedSpec("INVARSPEC", "(eq, x_r0, 0)"),
        ]
        return expanded

    def test_configuration_section_present(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "configuration {" in text

    def test_enumerations_section_present(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "enumerations {" in text

    def test_constants_section_present(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "constants {" in text

    def test_section_order_config_before_variables(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert text.index("configuration") < text.index("variables {")

    def test_section_order_variables_before_env_update(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert text.index("variables {") < text.index("environment_update {")

    def test_section_order_checks_before_env_checks(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert text.index("\nchecks {}") < text.index("environment_checks {")

    def test_section_order_actions_before_subtrees(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert text.index("actions {") < text.index("sub_trees {}")

    def test_section_order_tree_before_tick(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert text.index("tree {") < text.index("tick_prerequisite {")

    def test_section_order_tick_before_specs(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert text.index("tick_prerequisite {") < text.index("specifications {")

    def test_variable_name_in_output(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "x_r0" in text

    def test_check_name_in_output(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "AtGoal_r0" in text

    def test_action_name_in_output(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "Move_r0" in text

    def test_spec_in_output(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "INVARSPEC" in text
        assert "(eq, x_r0, 0)" in text

    def test_no_agent_array_syntax(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "[agents]" not in text
        assert "agents[i]" not in text
        assert "[self]" not in text

    def test_no_agent_types_section(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "agent_types {" not in text
        assert "agent_type {" not in text

    def test_no_agents_section(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "\nagents {" not in text

    def test_parallel_node_in_tree(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "parallel" in text

    def test_tick_prerequisite_value(self):
        text = self.ae.model_to_tree_text(self._build_model())
        assert "tick_prerequisite {(True)}" in text
