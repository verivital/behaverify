import py_trees
import math
import operator


class compute_waypoint(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(compute_waypoint, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('waypoint'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('valid_goal'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.compute_waypoint_function__condition(self):
            self.blackboard.valid_goal = True
            __temp_var__ = self.environment.compute_waypoint_function__0(self)
            for (index, val) in __temp_var__:
                self.blackboard.waypoint[index] = val
        else:
            self.blackboard.valid_goal = False
        if self.blackboard.valid_goal:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of compute_waypoint: ' + str(return_status) + '\n')
        return return_status
