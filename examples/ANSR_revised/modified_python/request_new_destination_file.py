import py_trees
import math
import operator


class request_new_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(request_new_destination, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)

    def update(self):
        self.environment.delay_this_action(self.environment.request_new_destination_function__0, self)
        return_status = py_trees.common.Status.FAILURE
        return return_status
