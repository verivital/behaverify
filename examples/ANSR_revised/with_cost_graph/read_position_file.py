import py_trees
import math
import operator


class read_position(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, convert_odometry_to_bt):
        super(read_position, self).__init__(name)
        self.name = name
        self.convert_odometry_to_bt = convert_odometry_to_bt
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = 'map_info', access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.WRITE)
        self.read_success = False

    def update(self):
        if self.environment.read_position_ready():
            self.read_success = True
            self.blackboard.position = self.convert_odometry_to_bt(self.blackboard.map_info, self.environment.read_position())
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('drone: ' + str(self.blackboard.position) + '\n')
        else:
            self.read_success = False
        if self.read_success:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('read_position: ' + str(return_status) + '\n')
        return return_status
