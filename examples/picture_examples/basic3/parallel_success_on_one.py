import py_trees


def create_root(print_pic=False):
    p_one = py_trees.common.ParallelPolicy.SuccessOnOne();
    parallel = py_trees.composites.Parallel('parallel', p_one)
    if print_pic:
        py_trees.display.render_dot_tree(parallel, target_directory = '../pictures')#works
    return parallel

create_root(True)
