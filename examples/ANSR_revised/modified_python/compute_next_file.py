import py_trees
import math
import operator


class compute_next(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(compute_next, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_z'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x_delta'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y_delta'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('next_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('next_y'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('next_z'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('valid_destination'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.compute_path_function__condition(self):
            self.blackboard.valid_destination = True
            self.blackboard.next_x = self.environment.compute_path_function__0(self)
            self.blackboard.next_y = self.environment.compute_path_function__1(self)
            self.blackboard.next_z = self.environment.compute_path_function__2(self)
        else:
            self.blackboard.valid_destination = False
        if self.blackboard.valid_destination:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        return return_status
