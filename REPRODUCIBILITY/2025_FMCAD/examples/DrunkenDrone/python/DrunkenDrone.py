from pathlib import Path
import py_trees
import NewGoal_file
import NextAct_file
import NeedNew_file
import onnxruntime


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'act', access = py_trees.common.Access.WRITE)
    blackboard_reader.act = None
    blackboard_reader.register_key(key = 'new', access = py_trees.common.Access.WRITE)
    blackboard_reader.new = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.act = 'XX'
    blackboard_reader.new = False
    return


def create_tree(environment):
    NeedNew = NeedNew_file.NeedNew('NeedNew', environment)
    NewGoal = NewGoal_file.NewGoal('NewGoal', environment)
    GoalSeq = py_trees.composites.Sequence(name = 'GoalSeq', memory = False, children = [NeedNew, NewGoal])
    NextAct = NextAct_file.NextAct('NextAct', environment)
    Drone = py_trees.composites.Selector(name = 'Drone', memory = False, children = [GoalSeq, NextAct])
    return Drone
