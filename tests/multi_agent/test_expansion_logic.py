"""
Pure unit tests for expansion logic helpers.

Tests: _build_agent_subs, _substitute_agent_in_body,
       _try_extract_top_forall, _expand_spec_body, _resolve_constants
"""

from types import SimpleNamespace as NS

from .conftest import (
    _import_expander,
    _cs_ref, _cs_int,
    _make_mock_model_constants,
)


class TestBuildAgentSubs:

    def setup_method(self):
        self.ae = _import_expander()

    def test_env_array_self_substitution(self):
        subs = self.ae._build_agent_subs(
            'r0', agent_vars=[], env_arrays=['x_pos'], consts={}, params={}
        )
        assert subs['x_pos[self]'] == 'x_pos_r0'

    def test_multiple_env_arrays(self):
        subs = self.ae._build_agent_subs(
            'r1', agent_vars=[], env_arrays=['x_pos', 'y_pos'], consts={}, params={}
        )
        assert subs['x_pos[self]'] == 'x_pos_r1'
        assert subs['y_pos[self]'] == 'y_pos_r1'

    def test_agent_local_var_suffixed(self):
        subs = self.ae._build_agent_subs(
            'r0', agent_vars=['act'], env_arrays=[], consts={}, params={}
        )
        assert subs['act'] == 'act_r0'

    def test_multiple_agent_local_vars(self):
        subs = self.ae._build_agent_subs(
            'r2', agent_vars=['act', 'mode'], env_arrays=[], consts={}, params={}
        )
        assert subs['act'] == 'act_r2'
        assert subs['mode'] == 'mode_r2'

    def test_parameter_substitution(self):
        subs = self.ae._build_agent_subs(
            'r0', agent_vars=[], env_arrays=[], consts={},
            params={'goal_x': 4, 'start_x': 0}
        )
        assert subs['goal_x'] == '4'
        assert subs['start_x'] == '0'

    def test_combined_subs(self):
        subs = self.ae._build_agent_subs(
            'r1',
            agent_vars=['act'],
            env_arrays=['x_pos'],
            consts={'min_val': 0},
            params={'goal_x': 0}
        )
        assert subs['x_pos[self]'] == 'x_pos_r1'
        assert subs['act'] == 'act_r1'
        assert subs['goal_x'] == '0'

    def test_different_agent_names(self):
        subs_r0 = self.ae._build_agent_subs('r0', ['act'], ['x_pos'], {}, {})
        subs_r5 = self.ae._build_agent_subs('r5', ['act'], ['x_pos'], {}, {})
        assert subs_r0['act'] == 'act_r0'
        assert subs_r5['act'] == 'act_r5'
        assert subs_r0['x_pos[self]'] == 'x_pos_r0'
        assert subs_r5['x_pos[self]'] == 'x_pos_r5'


class TestSubstituteAgentInBody:

    def setup_method(self):
        self.ae = _import_expander()

    def _sub(self, body, var='i', agent='r0', env_arrays=None,
             agent_local_vars=None, agent_params=None):
        env_arrays = env_arrays or []
        agent_local_vars = agent_local_vars or []
        agent_params = agent_params or {}
        return self.ae._substitute_agent_in_body(
            body, var, agent, env_arrays, agent_local_vars, agent_params, {}
        )

    def test_env_array_indexed_substituted(self):
        result = self._sub('x_pos[i]', env_arrays=['x_pos'])
        assert result == 'x_pos_r0'

    def test_env_array_in_expression(self):
        result = self._sub('(eq, x_pos[i], 4)', env_arrays=['x_pos'])
        assert 'x_pos_r0' in result
        assert 'x_pos[i]' not in result

    def test_env_array_with_at(self):
        result = self._sub('x_pos[i] at -1', env_arrays=['x_pos'])
        assert 'x_pos_r0 at -1' in result

    def test_parameter_indexed_substituted(self):
        result = self._sub('goal_x[i]',
                           agent_params={'r0': {'goal_x': 4}})
        assert result == '4'

    def test_string_parameter_quoted(self):
        result = self._sub('dir[i]',
                           agent_params={'r0': {'dir': 'Ea'}})
        assert result == "'Ea'"

    def test_bare_index_var_in_neq(self):
        result = self._sub('(neq, i, j)')
        assert 'r0' in result
        assert ', i,' not in result

    def test_bare_index_var_at_end(self):
        result = self._sub('(eq, x, i)')
        assert 'r0' in result
        assert ', i)' not in result

    def test_multiple_env_arrays(self):
        result = self._sub(
            '(and, (eq, x_pos[i], 0), (eq, y_pos[i], 1))',
            env_arrays=['x_pos', 'y_pos']
        )
        assert 'x_pos_r0' in result
        assert 'y_pos_r0' in result

    def test_different_agent_name(self):
        result = self._sub('x_pos[i]', agent='r3', env_arrays=['x_pos'])
        assert result == 'x_pos_r3'

    def test_no_match_passthrough(self):
        body = '(eq, a, b)'
        result = self._sub(body)
        assert result == body


