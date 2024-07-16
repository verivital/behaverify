import py_trees
import math
import operator


class not_at_goal(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(not_at_goal, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (not (((self.blackboard.position[0] == self.blackboard.goal[0]) and (self.blackboard.position[1] == self.blackboard.goal[1]) and (self.blackboard.position[2] == self.blackboard.goal[2])))) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of not_at_goal: ' + str(return_status) + '\n')
        return return_status
