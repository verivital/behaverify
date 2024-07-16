import py_trees
import math
import operator


class send_waypoint(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(send_waypoint, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('waypoint'), access = py_trees.common.Access.READ)

    def update(self):
        self.environment.send_waypoint_function__0(self)
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of send_waypoint: ' + str(return_status) + '\n')
        return return_status
