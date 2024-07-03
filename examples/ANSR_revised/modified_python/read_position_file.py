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
        self.blackboard.register_key(key = ('previous_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('previous_y'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('previous_z'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_z'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_x_delta'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_y_delta'), access = py_trees.common.Access.WRITE)
        self.success_read = False

    def update(self):
        self.blackboard.previous_x = self.blackboard.drone_x
        self.blackboard.previous_y = self.blackboard.drone_y
        self.blackboard.previous_z = self.blackboard.drone_z
        if self.environment.read_position_function__condition(self):
            self.success_read = True
            self.blackboard.drone_x = self.environment.read_position_function__0(self)
            self.blackboard.drone_y = self.environment.read_position_function__1(self)
            self.blackboard.drone_z = self.environment.read_position_function__2(self)
            self.blackboard.drone_x_delta = self.environment.read_position_function__3(self)
            self.blackboard.drone_y_delta = self.environment.read_position_function__4(self)
        else:
            self.success_read = False
        return_status = py_trees.common.Status.SUCCESS
        return return_status
