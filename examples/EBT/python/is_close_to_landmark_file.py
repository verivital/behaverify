import py_trees
import math
import operator


class is_close_to_landmark(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(is_close_to_landmark, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('current_landmark'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_location'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (((self.blackboard.drone_location[0] == self.blackboard.current_landmark(0)) and (self.blackboard.drone_location[1] == self.blackboard.current_landmark(1)))) else (py_trees.common.Status.FAILURE))
        return return_status
