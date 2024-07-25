import py_trees
import math
import operator


class path_segment_exists_check(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(path_segment_exists_check, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.blackboard.path_segment[1] > self.blackboard.path_segment[0]) else (py_trees.common.Status.FAILURE))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('path_segment_exists_check: ' + str(return_status) + '\n')
        return return_status
