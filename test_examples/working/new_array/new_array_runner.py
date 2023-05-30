import new_array
import new_array_environment

blackboard_reader = new_array.create_blackboard()
environment = new_array_environment.new_array_environment(blackboard_reader)
tree = new_array.create_tree(environment)


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
    print_blackboard()
    print_environment()
    if environment.check_tick_condition():
        full_tick()
    else:
        break
