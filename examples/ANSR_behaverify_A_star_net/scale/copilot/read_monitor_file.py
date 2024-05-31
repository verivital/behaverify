import py_trees
import math
import operator
import ctypes
import os
THIS_LOCATION = os.path.dirname(os.path.abspath(__file__))
collision_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'collision_monitor.so'))
collision_monitor_lib.user_interface.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
collision_monitor_lib.user_interface.restype = ctypes.c_int
loop_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'loop_monitor.so'))
loop_monitor_lib.user_interface.argtypes = [ctypes.c_int]
loop_monitor_lib.user_interface.restype = ctypes.c_int

ACTION_TO_INT = {
    'left' : 0,
    'right' : 1,
    'up' : 2,
    'down' : 3,
    'no_action' : 4
}

class read_monitor(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_monitor, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_speed'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('monitor_var'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.drone_speed = 2
        temp = collision_monitor_lib.user_interface(self.blackboard.drone_x, self.blackboard.drone_y, self.blackboard.delta_x(), self.blackboard.delta_y(), self.blackboard.drone_speed)
        self.blackboard.monitor_var = ('unsafe' if temp == 1 else 'unknown')
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        temp = loop_monitor_lib.user_interface(ACTION_TO_INT[self.blackboard.current_action])
        self.blackboard.monitor_var = ('unsafe' if temp == 1 else 'unknown')
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
