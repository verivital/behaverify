import py_trees
import math
import operator


class get_next_landmark(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(get_next_landmark, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('landmark_index'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.landmark_index = self.blackboard.serene_randomizer.r_0(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
