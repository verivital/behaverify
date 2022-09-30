import py_trees


def create_root(print_pic=False):
    parent = py_trees.composites.Selector('selector', memory = False)
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    d3 = py_trees.behaviours.Dummy('child3')
    parent.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(parent, target_directory = '../pictures')#works

        
    parent = py_trees.composites.Sequence('sequence', memory = False)
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    d3 = py_trees.behaviours.Dummy('child3')
    parent.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(parent, target_directory = '../pictures')#works


        
    parent = py_trees.composites.Parallel('parallel')
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    d3 = py_trees.behaviours.Dummy('child3')
    parent.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(parent, target_directory = '../pictures')#works

create_root(True)
