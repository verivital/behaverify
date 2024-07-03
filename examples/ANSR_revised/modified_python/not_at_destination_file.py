import py_trees
import math
import operator


class not_at_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(not_at_destination, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_z'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_z'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (((self.blackboard.drone_x == self.blackboard.destination_x) and (self.blackboard.drone_y == self.blackboard.destination_y) and (self.blackboard.drone_z == self.blackboard.destination_z))) else (py_trees.common.Status.FAILURE))
        return return_status
