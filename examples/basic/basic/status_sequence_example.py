import py_trees


def create_root():
    return py_trees.behaviours.StatusSequence('default1', [py_trees.common.Status.SUCCESS, py_trees.common.Status.SUCCESS, py_trees.common.Status.FAILURE, py_trees.common.Status.RUNNING], None)




