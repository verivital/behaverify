import abs
import abs_environment

blackboard_reader = abs.create_blackboard()
environment = abs_environment.abs_environment(blackboard_reader)
tree = abs.create_tree(environment)


def full_tick():
    tree.tick_once()
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
    print_blackboard()
    print_environment()
    if environment.check_tick_condition():
        full_tick()
    else:
        break
