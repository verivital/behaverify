import py_trees
import math
import operator


class compute_path_segment(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(compute_path_segment, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_segment_sent'), access = py_trees.common.Access.WRITE)

    def update(self):
        index = self.blackboard.path_segment[1]
        altitude = self.blackboard.path[index][2]
        while index < len(self.blackboard.path) and altitude == self.blackboard.path[index][2]:
            index = index + 1
        self.blackboard.path_segment = (self.blackboard.path_segment[1], index)
        self.blackboard.path_segment_sent = False
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('compute_path_segment: ' + str(return_status) + '\n')
        return return_status
