import py_trees
import math
import operator


class read_goal(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_goal, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('goal_requested'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('valid_goal'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.read_goal_function__condition(self):
            __temp_var__ = self.environment.read_goal_function__0(self)
            for (index, val) in __temp_var__:
                self.blackboard.goal[index] = val
            self.blackboard.goal_requested = self.environment.read_goal_function__1(self)
            self.blackboard.valid_goal = self.environment.read_goal_function__2(self)
        if self.blackboard.valid_goal:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of read_goal: ' + str(return_status) + '\n')
        return return_status
