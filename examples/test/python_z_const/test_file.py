import py_trees
import math
import operator


class test(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(test, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.x = (
            0
            if (self.blackboard.y == 0) else
            (
                self.blackboard.serene_randomizer.r_0(self)
        ))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
