import py_trees


def create_root(print_pic=False):
    sel1 = py_trees.composites.Selector('basic_1_sel1')
    seq1 = py_trees.composites.Sequence('move_and_report')
    d1 = py_trees.behaviours.Dummy('failure_if_have_data')
    d2 = py_trees.behaviours.Dummy('move_to_location')
    d3 = py_trees.behaviours.Dummy('report_success')
    sel1.add_children([d1, seq1])
    seq1.add_children([d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return seq1
