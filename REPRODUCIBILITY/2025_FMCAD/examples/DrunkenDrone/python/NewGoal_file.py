import py_trees
import math
import operator


class NewGoal(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(NewGoal, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('new'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('act'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.new = True
        self.blackboard.act = 'XX'
        return_status = py_trees.common.Status.RUNNING
        return return_status
