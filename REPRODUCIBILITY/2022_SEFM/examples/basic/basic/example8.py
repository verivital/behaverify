import py_trees


def create_root(print_pic=False):
    seq1 = py_trees.composites.Sequence('example_8_seq1')
    sel1 = py_trees.composites.Selector('sel1')
    sel2 = py_trees.composites.Selector('sel2')

    d1 = py_trees.behaviours.Dummy('leaf_1')
    d2 = py_trees.behaviours.Dummy('leaf_2')
    d3 = py_trees.behaviours.Dummy('leaf_3')
    d4 = py_trees.behaviours.Dummy('leaf_4')
    d5 = py_trees.behaviours.Dummy('leaf_5')
    d6 = py_trees.behaviours.Dummy('leaf_6')
    d7 = py_trees.behaviours.Dummy('leaf_7')
    d8 = py_trees.behaviours.Dummy('leaf_8')

    seq2 = py_trees.composites.Sequence('seq2')
    seq3 = py_trees.composites.Sequence('seq3')
    
    d9 = py_trees.behaviours.Dummy('leaf_9')
    d10 = py_trees.behaviours.Dummy('leaf_10')
    d11 = py_trees.behaviours.Dummy('leaf_11')
    d12 = py_trees.behaviours.Dummy('leaf_12')
    d13 = py_trees.behaviours.Dummy('leaf_13')
    d14 = py_trees.behaviours.Dummy('leaf_14')
    d15 = py_trees.behaviours.Dummy('leaf_15')
    d16 = py_trees.behaviours.Dummy('leaf_16')

    seq1.add_children([sel1, sel2])
    sel1.add_children([d1, d2, d3, d4, d5, d6, d7, d8])
    sel2.add_children([seq2, seq3])
    seq2.add_children([d9, d10, d11, d12])
    seq3.add_children([d13, d14, d15, d16])
    if print_pic:
        py_trees.display.render_dot_tree(seq1, target_directory = '../pictures')#works
    return seq1
