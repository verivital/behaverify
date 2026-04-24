"""
Pure unit tests for AST-to-text serializers using mock SimpleNamespace nodes.

Tests: _cs_to_text, _func_to_text, _assign_to_text, _domain_to_text
"""

from types import SimpleNamespace as NS

from .conftest import (
    _import_expander,
    _cs_ref, _cs_int, _cs_str, _cs_indexed, _cs_agent_param, _cs_func, _cs_status,
    _make_assign, _make_domain_range, _make_domain_bool, _make_domain_int, _make_domain_enum,
)


class TestCsToText:

    def setup_method(self):
        self.ae = _import_expander()

    def test_none_returns_none_string(self):
        assert self.ae._cs_to_text(None) == 'None'

    def test_atom_reference(self):
        cs = _cs_ref('x_pos')
        assert self.ae._cs_to_text(cs) == 'x_pos'

    def test_atom_int_constant(self):
        cs = _cs_int(42)
        assert self.ae._cs_to_text(cs) == '42'

    def test_atom_zero_constant(self):
        cs = _cs_int(0)
        assert self.ae._cs_to_text(cs) == '0'

    def test_atom_string_constant_quoted(self):
        cs = _cs_str('Ea')
        result = self.ae._cs_to_text(cs)
        assert result == "'Ea'"

    def test_atom_negative_int(self):
        cs = _cs_int(-1)
        assert self.ae._cs_to_text(cs) == '-1'

    def test_indexed_var_simple(self):
        cs = _cs_indexed('x_pos', 'i')
        assert self.ae._cs_to_text(cs) == 'x_pos[i]'

    def test_indexed_var_self(self):
        cs = _cs_indexed('x_pos', 'self')
        assert self.ae._cs_to_text(cs) == 'x_pos[self]'

    def test_indexed_var_with_at(self):
        at_cs = _cs_int(-1)
        cs = _cs_indexed('x_pos', 'i', read_at_idx=at_cs)
        result = self.ae._cs_to_text(cs)
        assert result == 'x_pos[i] at -1'

    def test_agent_param_ref(self):
        cs = _cs_agent_param('i', 'start_x')
        assert self.ae._cs_to_text(cs) == 'agents[i].start_x'

    def test_agent_param_ref_different_param(self):
        cs = _cs_agent_param('j', 'goal_y')
        assert self.ae._cs_to_text(cs) == 'agents[j].goal_y'

    def test_function_call_wraps_parens(self):
        cs = _cs_func('eq', _cs_ref('x'), _cs_int(0))
        result = self.ae._cs_to_text(cs)
        assert result.startswith('(')
        assert result.endswith(')')

    def test_function_call_eq(self):
        cs = _cs_func('eq', _cs_ref('x'), _cs_int(0))
        assert self.ae._cs_to_text(cs) == '(eq, x, 0)'

    def test_function_call_add(self):
        cs = _cs_func('add', _cs_ref('x'), _cs_int(1))
        assert self.ae._cs_to_text(cs) == '(add, x, 1)'

    def test_function_call_not(self):
        cs = _cs_func('not', _cs_func('eq', _cs_ref('a'), _cs_ref('b')))
        result = self.ae._cs_to_text(cs)
        assert result == '(not, (eq, a, b))'

    def test_function_call_and_two_args(self):
        cs = _cs_func('and', _cs_func('eq', _cs_ref('a'), _cs_int(1)),
                              _cs_func('eq', _cs_ref('b'), _cs_int(2)))
        result = self.ae._cs_to_text(cs)
        assert result == '(and, (eq, a, 1), (eq, b, 2))'

    def test_status_function_success(self):
        cs = _cs_status('success', _cs_ref('MyNode'))
        result = self.ae._cs_to_text(cs)
        assert result == '(success, MyNode)'

    def test_status_function_failure(self):
        cs = _cs_status('failure', _cs_ref('RobotRoot'))
        result = self.ae._cs_to_text(cs)
        assert result == '(failure, RobotRoot)'


