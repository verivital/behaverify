import py_trees
import math
import operator


class valid_destination_check(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(valid_destination_check, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('valid_destination'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.blackboard.valid_destination) else (py_trees.common.Status.FAILURE))
        return return_status
