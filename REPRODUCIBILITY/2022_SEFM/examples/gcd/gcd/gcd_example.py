import py_trees
import operator
import random

def create_root(print_pic = False, val1 = -2, val2 = -2):

    blackboard = py_trees.blackboard.Client()
    blackboard.register_key(key = "r", access = py_trees.common.Access.WRITE)
    blackboard.register_key(key = "q", access = py_trees.common.Access.WRITE)
    blackboard.register_key(key = "temp", access = py_trees.common.Access.WRITE)
    blackboard.register_key(key = "r_q_compare", access = py_trees.common.Access.WRITE)

    
    if val1 == -2:
        blackboard.r = random.randint(1, 100)
    else:
        blackboard.r = val1
    if val2 == -2:
        blackboard.q = random.randint(1, 100)
    else:
        blackboard.q = val2
    blackboard.temp = -1

    blackboard.r_q_compare = 1

    gcd_root=py_trees.composites.Selector('gcd_root')
    sub_seq=py_trees.composites.Sequence('subtract_seq')
    set_r_q_compare = py_trees.behaviours.SetBlackboardVariable('r_q_compare', lambda : 1 if blackboard.r >= blackboard.q else 0, True, 'set_comparison_value')
    check_r_q_compare = py_trees.behaviours.CheckBlackboardVariableValue(py_trees.common.ComparisonExpression('r_q_compare', 1, operator.eq), 'check_r_gte_q')
    sub=py_trees.behaviours.SetBlackboardVariable('r', lambda : blackboard.r - blackboard.q, True, 'r_minus_q')
    swap_seq=py_trees.composites.Sequence('swap_seq')
    store_r=py_trees.behaviours.SetBlackboardVariable('temp', lambda : blackboard.r, True, 'store_r')
    update_r=py_trees.behaviours.SetBlackboardVariable('r', lambda : blackboard.q, True, 'update_r')
    update_q=py_trees.behaviours.SetBlackboardVariable('q', lambda : blackboard.temp, True, 'update_q')
    
    gcd_root.add_children([sub_seq, swap_seq])

    sub_seq.add_children([set_r_q_compare, check_r_q_compare, sub])
    
    swap_seq.add_children([store_r, update_r, update_q])

    if print_pic:
        py_trees.display.render_dot_tree(gcd_root, with_blackboard_variables=True)

    return gcd_root
