import py_trees
import math
import operator


class update_direction(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(update_direction, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dir'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.dir = (
            self.blackboard.serene_randomizer.r_6(self)
            if (self.blackboard.cur_y == 10) else
            (
                self.blackboard.serene_randomizer.r_7(self)
                if (self.blackboard.cur_y == 0) else
                (
                self.blackboard.serene_randomizer.r_8(self)
        )))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
