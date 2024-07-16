import py_trees
import math
import operator


class read_map(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_map, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('valid_position'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('map_exists'), access = py_trees.common.Access.WRITE)
        self.success_read = False

    def update(self):
        if self.environment.read_map_function__condition(self):
            self.blackboard.map_exists = self.environment.read_map_function__0(self)
        if self.blackboard.map_exists:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of read_map: ' + str(return_status) + '\n')
        return return_status
