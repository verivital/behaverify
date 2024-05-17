import py_trees
import math
import operator


class read_position(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_position, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('cell_changed_var'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.function_get_position__condition(self):
            self.blackboard.cell_changed_var = self.environment.function_get_position__0(self)
            self.blackboard.drone_x = self.environment.function_get_position__1(self)
            self.blackboard.drone_y = self.environment.function_get_position__2(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
