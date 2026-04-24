"""
Pure unit tests for string manipulation and simplification helpers.

Tests: _split_top_level, _extract_inner, _substitute,
       _simplify_agent_identities, _simplify_implies, _remove_true_from_and
"""

from .conftest import _import_expander


class TestStringHelpers:

    def setup_method(self):
        self.ae = _import_expander()

    def test_split_top_level_simple(self):
        parts = self.ae._split_top_level("a, b, c")
        assert [p.strip() for p in parts] == ["a", "b", "c"]

    def test_split_top_level_nested_parens(self):
        parts = self.ae._split_top_level("a, (b, c), d")
        stripped = [p.strip() for p in parts]
        assert stripped == ["a", "(b, c)", "d"]

    def test_split_top_level_deeply_nested(self):
        parts = self.ae._split_top_level("forall, i, agents, (eq, x_pos[i], 0)")
        stripped = [p.strip() for p in parts]
        assert stripped[0] == "forall"
        assert stripped[1] == "i"
        assert stripped[2] == "agents"
        assert "(eq, x_pos[i], 0)" in stripped[3]

    def test_split_top_level_empty(self):
        parts = self.ae._split_top_level("")
        assert parts == [] or parts == [""]

    def test_split_top_level_single_item(self):
        parts = self.ae._split_top_level("x")
        assert parts == ["x"]

    def test_split_top_level_braces_not_counted(self):
        parts = self.ae._split_top_level("a, {b, c}, d")
        stripped = [p.strip() for p in parts]
        assert stripped == ["a", "{b, c}", "d"]

    def test_extract_inner_basic(self):
        result = self.ae._extract_inner("(and, a, b)", 0)
        assert result == "and, a, b"

    def test_extract_inner_offset(self):
        result = self.ae._extract_inner("xx(foo, bar)yy", 2)
        assert result == "foo, bar"

    def test_extract_inner_nested(self):
        result = self.ae._extract_inner("(a, (b, c), d)", 0)
        assert result == "a, (b, c), d"

    def test_extract_inner_not_paren(self):
        result = self.ae._extract_inner("no parens here", 0)
        assert result is None

    def test_extract_inner_unclosed(self):
        result = self.ae._extract_inner("(unclosed", 0)
        assert result is None

    def test_substitute_basic(self):
        result = self.ae._substitute("x_pos[self]", {"x_pos[self]": "x_pos_r0"})
        assert result == "x_pos_r0"

    def test_substitute_longest_first(self):
        # Longer key "ab" must be substituted before shorter key "a".
        # Without longest-first ordering, "a" on "ab" → "Yb", making "ab" never match.
        subs = {"ab": "LONG", "a": "SHORT"}
        result = self.ae._substitute("ab", subs)
        assert result == "LONG"

    def test_substitute_multiple_keys(self):
        subs = {"x_pos[self]": "x_pos_r0", "act": "act_r0"}
        result = self.ae._substitute("act and x_pos[self]", subs)
        assert "act_r0" in result
        assert "x_pos_r0" in result
        assert "x_pos[self]" not in result

    def test_substitute_no_match(self):
        result = self.ae._substitute("hello world", {"foo": "bar"})
        assert result == "hello world"

    def test_substitute_empty_dict(self):
        result = self.ae._substitute("some text", {})
        assert result == "some text"


class TestSimplification:

    def setup_method(self):
        self.ae = _import_expander()

    def test_simplify_identities_eq_same_agent(self):
        result = self.ae._simplify_agent_identities("(eq, r0, r0)", ["r0", "r1"])
        assert result == "True"

    def test_simplify_identities_eq_different_agents(self):
        result = self.ae._simplify_agent_identities("(eq, r0, r1)", ["r0", "r1"])
        assert result == "False"

    def test_simplify_identities_neq_same_agent(self):
        result = self.ae._simplify_agent_identities("(neq, r0, r0)", ["r0", "r1"])
        assert result == "False"

    def test_simplify_identities_neq_different_agents(self):
        result = self.ae._simplify_agent_identities("(neq, r0, r1)", ["r0", "r1"])
        assert result == "True"

    def test_simplify_implies_true(self):
        result = self.ae._simplify_implies("(implies, True, (eq, x, 0))")
        assert result == "(eq, x, 0)"

    def test_simplify_implies_false(self):
        result = self.ae._simplify_implies("(implies, False, (eq, x, 0))")
        assert result == "True"

    def test_simplify_implies_no_match(self):
        original = "(implies, (eq, a, b), (eq, x, 0))"
        result = self.ae._simplify_implies(original)
        assert result == original

    def test_simplify_implies_plain_text_unchanged(self):
        result = self.ae._simplify_implies("some plain text")
        assert result == "some plain text"

    def test_remove_true_from_and_leading(self):
        result = self.ae._remove_true_from_and("(and, True, (eq, x, 0))")
        assert result == "(eq, x, 0)"

    def test_remove_true_from_and_trailing(self):
        result = self.ae._remove_true_from_and("(and, (eq, x, 0), True)")
        assert result == "(eq, x, 0)"

    def test_remove_true_from_and_no_true(self):
        original = "(and, (eq, a, 0), (eq, b, 1))"
        result = self.ae._remove_true_from_and(original)
        assert result == original

    def test_simplify_full_chain_neq(self):
        # (implies, (neq, r0, r1), BODY) → (implies, True, BODY) → BODY
        text = "(implies, (neq, r0, r1), (neq, x_pos_r0, x_pos_r1))"
        result = self.ae._simplify_agent_identities(text, ["r0", "r1"])
        assert result == "(neq, x_pos_r0, x_pos_r1)"

    def test_simplify_full_chain_same_agents_gives_true(self):
        # (implies, (neq, r0, r0), BODY) → (implies, False, BODY) → True
        text = "(implies, (neq, r0, r0), (neq, x_pos_r0, x_pos_r0))"
        result = self.ae._simplify_agent_identities(text, ["r0", "r1"])
        assert result == "True"

    def test_simplify_three_agents_neq(self):
        result = self.ae._simplify_agent_identities("(neq, r0, r2)", ["r0", "r1", "r2"])
        assert result == "True"

    def test_simplify_three_agents_eq_same(self):
        result = self.ae._simplify_agent_identities("(eq, r1, r1)", ["r0", "r1", "r2"])
        assert result == "True"
