import my_check_file
import my_action_1_file
import my_action_2_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'a', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'b', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'c', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'd', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'e', access = py_trees.common.Access.WRITE)
    blackboard_reader.a = [None] * 3
    __temp_var__ = serene_safe_assignment.a([(0, (0 * 2)), (1, (1 * 2)), (2, (2 * 2))])
    for (index, val) in __temp_var__:
        blackboard_reader.a[index] = val
    blackboard_reader.b = [None] * 3
    __temp_var__ = serene_safe_assignment.b([(0, 0), (1, 4), (2, blackboard_reader.a[2])])
    for (index, val) in __temp_var__:
        blackboard_reader.b[index] = val
    blackboard_reader.c = [None] * 3
    __temp_var__ = serene_safe_assignment.c([(0, 0), (1, 4), (2, blackboard_reader.a[2])])
    for (index, val) in __temp_var__:
        blackboard_reader.c[index] = val
    blackboard_reader.d = [None] * 3


    def d(index):
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing d: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing d: ' + str(index))
        if index == 0:
            return (
                (blackboard_reader.a[0] + blackboard_reader.b[(0 + 1)])
                if (0 < 2) else
                (
                (blackboard_reader.a[0] + blackboard_reader.b[0])
            ))
        elif index == 1:
            return (
                (blackboard_reader.a[1] + blackboard_reader.b[(1 + 1)])
                if (1 < 2) else
                (
                (blackboard_reader.a[1] + blackboard_reader.b[0])
            ))
        elif index == 2:
            return (
                (blackboard_reader.a[2] + blackboard_reader.b[(2 + 1)])
                if (2 < 2) else
                (
                (blackboard_reader.a[2] + blackboard_reader.b[0])
            ))
        raise Exception('Reached unreachable state when accessing d: ' + str(index))

    blackboard_reader.d = d
    blackboard_reader.e = [None] * 3
    __temp_var__ = serene_safe_assignment.e([(0, (blackboard_reader.d(0) > 10)), (1, (blackboard_reader.d(1) > 10)), (2, (blackboard_reader.d(2) > 10))])
    for (index, val) in __temp_var__:
        blackboard_reader.e[index] = val
    return blackboard_reader


def create_tree(environment):
    my_check = my_check_file.my_check('my_check')
    my_action_1 = my_action_1_file.my_action_1('my_action_1', environment)
    idk2 = py_trees.composites.Sequence(name = 'idk2', memory = False, children = [my_check, my_action_1])
    my_action_2 = my_action_2_file.my_action_2('my_action_2', environment)
    idk = py_trees.composites.Selector(name = 'idk', memory = False, children = [idk2, my_action_2])
    return idk
