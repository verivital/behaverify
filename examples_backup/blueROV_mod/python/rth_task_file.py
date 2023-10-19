import py_trees
import math
import operator
import random
import serene_safe_assignment


class rth_task(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(rth_task, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cm_hsd_input'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.cm_hsd_input = serene_safe_assignment.cm_hsd_input('cm_rth_task')
        return_status = py_trees.common.Status.RUNNING
        return return_status
