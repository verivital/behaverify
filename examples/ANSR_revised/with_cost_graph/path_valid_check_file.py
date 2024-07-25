import py_trees
import math
import operator


class path_valid_check(py_trees.behaviour.Behaviour):
    def __init__(self, name, obstacle_at_point_function):
        super(path_valid_check, self).__init__(name)
        self.name = name
        self.obstacle_at_point_function = obstacle_at_point_function
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('map_info'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('obstacle_map'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = (
            (py_trees.common.Status.SUCCESS)
            if (not (any(self.obstacle_at_point_function(self.blackboard.map_info, self.blackboard.obstacle_map, point) for point in self.blackboard.path))) and len(self.blackboard.path) > 0 else
            (py_trees.common.Status.FAILURE)
        )
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('path_valid_check: ' + str(return_status) + '\n')
        return return_status
