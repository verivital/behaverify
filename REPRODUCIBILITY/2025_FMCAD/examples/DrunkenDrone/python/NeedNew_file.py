import py_trees
import math
import operator


class NeedNew(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(NeedNew, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x_d'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('y_d'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('act'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.environment.NeedNew(self)) else (py_trees.common.Status.FAILURE))
        return return_status
