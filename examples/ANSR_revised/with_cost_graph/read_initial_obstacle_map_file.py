import py_trees
import math
import operator


class read_initial_obstacle_map(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, reformat_obstacle_map_function, create_cost_graph_function):
        super(read_initial_obstacle_map, self).__init__(name)
        self.name = name
        self.reformat_obstacle_map_function = reformat_obstacle_map_function
        self.create_cost_graph_function = create_cost_graph_function
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('obstacle_map'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('cost_graph'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.read_obstacle_map_ready():
            (obstacle_map, self.blackboard.map_info) = self.environment.read_obstacle_map()
            self.blackboard.obstacle_map = self.reformat_obstacle_map_function(self.blackboard.map_info, obstacle_map)
            self.blackboard.cost_graph = self.create_cost_graph_function(self.blackboard.map_info, self.blackboard.obstacle_map)
        if self.blackboard.obstacle_map is not None:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('read_initial_obstacle_map: ' + str(return_status) + '\n')
        return return_status