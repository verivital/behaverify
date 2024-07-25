import py_trees
import math
import operator
from functools import partial
from ebt.bt.specialized_a_star import a_star

class action_compute_path(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, function_convert_bt_to_a_star, function_obstacle_at_point, function_cost):
        super(action_compute_path, self).__init__(name)
        self.name = name
        self.environment = environment
        self.function_convert_bt_to_a_star = function_convert_bt_to_a_star
        self.function_obstacle_at_point = function_obstacle_at_point
        self.function_cost = function_cost
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('flight_heights'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goals'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal_index'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('obstacle_map'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment_sent'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.path = a_star(
            partial(self.function_obstacle_at_point, self.blackboard.map_info, self.blackboard.obstacle_map),
            self.function_cost,
            self.blackboard.flight_heights,
            self.function_convert_bt_to_a_star(self.blackboard.map_info, self.blackboard.position),
            self.function_convert_bt_to_a_star(self.blackboard.map_info, self.blackboard.goals[self.blackboard.goal_index])
        )
        if len(self.blackboard.path) > 0:
            self.blackboard.path.pop(0)
        self.blackboard.path_segment = 0
        self.blackboard.path_segment_sent = False
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('action_compute_path: ' + str(return_status) + '\n')
        return return_status
