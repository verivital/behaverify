import py_trees
import seq_f_r
import seq_f_r_environment

blackboard_reader = seq_f_r.create_blackboard()
environment = seq_f_r_environment.seq_f_r_environment(blackboard_reader)
root = seq_f_r.create_tree(environment)
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
    return


def print_environment():
    print('environment:')
    return


for count in range(10):
    print('------------------------')
    print('iteration: ' + str(count))
    if environment.check_tick_condition():
        full_tick()
    else:
        print('after ' + str(count) + ' ticks, tick_condition no longer holds. exiting')
        break
    print_blackboard()
    print_environment()
