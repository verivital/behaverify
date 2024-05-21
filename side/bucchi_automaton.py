def guard__T0_init__TO__T0_S1(model_info):
    return True
def guard__T0_init__TO__accept_all(model_info):
    return model_info['p3']
def guard__T0_init__TO__accept_S5(model_info):
    return True
def guard__T0_init__TO__accept_S4(model_info):
    return (not model_info['p4']) and model_info['p5']
def guard__T0_S1__TO__T0_S1(model_info):
    return True
def guard__T0_S1__TO__accept_all(model_info):
    return model_info['p3']
def guard__accept_S5__TO__accept_all(model_info):
    return (not model_info['p1']) and (not model_info['p2'])
def guard__accept_S4__TO__accept_S4(model_info):
    return (not model_info['p4'])
def guard__accept_all__TO__accept_all(model_info):
    return True


STATE_TRANS = {
    'T0_init' : {
        (guard__T0_init__TO__T0_S1, 'T0_S1'),
        (guard__T0_init__TO__accept_all, 'accept_all'),
        (guard__T0_init__TO__accept_S5, 'accept_S5'),
        (guard__T0_init__TO__accept_S4, 'accept_S4')
    },
    'T0_S1' : {
        (guard__T0_S1__TO__T0_S1, 'T0_S1'),
        (guard__T0_S1__TO__accept_all, 'accept_all')
    },
    'accept_S5' : {
        (guard__accept_S5__TO__accept_all, 'accept_all')
    },
    'accept_S4' : {
        (guard__accept_S4__TO__accept_S4, 'accept_S4')
    },
    'accept_all' : {
        (guard__accept_all__TO__accept_all, 'accept_all')
    }
}

def p1_func(model_state):
    return model_state['p1']

def p2_func(model_state):
    return model_state['p2']

def p3_func(model_state):
    return model_state['p3']

def p4_func(model_state):
    return model_state['p4']

def p5_func(model_state):
    return model_state['p5']

MODEL_INFO_FUNCTIONS = {
    'p1' : p1_func,
    'p2' : p2_func,
    'p3' : p3_func,
    'p4' : p4_func,
    'p5' : p5_func
}

def model_state_to_model_info(model_state):
    return {
        key : item(model_state)
        for (key, item) in MODEL_INFO_FUNCTIONS.items()
    }


def transition(automaton_states, model_state):
    if 'accept_all' in automaton_states:
        return ({'accept_all'}, 'safe')
    if len(automaton_states) == 0:
        return (set(), 'unsafe')
    model_info = model_state_to_model_info(model_state)
    new_automaton_states = {
        new_automaton_state
        for automaton_state in automaton_states
        for (guard, new_automaton_state) in STATE_TRANS[automaton_state]
        if guard(model_info)
    }
    if 'accept_all' in new_automaton_states:
        return ({'accept_all'}, 'safe')
    if len(new_automaton_states) == 0:
        return (set(), 'unsafe')
    return (new_automaton_states, 'unknown')


import random
def test_loop(max_iter):
    current_states = {'T0_init'}
    rb = (True, False)
    for count in range(max_iter):
        model_state = {
            key : random.choice(rb)
            for key in MODEL_INFO_FUNCTIONS
        }
        (current_states, status) = transition(current_states, model_state)
        print('--------------------' + str(count))
        print(model_state)
        print(current_states)
        print(status)
    return

if __name__ == '__main__':
    test_loop(10)
