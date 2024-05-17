import py_trees
import math
import operator


class new_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(new_destination, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('destination_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.function_get_new_destination__condition(self):
            self.blackboard.destination_x = self.environment.function_get_new_destination__0(self)
            self.blackboard.destination_y = self.environment.function_get_new_destination__1(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
