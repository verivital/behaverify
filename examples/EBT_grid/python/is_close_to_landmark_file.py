import py_trees
import math
import operator


class is_close_to_landmark(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(is_close_to_landmark, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_landmark_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_landmark_y'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (((self.blackboard.drone_x == self.blackboard.current_landmark_x()) and (self.blackboard.drone_y == self.blackboard.current_landmark_y()))) else (py_trees.common.Status.FAILURE))
        return return_status
