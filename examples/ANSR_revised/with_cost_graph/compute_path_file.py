import py_trees
import math
import operator
from ebt.bt.advanced_a_star import a_star

class compute_path(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, convert_bt_to_a_star):
        super(compute_path, self).__init__(name)
        self.name = name
        self.environment = environment
        self.convert_bt_to_a_star = convert_bt_to_a_star
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cost_graph'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goals'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal_index'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment_sent'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.path = a_star(
            self.blackboard.cost_graph,
            self.convert_bt_to_a_star(self.blackboard.map_info, self.blackboard.position),
            self.convert_bt_to_a_star(self.blackboard.map_info, self.blackboard.goals[self.blackboard.goal_index])
        )
        if len(self.blackboard.path) > 0:
            self.blackboard.path.pop(0)
        self.blackboard.path_segment = (0, 0)
        self.blackboard.path_segment_sent = False
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('compute_path: ' + str(return_status) + '\n')
        return return_status
