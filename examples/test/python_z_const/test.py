from pathlib import Path
import py_trees
import test_file
import onnxruntime


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'x', access = py_trees.common.Access.WRITE)
    blackboard_reader.x = None
    blackboard_reader.register_key(key = 'y', access = py_trees.common.Access.WRITE)
    blackboard_reader.y = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.x = (-5)
    blackboard_reader.y = (-10)
    return


def create_tree(environment):
    test = test_file.test('test', environment)
    return test
