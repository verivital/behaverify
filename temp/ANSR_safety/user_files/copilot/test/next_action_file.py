import py_trees
import math
import operator


class next_action(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(next_action, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('fake_network'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('destination_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cell_changed_var'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.cell_changed_var = False
        self.blackboard.current_action = self.blackboard.fake_network()
        return_status = py_trees.common.Status.SUCCESS
        return return_status
