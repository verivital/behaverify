import py_trees
import additional_leafs
import queue

def create_root(to_create = 1):
    p_all_f=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False)

    to_create = max(1, int(to_create))

    children = queue.Queue(0)

    for i in range(to_create):
        local_root = py_trees.composites.Selector('sel' + str(i))
        check = additional_leafs.Non_Blocking_Leaf('safety_check' + str(i))
        safety = py_trees.behaviours.Success('backup' + str(i))
        local_root.add_children([check, safety])
        children.put(local_root)

    count = 0
    while not children.empty():
        child1 = children.get()

        if children.empty():
            break
        child2 = children.get()

        new_parent = py_trees.composites.Parallel('linkPar' + str(count), p_all_f)
        count = count + 1
        new_parent.add_children([child1, child2])
        children.put(new_parent)
    return child1
