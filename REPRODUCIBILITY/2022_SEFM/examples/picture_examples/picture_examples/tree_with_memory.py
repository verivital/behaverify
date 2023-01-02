import py_trees


def create_root(print_pic=False):
    has_memory = py_trees.composites.Sequence('has_memory')
    success_baby = py_trees.behaviours.Success('child_that_became_a_doctor')
    running_baby = py_trees.behaviours.Running('child_that_became_a_runner')
    has_memory.add_children([success_baby, running_baby])
    if print_pic:
        py_trees.display.render_dot_tree(has_memory, target_directory = '../pictures')#works
    has_amnesia = py_trees.composites.Sequence('has_amnesia', memory = False)
    success_baby = py_trees.behaviours.Success('child_that_became_a_doctor')
    running_baby = py_trees.behaviours.Running('child_that_became_a_runner')
    has_amnesia.add_children([success_baby, running_baby])
    if print_pic:
        py_trees.display.render_dot_tree(has_amnesia, target_directory = '../pictures')#works
    return True

create_root(True)
