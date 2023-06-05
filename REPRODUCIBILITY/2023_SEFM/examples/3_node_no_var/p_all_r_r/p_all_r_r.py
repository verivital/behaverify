import f_file
import r_file
import s_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    return blackboard_reader


def create_tree(environment):
    r = r_file.r('r', environment)
    r_1 = r_file.r('r_1', environment)
    p_all = py_trees.composites.Parallel(name = 'p_all', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [r, r_1])
    return p_all
