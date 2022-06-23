import py_trees
import queue


def create_root(print_pic, num_selector, num_sequence):
    num_selector = max(0, num_selector)
    num_sequence = max(0, num_sequence)
    file_name = "sel" + str(num_selector) + "-seq" + str(num_sequence)
    need_children = queue.Queue(num_selector + num_sequence)
    if num_selector + num_sequence == 0 :
        root = py_trees.behaviours.Dummy('root')
    else:
        if num_selector > num_sequence:
            root = py_trees.composites.Selector('root')
            num_selector = num_selector - 1
        else:
            root = py_trees.composites.Sequence('root')
            num_sequence = num_sequence - 1
        need_children.put(root)
    leaf_count = 0
    while num_selector + num_sequence > 0:
        if num_selector > num_sequence:
            child1 = py_trees.composites.Selector('sel' + str(num_selector))
            num_selector = num_selector - 1
        else:
            child1 = py_trees.composites.Sequence('seq' + str(num_selector))
            num_sequence = num_sequence - 1
        
        need_children.put(child1)
        if num_selector + num_sequence == 0:
            child2 = py_trees.behaviours.Dummy('leaf' + str(leaf_count))
            leaf_count = leaf_count + 1
        else:
            if num_selector > num_sequence:
                child2 = py_trees.composites.Selector('sel' + str(num_selector))
                num_selector = num_selector - 1
            else:
                child2 = py_trees.composites.Sequence('seq' + str(num_selector))
                num_sequence = num_sequence - 1
            need_children.put(child2)
        parent = need_children.get()
        parent.add_children([child1, child2])
    while not need_children.empty():
        parent = need_children.get()
        child1 = py_trees.behaviours.Dummy('leaf' + str(leaf_count))
        leaf_count = leaf_count + 1
        child2 = py_trees.behaviours.Dummy('leaf' + str(leaf_count))
        leaf_count = leaf_count + 1
        parent.add_children([child1, child2])
        
    if print_pic:
        py_trees.display.render_dot_tree(root, target_directory = '../pictures/'+file_name)#works
    return root
    

