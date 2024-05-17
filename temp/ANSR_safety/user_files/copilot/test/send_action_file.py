import py_trees
import math
import operator


class send_action(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(send_action, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)

    def update(self):
        self.environment.function_send_action__0(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
