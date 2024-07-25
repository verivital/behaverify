import py_trees
import math
import operator


class action_read_goals(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, function_convert_planner_to_bt):
        super(action_read_goals, self).__init__(name)
        self.name = name
        self.environment = environment
        self.function_convert_planner_to_bt = function_convert_planner_to_bt
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('goal_index'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = 'map_info', access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goals'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment_sent'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.read_goals_ready():
            (new_goals_index, new_goals) = self.environment.read_goals()
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('new_goals (index, len): ' + str((new_goals_index, len(new_goals))) + '\n')
            if new_goals_index < 0:
                new_goals_index = len(self.blackboard.goals) + new_goals_index
            new_goals_index = max(new_goals_index, self.blackboard.goal_index)
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('adjusted index: ' + str(new_goals_index) + '\n')
            if new_goals_index == self.blackboard.goal_index:
                self.blackboard.path = []
                self.blackboard.path_segment = 0
                self.blackboard.path_segment_sent = False
            self.blackboard.goals = self.blackboard.goals[0:new_goals_index] + [self.function_convert_planner_to_bt(self.blackboard.map_info, goal) for goal in new_goals]
        return_status = py_trees.common.Status.SUCCESS if self.blackboard.goal_index < len(self.blackboard.goals) else py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('action_read_goals: ' + str(return_status) + '\n')
        return return_status