class TestTryExtractTopForall:

    def setup_method(self):
        self.ae = _import_expander()

    def test_valid_forall_over_agents(self):
        text = '(forall, i, agents, (eq, x, 0))'
        result = self.ae._try_extract_top_forall(text)
        assert result is not None
        quant, var, domain, body = result
        assert quant == 'forall'
        assert var == 'i'
        assert domain == 'agents'
        assert '(eq, x, 0)' in body

    def test_valid_exists_over_agents(self):
        text = '(exists, i, agents, (eq, x, 0))'
        result = self.ae._try_extract_top_forall(text)
        assert result is not None
        assert result[0] == 'exists'

    def test_non_quantifier_function_returns_none(self):
        text = '(always_globally, (eq, x, 0))'
        assert self.ae._try_extract_top_forall(text) is None

    def test_no_outer_parens_returns_none(self):
        assert self.ae._try_extract_top_forall('forall, i, agents, x') is None

    def test_too_few_parts_returns_none(self):
        assert self.ae._try_extract_top_forall('(forall, i, agents)') is None

    def test_non_agents_domain_still_parsed(self):
        text = '(forall, i, mylist, (eq, x, 0))'
        result = self.ae._try_extract_top_forall(text)
        assert result is not None
        assert result[2] == 'mylist'

    def test_nested_body_preserved(self):
        text = '(forall, i, agents, (always_globally, (exists_finally, (eq, x, 0))))'
        result = self.ae._try_extract_top_forall(text)
        assert result is not None
        _, _, _, body = result
        assert 'always_globally' in body
        assert 'exists_finally' in body

    def test_empty_string_returns_none(self):
        assert self.ae._try_extract_top_forall('') is None

    def test_plain_atom_returns_none(self):
        assert self.ae._try_extract_top_forall('x_pos_r0') is None


class TestExpandSpecBody:

    def setup_method(self):
        self.ae = _import_expander()

    def _expand(self, text, agent_names=None, env_arrays=None, agent_params=None):
        agent_names = agent_names or ['r0', 'r1']
        env_arrays = env_arrays or {}
        agent_params = agent_params or {n: {} for n in agent_names}
        return self.ae._expand_spec_body(
            text, agent_names, env_arrays, [], agent_params, {}
        )

    def test_forall_over_agents_becomes_and(self):
        text = '(forall, i, agents, (eq, x_pos[i], 0))'
        result = self._expand(text, env_arrays={'x_pos': {}})
        assert result.startswith('(and,')
        assert 'x_pos_r0' in result
        assert 'x_pos_r1' in result

    def test_exists_over_agents_becomes_or(self):
        text = '(exists, i, agents, (eq, x_pos[i], 0))'
        result = self._expand(text, env_arrays={'x_pos': {}})
        assert result.startswith('(or,')

    def test_no_quantifier_passthrough(self):
        text = '(eq, x_pos_r0 at -1, 4)'
        result = self._expand(text)
        assert result == text

    def test_three_agents_forall(self):
        result = self._expand(
            '(forall, i, agents, P)',
            agent_names=['r0', 'r1', 'r2']
        )
        assert result.startswith('(and,')
        assert result.count('P') == 3

    def test_nested_forall_fully_expanded(self):
        text = '(forall, i, agents, (forall, j, agents, (neq, x_pos[i], x_pos[j])))'
        result = self._expand(text, env_arrays={'x_pos': {}})
        assert 'forall' not in result
        assert 'x_pos_r0' in result
        assert 'x_pos_r1' in result

    def test_single_agent_forall_no_and_wrapper(self):
        result = self._expand(
            '(forall, i, agents, (eq, x_pos[i], 0))',
            agent_names=['r0'],
            env_arrays={'x_pos': {}}
        )
        assert 'x_pos_r0' in result
        assert 'x_pos_r1' not in result

    def test_domain_other_than_agents_not_expanded(self):
        text = '(forall, i, mylist, (eq, x, 0))'
        result = self._expand(text)
        assert result == text


class TestResolveConstants:

    def setup_method(self):
        self.ae = _import_expander()

    def test_int_constant_with_val_wrapper(self):
        model = _make_mock_model_constants(min_val=0, max_val=4)
        consts = self.ae._resolve_constants(model)
        assert consts['min_val'] == 0
        assert consts['max_val'] == 4

    def test_multiple_constants(self):
        model = _make_mock_model_constants(a=1, b=2, c=3)
        consts = self.ae._resolve_constants(model)
        assert consts == {'a': 1, 'b': 2, 'c': 3}

    def test_zero_constant(self):
        model = _make_mock_model_constants(zero=0)
        consts = self.ae._resolve_constants(model)
        assert consts['zero'] == 0

    def test_negative_constant(self):
        model = _make_mock_model_constants(neg=NS(val=-5))
        consts = self.ae._resolve_constants(model)
        assert 'neg' in consts

    def test_empty_constants(self):
        model = NS(constants=[])
        consts = self.ae._resolve_constants(model)
        assert consts == {}

    def test_resolve_value_constant(self):
        value_obj = NS(constant=NS(val=4), reference=None)
        result = self.ae._resolve_value(value_obj, {})
        assert result == 4

    def test_resolve_value_reference_to_constant(self):
        value_obj = NS(constant=None, reference='max_val')
        result = self.ae._resolve_value(value_obj, {'max_val': 4})
        assert result == 4

    def test_resolve_value_unknown_reference(self):
        value_obj = NS(constant=None, reference='unknown')
        result = self.ae._resolve_value(value_obj, {})
        assert result == 'unknown'

    def test_resolve_value_none(self):
        assert self.ae._resolve_value(None, {}) is None
