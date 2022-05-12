import py_trees
import math

def node_return(mode, depth, count):
    if mode == 0:
        return py_trees.composites.Selector('node'+str(count))
    elif mode == 1:
        return py_trees.composites.Parallel('node'+str(count), py_trees.common.ParallelPolicy.SuccessOnAll())
    elif mode == 2:
        return py_trees.composites.Parallel('node'+str(count), py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = False))
    elif mode == 3:
        if (count % 2) == 0:
            return py_trees.composites.Selector('node'+str(count))
        else:
            return py_trees.composites.Parallel('node'+str(count), py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = False))
    elif mode == 4:
        if (count % 2) == 0:
            return py_trees.composites.Selector('node'+str(count))
        else:
            return py_trees.composites.Parallel('node'+str(count), py_trees.common.ParallelPolicy.SuccessOnAll())
    elif mode == 5:
        if (depth % 2) == 0:
            return py_trees.composites.Selector('node'+str(count))
        else:
            return py_trees.composites.Parallel('node'+str(count), py_trees.common.ParallelPolicy.SuccessOnAll())
    elif mode == 6:
        if (depth % 2) == 0:
            return py_trees.composites.Selector('node'+str(count))
        else:
            return py_trees.composites.Parallel('node'+str(count), py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = False))

def full_binary_mode(max_depth, mode=0, count=0):
    count=count+1
    if max_depth == 0:
        return (py_trees.behaviours.Dummy(), count)
    else:
        this_node = node_return(mode, max_depth, count)
        (to_add1, count) = full_binary_mode(max_depth-1, mode, count)
        (to_add2, count) = full_binary_mode(max_depth-1, mode, count)
        this_node.add_children([to_add1, to_add2])
        return (this_node, count)

def wide_mode(num_nodes, mode=0):
    if mode == 0:
        root_node=py_trees.composites.Selector('root')
    elif mode == 1:
        root_node=py_trees.composites.Parallel('root', py_trees.common.ParallelPolicy.SuccessOnAll())
    elif mode == 2:
        root_node=py_trees.composites.Parallel('root', py_trees.common.ParallelPolicy.SuccessOnAll(synchronise = False))
    children=[]
    for i in range(num_nodes):
        children.append(py_trees.behaviours.Dummy())
    root_node.add_children(children)
    
    return root_node



def create_root(num_nodes, mode, binary):
    if binary:
        return full_binary_mode(num_nodes, mode)[0]
    else:
        return wide_mode(num_nodes, mode)
