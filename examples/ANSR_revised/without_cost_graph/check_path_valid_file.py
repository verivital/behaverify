import py_trees
import math
import operator


class check_path_valid(py_trees.behaviour.Behaviour):
    def __init__(self, name, function_obstacle_at_point):
        super(check_path_valid, self).__init__(name)
        self.name = name
        self.function_obstacle_at_point = function_obstacle_at_point
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('obstacle_map'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = (
            (py_trees.common.Status.SUCCESS)
            if (not (any(self.function_obstacle_at_point(self.blackboard.map_info, self.blackboard.obstacle_map, point) for point in self.blackboard.path))) and len(self.blackboard.path) > 0 else
            (py_trees.common.Status.FAILURE)
        )
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('check_path_valid: ' + str(return_status) + '\n')
        return return_status
