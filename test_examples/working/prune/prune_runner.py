import py_trees
import prune
import prune_environment

blackboard_reader = prune.create_blackboard()
environment = prune_environment.prune_environment(blackboard_reader)
root = prune.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)
visualizer = py_trees.visitors.DisplaySnapshotVisitor()
tree.add_visitor(visualizer)


def full_tick():
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.between_tick_environment_update()
    return


def print_blackboard():
    print('blackboard:')
    print('  test: ' + str(blackboard_reader.test))
    return


def print_environment():
    print('environment:')
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
