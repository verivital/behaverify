import py_trees
import math
import operator


class read_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_destination, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('destination_y'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('destination_z'), access = py_trees.common.Access.WRITE)
        self.success_read = False

    def update(self):
        if self.environment.read_destination_function__condition(self):
            self.success_read = True
            self.blackboard.destination_x = self.environment.read_destination_function__0(self)
            self.blackboard.destination_y = self.environment.read_destination_function__1(self)
            self.blackboard.destination_z = self.environment.read_destination_function__2(self)
        else:
            self.success_read = False
        if self.success_read:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
