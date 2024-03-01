import py_trees
import math
import operator


class compute_path(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(compute_path, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = py_trees.common.Status.SUCCESS
        return return_status
