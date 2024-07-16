import py_trees
import math
import operator


class valid_goal_check(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(valid_goal_check, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('valid_goal'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.blackboard.valid_goal) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of valid_goal: ' + str(return_status) + '\n')
        return return_status
