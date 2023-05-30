import array_test
import array_test_environment

blackboard_reader = array_test.create_blackboard()
environment = array_test_environment.array_test_environment(blackboard_reader)
tree = array_test.create_tree(environment)


def full_tick():
    tree.tick_once()
    environment.execute_delayed_action_queue()
    environment.between_tick_environment_update()
    return


def print_blackboard():
    print('blackboard:')
    print('  a: ' + str(blackboard_reader.a))
    print('  b: ' + str(blackboard_reader.b))
    print('  c: ' + str(blackboard_reader.c))
    print('  d: ' + str([blackboard_reader.d(x) for x in range(3)]))
    print('  e: ' + str(blackboard_reader.e))
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
