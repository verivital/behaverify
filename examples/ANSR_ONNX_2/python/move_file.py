import py_trees
import math
import operator


class move(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, delta_x, delta_y):
        self.delta_x = delta_x
        self.delta_y = delta_y
        super(move, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cur_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.cur_x = self.blackboard.serene_randomizer.r_3(self)
        self.blackboard.cur_y = self.blackboard.serene_randomizer.r_4(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
