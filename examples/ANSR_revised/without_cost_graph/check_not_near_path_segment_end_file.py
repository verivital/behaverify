import py_trees
import math
import operator


class check_not_near_path_segment_end(py_trees.behaviour.Behaviour):
    def __init__(self, name, function_near_path_segment_end):
        super(check_not_near_path_segment_end, self).__init__(name)
        self.name = name
        self.function_near_path_segment_end = function_near_path_segment_end
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (not (self.function_near_path_segment_end(self.blackboard.position, self.blackboard.path[self.blackboard.path_segment - 1]))) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('check_not_near_path_segment_end: ' + str(return_status) + '\n')
        return return_status
