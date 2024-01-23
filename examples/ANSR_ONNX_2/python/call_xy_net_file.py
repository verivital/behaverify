import py_trees
import math
import operator


class call_xy_net(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(call_xy_net, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('x_net'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('y_net'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dir_int'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dest_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('dest_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.dest_x = (
            self.blackboard.serene_randomizer.r_0(self)
            if (self.blackboard.x_net(0) == 0) else
            (
            self.blackboard.serene_randomizer.r_1(self)
        ))
        self.blackboard.dest_y = self.blackboard.serene_randomizer.r_2(self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
