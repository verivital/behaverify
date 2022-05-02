import py_trees
import operator


def create_root():
    
    a_s = py_trees.common.ParallelPolicy.SuccessOnAll()
    a_u = py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = False)
    o_s = py_trees.common.ParallelPolicy.SuccessOnOne()
    
    root_node=py_trees.composites.Sequence('root')
    s1 = py_trees.composites.Selector('s1')
    s2 = py_trees.composites.Selector('s2')
    s3 = py_trees.composites.Selector('s3')
    s4 = py_trees.composites.Selector('s4')
    s5 = py_trees.composites.Selector('s5')
    d1 = py_trees.behaviours.Dummy('d1')
    d2 = py_trees.behaviours.Dummy('d2')
    d3 = py_trees.behaviours.Dummy('d3')
    d4 = py_trees.behaviours.Dummy('d4')
    d5 = py_trees.behaviours.Dummy('d5')
    d6 = py_trees.behaviours.Dummy('d6')
    d7 = py_trees.behaviours.Dummy('d7')
    d8 = py_trees.behaviours.Dummy('d8')
    d9 = py_trees.behaviours.Dummy('d9')
    d10 = py_trees.behaviours.Dummy('d10')
    d11 = py_trees.behaviours.Dummy('d11')
    d12 = py_trees.behaviours.Dummy('d12')
    d13 = py_trees.behaviours.Dummy('d13')
    d14 = py_trees.behaviours.Dummy('d14')
    d15 = py_trees.behaviours.Dummy('d15')
    d16 = py_trees.behaviours.Dummy('d16')
    d17 = py_trees.behaviours.Dummy('d17')
    d18 = py_trees.behaviours.Dummy('d18')
    d19 = py_trees.behaviours.Dummy('d19')
    d20 = py_trees.behaviours.Dummy('d20')
    p_a_s = py_trees.composites.Parallel('p_a_s', a_s)
    p_a_u = py_trees.composites.Parallel('p_a_u', a_u)
    p_o_s = py_trees.composites.Parallel('p_o_s', o_s)
    p_o_s2 = py_trees.composites.Parallel('p_o_s2', o_s)

    root_node.add_children([d1, d2,  p_a_s, d3])
    p_a_s.add_children([d4, d5, s1])
    s1.add_children([p_a_u, d6])
    p_a_u.add_children([s2, d7, d8, p_o_s2])
    s2.add_children([d9, d10, s3, p_o_s])
    p_o_s2.add_children([s4, d11, d12])
    s3.add_children([d13, d14, d15])
    p_o_s.add_children([d16, s5])
    s4.add_children([d17, d18])
    s5.add_children([d19, d20])
    
    #py_trees.display.render_dot_tree(root_node)

    return root_node
