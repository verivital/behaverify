import py_trees
import operator


def create_root():
    root_node=py_trees.composites.Sequence('root')
    guard_node_a=py_trees.composites.Selector('guard_node')
    a_exists=py_trees.behaviours.CheckBlackboardVariableExists('a', 'check_a_exists')
    create_a=py_trees.behaviours.SetBlackboardVariable('a', 'int', False, 'init_a')
    guard_node_b=py_trees.composites.Selector('guard_node')
    b_exists=py_trees.behaviours.CheckBlackboardVariableExists('b', 'check_b_exists')
    create_b=py_trees.behaviours.SetBlackboardVariable('b', 'int', False, 'init_b')

    gcd_root=py_trees.composites.Selector('gcd_root')
    sub_seq=py_trees.composites.Sequence('subtract_seq')
    check_r_gt_q=py_trees.behaviours.CheckBlackboardVariableValue(py_trees.common.ComparisonExpression('r', True, operator.eq), 'check_r_gt_q')
    sub=py_trees.behaviours.SetBlackboardVariable('r', 'r-q', True, 'r_minus_q')
    swap_seq=py_trees.composites.Sequence('swap_seq')
    store_r=py_trees.behaviours.SetBlackboardVariable('temp', 'r', True, 'store_r')
    update_r=py_trees.behaviours.SetBlackboardVariable('r', 'q', True, 'update_r')
    update_q=py_trees.behaviours.SetBlackboardVariable('q', 'temp', True, 'update_q')

    root_node.add_children([guard_node_a, guard_node_b,  gcd_root])
    guard_node_a.add_children([a_exists, create_a])
    guard_node_b.add_children([b_exists, create_b])
    
    gcd_root.add_children([sub_seq, swap_seq])

    sub_seq.add_children([check_r_gt_q, sub])
    swap_seq.add_children([store_r, update_r, update_q])

    #py_trees.display.render_dot_tree(root_node, with_blackboard_variables=True)

    return root_node
