import sel_f_f
import sel_f_f_environment
import py_trees

blackboard_reader = sel_f_f.create_blackboard()
environment = sel_f_f_environment.sel_f_f_environment(blackboard_reader)
tree = sel_f_f.create_tree(environment)
visualizer = py_trees.visitors.DisplaySnapshotVisitor()


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
    return


visualizer.run(tree)
for count in range(5):
    print('------------------------')
    print('iteration: ' + str(count))
    print_blackboard()
    print_environment()
    if environment.check_tick_condition():
        full_tick()
        visualizer.finalise()
    else:
        break
