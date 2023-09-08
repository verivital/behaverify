import addition_more_file
import move_index_file
import action_one_file
import action_two_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'foo', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'trom', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'index_var', access = py_trees.common.Access.WRITE)
    blackboard_reader.foo = [None] * 3
    __temp_var__ = serene_safe_assignment.foo([(0, 0), (1, 1), (2, 2)])
    for (index, val) in __temp_var__:
        blackboard_reader.foo[index] = val
    blackboard_reader.trom = [None] * 2


    def trom(index):
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing trom: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise Exception('Index out of bounds when accessing trom: ' + str(index))
        if index == 0:
            return (blackboard_reader.foo[0] + blackboard_reader.foo[1] + blackboard_reader.foo[2])
        elif index == 1:
            return (blackboard_reader.foo[0] * blackboard_reader.foo[1] * blackboard_reader.foo[2])
        raise Exception('Reached unreachable state when accessing trom: ' + str(index))

    blackboard_reader.trom = trom
    blackboard_reader.index_var = serene_safe_assignment.index_var(random.choice([0, 1, 2]))
    return blackboard_reader


def create_tree(environment):
    move_index = move_index_file.move_index('move_index', environment)
    addition_more = addition_more_file.addition_more('addition_more')
    action_one = action_one_file.action_one('action_one', environment)
    try_option = py_trees.composites.Sequence(name = 'try_option', memory = False, children = [addition_more, action_one])
    action_two = action_two_file.action_two('action_two', environment)
    controller = py_trees.composites.Selector(name = 'controller', memory = False, children = [move_index, try_option, action_two])
    return controller
