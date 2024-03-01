import py_trees
import math
import operator


class move_action(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(move_action, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_landmark_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_landmark_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.drone_x = (
            self.blackboard.drone_x
            if (self.blackboard.drone_x == self.blackboard.current_landmark_x()) else
            (
                min(19, (self.blackboard.drone_x + 1))
                if (self.blackboard.drone_x < self.blackboard.current_landmark_x()) else
                (
                max(0, (self.blackboard.drone_x - 1))
        )))
        self.blackboard.drone_y = (
            self.blackboard.drone_y
            if (self.blackboard.drone_y == self.blackboard.current_landmark_y()) else
            (
                min(19, (self.blackboard.drone_y + 1))
                if (self.blackboard.drone_y < self.blackboard.current_landmark_y()) else
                (
                max(0, (self.blackboard.drone_y - 1))
        )))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
