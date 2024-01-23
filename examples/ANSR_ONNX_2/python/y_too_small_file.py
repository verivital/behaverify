import py_trees
import math
import operator


class y_too_small(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(y_too_small, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dest_y'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.cur_y < self.blackboard.dest_y)) else (py_trees.common.Status.FAILURE))
        return return_status
