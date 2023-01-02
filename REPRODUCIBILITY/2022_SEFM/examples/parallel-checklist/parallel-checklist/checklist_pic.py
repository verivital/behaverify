import py_trees
import additional_leafs
import queue

def create_root(to_create = 1, print_pic = False):

    to_create = max(1, int(to_create))
    p_all_f=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False)

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
    if print_pic:
        py_trees.display.render_dot_tree(child1, target_directory = '../pictures/'+str(to_create))#works
        
    return child1

#create_root(1, True)
#create_root(5, True)
#create_root(10, True)
#create_root(50, True)
#create_root(18, True)
#create_root(19, True)
#create_root(20, True)

# create_root(14, True)
# create_root(15, True)
# create_root(16, True)
# create_root(17, True)
create_root(30, True)
