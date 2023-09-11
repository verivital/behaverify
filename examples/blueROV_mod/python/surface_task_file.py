import py_trees
import math
import operator
import random
import serene_safe_assignment


class surface_task(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(surface_task, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cm_hsd_input'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('BLUEROV_SURFACED'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.cm_hsd_input = serene_safe_assignment.cm_hsd_input('cm_surface_task')
        self.blackboard.BLUEROV_SURFACED = serene_safe_assignment.BLUEROV_SURFACED(True)
        return_status = py_trees.common.Status.RUNNING
        return return_status
