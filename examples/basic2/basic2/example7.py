import py_trees


def create_root(print_pic=False):
    sel1 = py_trees.composites.Selector('example_7_sel1')
    sel2 = py_trees.composites.Selector('sel2')
    seq1 = py_trees.composites.Sequence('seq1')
    seq2 = py_trees.composites.Sequence('seq2')
    seq3 = py_trees.composites.Sequence('seq3')
    seq4 = py_trees.composites.Sequence('seq4')
    d1 = py_trees.behaviours.Dummy('leaf_1')
    d2 = py_trees.behaviours.Dummy('leaf_2')
    d3 = py_trees.behaviours.Dummy('leaf_3')
    d4 = py_trees.behaviours.Dummy('leaf_4')
    d5 = py_trees.behaviours.Dummy('leaf_5')
    d6 = py_trees.behaviours.Dummy('leaf_6')
    d7 = py_trees.behaviours.Dummy('leaf_7')
    d8 = py_trees.behaviours.Dummy('leaf_8')
    d9 = py_trees.behaviours.Dummy('leaf_9')
    d10 = py_trees.behaviours.Dummy('leaf_10')
    sel1.add_children([seq1, seq2])
    seq1.add_children([d1, d2, d3, d4])
    seq2.add_children([d5, sel2, seq3])
    sel2.add_children([d6, seq4])
    seq4.add_children([d7, d8])
    seq3.add_children([d9, d10])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return sel1
