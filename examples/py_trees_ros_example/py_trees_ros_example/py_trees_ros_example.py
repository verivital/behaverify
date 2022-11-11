import py_trees
import py_trees_ros
import custom_node


def create_root():
    root = py_trees.composites.Selector('root')
    sequence_sif = py_trees.meta.success_is_failure(py_trees.composites.Sequence)('seq_sif')
    parallel = py_trees.composites.Parallel('par')
    battery_node = py_trees_ros.battery.ToBlackboard('battery_node')
    check_data = py_trees_ros.subscribers.CheckData()
    event_to_blackboard = py_trees_ros.subscribers.EventToBlackboard()
    to_blackboard = py_trees_ros.subscribers.ToBlackboard()
    wait_for_data = py_trees_ros.subscribers.WaitForData()
    my_custom_node = custom_node.ToBlackboard('custom')

    root.add_children([sequence_sif, parallel])
    sequence_sif.add_children([battery_node, check_data, event_to_blackboard])
    parallel.add_children([to_blackboard, wait_for_data, my_custom_node])

    return root
