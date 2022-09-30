import py_trees


def create_root(print_pic=False):
    sel1 = py_trees.composites.Selector('basic_1_sel1')
    seq1 = py_trees.composites.Sequence('move_and_report')
    d1 = py_trees.behaviours.Dummy('destination_known')
    sif = py_trees.decorators.SuccessIsFailure(name="SiF", child=d1)
    d2 = py_trees.behaviours.Dummy('move_to_destination')
    d3 = py_trees.behaviours.Dummy('report_success')
    sel1.add_children([sif, seq1])
    seq1.add_children([d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return sel1

create_root(True)
