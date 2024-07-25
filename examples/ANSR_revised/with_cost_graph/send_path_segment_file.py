import py_trees
import math
import operator


class send_path_segment(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, convert_bt_to_waypoint):
        super(send_path_segment, self).__init__(name)
        self.name = name
        self.environment = environment
        self.convert_bt_to_waypoint = convert_bt_to_waypoint
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = 'map_info', access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path_segment'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path_segment_sent'), access = py_trees.common.Access.WRITE)

    def update(self):
        segment = self.blackboard.path[self.blackboard.path_segment[0] : self.blackboard.path_segment[1]]
        self.environment.send_path_segment_function(segment, self.convert_bt_to_waypoint, self.blackboard.map_info)
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('sent: path segment: ' + str(segment) + '\n')
        self.blackboard.path_segment_sent = True
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('send_path_segment: ' + str(return_status) + '\n')
        return return_status
