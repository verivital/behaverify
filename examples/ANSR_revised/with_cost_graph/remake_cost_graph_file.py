import py_trees
import math
import operator


class remake_cost_graph(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, create_cost_graph_function):
        super(remake_cost_graph, self).__init__(name)
        self.name = name
        self.create_cost_graph_function = create_cost_graph_function
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('obstacle_map'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cost_graph'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.cost_graph = self.create_cost_graph_function(self.blackboard.map_info, self.blackboard.obstacle_map)
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('remake_cost_graph: ' + str(return_status) + '\n')
        return return_status
