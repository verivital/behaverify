import py_trees
import math
import operator


class send_next_goal_request(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(send_next_goal_request, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('goal_requested'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.goal_requested = True
        self.environment.send_next_goal_request_function__0(self)
        return_status = py_trees.common.Status.FAILURE
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('STATUS of send_next_goal_request: ' + str(return_status) + '\n')
        return return_status
