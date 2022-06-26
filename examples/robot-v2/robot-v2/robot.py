import py_trees
import additional_leafs
import queue

def create_root(to_create = 1):

    to_create = max(1, int(to_create))

    children = []

    for i in range(to_create):
        local_root = py_trees.composites.Selector('sel' + str(i))
        check = additional_leafs.Non_Blocking_Leaf('safety_check' + str(i))
        safety = py_trees.behaviours.Success('backup' + str(i))
        local_root.add_children([check, safety])
        children.append(local_root)

    root = py_trees.composites.Sequence('rootSeq')
    root.add_children(children)
    return root
