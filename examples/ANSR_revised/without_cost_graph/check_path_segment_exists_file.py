import py_trees
import math
import operator


class check_path_segment_exists(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(check_path_segment_exists, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.blackboard.path_segment > 0) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('check_path_segment_exists: ' + str(return_status) + '\n')
        return return_status
