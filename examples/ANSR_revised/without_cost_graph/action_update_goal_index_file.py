import py_trees
import math
import operator


class action_update_goal_index(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(action_update_goal_index, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('goals'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal_index'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment_sent'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.goal_index = (1 + self.blackboard.goal_index)
        self.blackboard.path_segment_sent = False
        self.blackboard.path = []
        self.blackboard.path_segment = 0
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('new goal: ' + str(self.blackboard.goals[self.blackboard.goal_index]) + '\n')
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('action_update_goal_index: ' + str(return_status) + '\n')
        return return_status
