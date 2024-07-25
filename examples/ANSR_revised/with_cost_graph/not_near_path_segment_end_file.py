import py_trees
import math
import operator


class not_near_path_segment_end(py_trees.behaviour.Behaviour):
    def __init__(self, name, near_path_segment_end_function):
        super(not_near_path_segment_end, self).__init__(name)
        self.name = name
        self.near_path_segment_end_function = near_path_segment_end_function
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (not (self.near_path_segment_end_function(self.blackboard.position, self.blackboard.path[self.blackboard.path_segment[1] - 1]))) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('not_near_path_segment_end: ' + str(return_status) + '\n')
        return return_status
