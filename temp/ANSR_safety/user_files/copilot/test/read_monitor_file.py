import py_trees
import math
import operator


class read_monitor(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_monitor, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_speed'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.function_get_velocity__condition(self):
            self.blackboard.drone_speed = self.environment.function_get_velocity__0(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
