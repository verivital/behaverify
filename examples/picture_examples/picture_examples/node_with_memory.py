import py_trees


def create_root(print_pic=False):
    has_memory = py_trees.composites.Sequence('has_memory')
    has_amnesia = py_trees.composites.Sequence('has_amnesia', memory = False)
    #has_memory.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(has_memory, target_directory = '../pictures')#works
        py_trees.display.render_dot_tree(has_amnesia, target_directory = '../pictures')#works
    return True

create_root(True)
