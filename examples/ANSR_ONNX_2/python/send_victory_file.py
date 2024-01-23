import py_trees
import math
import operator


class send_victory(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(send_victory, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('victory'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.victory = self.blackboard.serene_randomizer.r_5(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
