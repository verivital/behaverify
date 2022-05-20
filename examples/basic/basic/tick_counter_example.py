import py_trees


def create_root():
    return py_trees.behaviours.TickCounter(3, 'default1', py_trees.common.Status.SUCCESS)




