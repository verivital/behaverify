import py_trees


def create_root(mem1, mem2, node1, node2, print_pic=False):
    if node1 == "sel":
        sel1 = py_trees.composites.Selector('node1', memory = mem1)
    elif node1 == "seq":
        sel1 = py_trees.composites.Sequence('node1', memory = mem1)
    else:
        sel1 = py_trees.composites.Parallel('node1', py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = mem1))
    
    if node2 == "sel":
        sel2 = py_trees.composites.Selector('node2', memory = mem2)
    elif node2 == "seq":
        sel2 = py_trees.composites.Sequence('node2', memory = mem2)
    else:
        sel2 = py_trees.composites.Parallel('node2', py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = mem2))
    d1 = py_trees.behaviours.Dummy('node_w')
    d2 = py_trees.behaviours.Dummy('node_x')
    d3 = py_trees.behaviours.Dummy('node_y')
    d4 = py_trees.behaviours.Dummy('node_z')
    sel1.add_children([d1, sel2])
    sel2.add_children([d2, d3, d4])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return sel1


