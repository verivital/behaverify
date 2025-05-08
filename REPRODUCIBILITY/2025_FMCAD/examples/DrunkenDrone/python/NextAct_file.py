import py_trees
import math
import operator


class NextAct(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(NextAct, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('new'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('act'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.new = False
        self.blackboard.act = self.blackboard.serene_randomizer.r_0(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
