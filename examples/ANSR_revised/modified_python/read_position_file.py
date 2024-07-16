import py_trees
import math
import operator


class read_position(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_position, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('position'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('valid_position'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.read_position_function__condition(self):
            self.blackboard.valid_position = True
            __temp_var__ = self.environment.read_position_function__0(self)
            for (index, val) in __temp_var__:
                self.blackboard.position[index] = val
        else:
            self.blackboard.valid_position = False
        return_status = py_trees.common.Status.SUCCESS
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of read_position: ' + str(return_status) + '\n')
        return return_status
