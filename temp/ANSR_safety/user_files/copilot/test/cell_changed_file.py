import py_trees
import math
import operator


class cell_changed(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(cell_changed, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cell_changed_var'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.cell_changed_var or (self.blackboard.current_action == 'no_action'))) else (py_trees.common.Status.FAILURE))
        return return_status
