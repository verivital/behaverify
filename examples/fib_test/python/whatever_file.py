import py_trees
import math
import operator


class whatever(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(whatever, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('fib_val'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.fib_val(1) > self.blackboard.fib_val(0))) else (py_trees.common.Status.FAILURE))
        return return_status
