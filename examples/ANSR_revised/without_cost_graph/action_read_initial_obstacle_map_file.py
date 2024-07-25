import py_trees
import math
import operator


class action_read_initial_obstacle_map(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, function_reformat_obstacle_map):
        super(action_read_initial_obstacle_map, self).__init__(name)
        self.name = name
        self.function_reformat_obstacle_map = function_reformat_obstacle_map
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('obstacle_map'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.read_obstacle_map_ready():
            (obstacle_map, self.blackboard.map_info) = self.environment.read_obstacle_map()
            self.blackboard.obstacle_map = self.function_reformat_obstacle_map(self.blackboard.map_info, obstacle_map)
        if self.blackboard.obstacle_map is not None:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('action_read_initial_obstacle_map: ' + str(return_status) + '\n')
        return return_status
