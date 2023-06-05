import py_trees
import frozen_lake_one_hole
import frozen_lake_one_hole_environment

blackboard_reader = frozen_lake_one_hole.create_blackboard()
environment = frozen_lake_one_hole_environment.frozen_lake_one_hole_environment(blackboard_reader)
root = frozen_lake_one_hole.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)
visualizer = py_trees.visitors.DisplaySnapshotVisitor(display_blackboard = True, display_activity_stream = True)
tree.add_visitor(visualizer)


def full_tick():
    # tree.tick_once()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.between_tick_environment_update()
    return


def print_blackboard():
    print('blackboard:')
    print('  tiles: ' + str(blackboard_reader.tiles))
    print('  action: ' + str(blackboard_reader.action))
    print('  sometimes: ' + str(blackboard_reader.sometimes))
    print('  strategy: ' + str(blackboard_reader.strategy))
    print('  subgoal: ' + str(blackboard_reader.subgoal))
    print('  x_subgoal: ' + str(blackboard_reader.x_subgoal()))
    print('  y_subgoal: ' + str(blackboard_reader.y_subgoal()))
    return


def print_environment():
    print('environment:')
    print('  start_loc: ' + str(environment.start_loc))
    print('  goal_loc: ' + str(environment.goal_loc))
    print('  loc: ' + str(environment.loc))
    print('  x_loc: ' + str(environment.x_loc()))
    print('  y_loc: ' + str(environment.y_loc()))
    print('  hole_loc: ' + str(environment.hole_loc))
    print('  falls_remaining: ' + str(environment.falls_remaining))
    return


# visualizer.run(tree)
for count in range(50):
    if environment.check_tick_condition():
        full_tick()
        # visualizer.finalise()
    else:
        print('after ' + str(count) + ' ticks, tick_condition no longer holds. exiting')
        break
    print('------------------------')
    print('iteration: ' + str(count))
    print_blackboard()
    print_environment()