class TestFuncToText:

    def setup_method(self):
        self.ae = _import_expander()

    def _make_func(self, fname, *values):
        return NS(
            function_name=fname, values=list(values),
            loop_variable=None, loop_condition=None, loop_variable_domain=None,
            min_val=None, max_val=None, reverse=False,
            bound=None, to_index=None, constant_index=None,
            node_name=None, read_at=None, trace_num=None,
            cond_value=None, default_value=None,
        )

    def test_regular_binary_function(self):
        func = self._make_func('eq', _cs_ref('x'), _cs_int(0))
        assert self.ae._func_to_text(func) == 'eq, x, 0'

    def test_regular_unary_function(self):
        func = self._make_func('neg', _cs_ref('x'))
        assert self.ae._func_to_text(func) == 'neg, x'

    def test_regular_ternary_function(self):
        func = self._make_func('if', _cs_ref('c'), _cs_int(1), _cs_int(0))
        assert self.ae._func_to_text(func) == 'if, c, 1, 0'

    def test_forall_function(self):
        func = self._make_func('forall', _cs_ref('i'), _cs_ref('agents'), _cs_ref('body'))
        result = self.ae._func_to_text(func)
        assert result.startswith('forall,')
        assert 'i' in result
        assert 'agents' in result

    def test_exists_function(self):
        func = self._make_func('exists', _cs_ref('i'), _cs_ref('agents'), _cs_ref('body'))
        result = self.ae._func_to_text(func)
        assert result.startswith('exists,')

    def test_always_globally_function(self):
        func = self._make_func('always_globally', _cs_ref('p'))
        assert self.ae._func_to_text(func) == 'always_globally, p'

    def test_status_success(self):
        func = NS(
            function_name='success', values=[],
            node_name=_cs_ref('MyNode'),
            loop_variable=None, loop_condition=None, loop_variable_domain=None,
            min_val=None, max_val=None, reverse=False,
            bound=None, to_index=None, constant_index=None,
            read_at=None, trace_num=None,
            cond_value=None, default_value=None,
        )
        assert self.ae._func_to_text(func) == 'success, MyNode'

    def test_status_running(self):
        func = NS(
            function_name='running', values=[],
            node_name=_cs_ref('RootNode'),
            loop_variable=None, loop_condition=None, loop_variable_domain=None,
            min_val=None, max_val=None, reverse=False,
            bound=None, to_index=None, constant_index=None,
            read_at=None, trace_num=None,
            cond_value=None, default_value=None,
        )
        assert self.ae._func_to_text(func) == 'running, RootNode'

    def test_no_args_function(self):
        func = self._make_func('True')
        assert self.ae._func_to_text(func) == 'True, '


class TestAssignToText:

    def setup_method(self):
        self.ae = _import_expander()

    def test_simple_default_result(self):
        assign = _make_assign(default_values=[_cs_str('XX')])
        text = self.ae._assign_to_text(assign)
        assert "assign{" in text
        assert "result {" in text
        assert "'XX'" in text

    def test_int_default_result(self):
        assign = _make_assign(default_values=[_cs_int(0)])
        text = self.ae._assign_to_text(assign)
        assert "result {0}" in text or "result { 0}" in text

    def test_case_and_default(self):
        cond = _cs_func('eq', _cs_ref('act'), _cs_str('Ea'))
        assign = _make_assign(
            cases=[(cond, [_cs_int(1)])],
            default_values=[_cs_int(0)],
        )
        text = self.ae._assign_to_text(assign)
        assert "case {" in text
        assert "'Ea'" in text
        assert "result {1}" in text or "result { 1}" in text
        assert "result {0}" in text or "result { 0}" in text

    def test_multiple_cases(self):
        c1 = _cs_func('eq', _cs_ref('act'), _cs_str('We'))
        c2 = _cs_func('eq', _cs_ref('act'), _cs_str('Ea'))
        assign = _make_assign(
            cases=[(c1, [_cs_int(0)]), (c2, [_cs_int(1)])],
            default_values=[_cs_ref('x')],
        )
        text = self.ae._assign_to_text(assign)
        assert text.count("case {") == 2
        assert "'We'" in text
        assert "'Ea'" in text

    def test_none_assign_returns_fallback(self):
        text = self.ae._assign_to_text(None)
        assert "assign{" in text
        assert "result{0}" in text

    def test_result_with_multiple_values(self):
        assign = _make_assign(default_values=[_cs_str('We'), _cs_str('Ea')])
        text = self.ae._assign_to_text(assign)
        assert "'We'" in text
        assert "'Ea'" in text


class TestDomainToText:

    def setup_method(self):
        self.ae = _import_expander()

    def test_boolean_domain(self):
        domain = _make_domain_bool()
        assert self.ae._domain_to_text(domain) == 'BOOLEAN'

    def test_int_domain(self):
        domain = _make_domain_int()
        assert self.ae._domain_to_text(domain) == 'INT'

    def test_range_domain(self):
        domain = _make_domain_range(_cs_int(0), _cs_int(4))
        result = self.ae._domain_to_text(domain)
        assert result == '[0, 4]'

    def test_range_domain_negative(self):
        domain = _make_domain_range(_cs_int(-5), _cs_int(5))
        result = self.ae._domain_to_text(domain)
        assert '-5' in result
        assert '5' in result

    def test_enum_domain(self):
        domain = _make_domain_enum(_cs_str('We'), _cs_str('Ea'), _cs_str('XX'))
        result = self.ae._domain_to_text(domain)
        assert "'We'" in result
        assert "'Ea'" in result
        assert "'XX'" in result
        assert result.startswith('{')
        assert result.endswith('}')

    def test_none_domain_returns_int(self):
        assert self.ae._domain_to_text(None) == 'INT'

    def test_range_domain_with_ref(self):
        domain = _make_domain_range(_cs_ref('min_val'), _cs_ref('max_val'))
        result = self.ae._domain_to_text(domain)
        assert 'min_val' in result
        assert 'max_val' in result
