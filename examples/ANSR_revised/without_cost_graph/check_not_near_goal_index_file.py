import py_trees
import math
import operator


class check_not_near_goal_index(py_trees.behaviour.Behaviour):
    def __init__(self, name, function_near_goal):
        super(check_not_near_goal_index, self).__init__(name)
        self.name = name
        self.function_near_goal = function_near_goal
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('goals'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal_index'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (not (self.function_near_goal(self.blackboard.position, self.blackboard.goals[self.blackboard.goal_index]))) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('check_not_near_goal_index: ' + str(return_status) + '\n')
        return return_status
