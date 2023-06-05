import py_trees
import useful_array
import useful_array_environment

blackboard_reader = useful_array.create_blackboard()
environment = useful_array_environment.useful_array_environment(blackboard_reader)
root = useful_array.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)
visualizer = py_trees.visitors.DisplaySnapshotVisitor()
tree.add_visitor(visualizer)


def full_tick():
    tree.tick_once()
    environment.execute_delayed_action_queue()
    environment.between_tick_environment_update()
    return


def print_blackboard():
    print('blackboard:')
    return


def print_environment():
    print('environment:')
    print('  test: ' + str(environment.test))
    return


for count in range(100):
    print('------------------------')
    print('iteration: ' + str(count))
    if environment.check_tick_condition():
        full_tick()
    else:
        print('after ' + str(count) + ' ticks, tick_condition no longer holds. exiting')
        break
    print_blackboard()
    print_environment()
