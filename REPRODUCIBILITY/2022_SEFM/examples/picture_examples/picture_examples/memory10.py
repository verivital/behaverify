import py_trees


def create_root(print_pic=False):
    has_amnesia = py_trees.composites.Sequence('memory10', memory = True)
    for i in range(10):
        has_amnesia.add_child(py_trees.behaviours.Dummy(str(i)))
    #has_memory.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(has_amnesia, target_directory = '../pictures')#works
    return True

create_root(True)
