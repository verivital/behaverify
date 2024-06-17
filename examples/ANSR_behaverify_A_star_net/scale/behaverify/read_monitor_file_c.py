import py_trees
import math
import operator
import ctypes
import os
THIS_LOCATION = os.path.dirname(os.path.abspath(__file__))
collision_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'collision_monitor.so'))
collision_monitor_lib.collision_monitor_transition.argtypes = [ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
collision_monitor_lib.collision_monitor_transition.restype = ctypes.c_int
loop_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'loop_monitor.so'))
loop_monitor_lib.loop_monitor_transition.argtypes = [ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool), ctypes.c_char_p]
loop_monitor_lib.loop_monitor_transition.restype = ctypes.c_int

COLLISION_MONITOR = (ctypes.c_bool * 1)(True)
LOOP_MONITOR = (ctypes.c_bool * 16)(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
obs_array = None
obs_size_array = None

class read_monitor(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_monitor, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_speed'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('monitor_var'), access = py_trees.common.Access.WRITE)

    def update(self):
        global COLLISION_MONITOR, LOOP_MONITOR, obs_array, obs_size_array
        if obs_array is None:
            obs_array = (ctypes.c_int * len(self.environment.obstacles))(*self.environment.obstacles)
            obs_size_array = (ctypes.c_int * len(self.environment.obstacle_sizes))(*self.environment.obstacle_sizes)
        self.blackboard.drone_speed = 2
        temp_var = collision_monitor_lib.collision_monitor_transition(
            COLLISION_MONITOR,
            (ctypes.c_bool * 1)(),
            self.blackboard.delta_x(),
            self.blackboard.delta_y(),
            self.blackboard.drone_x,
            self.blackboard.drone_y,
            obs_size_array,
            obs_array
        )
        self.blackboard.monitor_var = ('safe' if temp_var == 0 else ('unknown' if temp_var == 1 else 'unsafe'))
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        loop_output = (ctypes.c_bool * 16)()
        temp_var = loop_monitor_lib.loop_monitor_transition(
            LOOP_MONITOR,
            loop_output,
            self.blackboard.current_action.encode('utf-8')
        )
        self.blackboard.monitor_var = ('safe' if temp_var == 0 else ('unknown' if temp_var == 1 else 'unsafe'))
        if self.blackboard.monitor_var == 'unsafe':
            LOOP_MONITOR = (ctypes.c_bool * 16)(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
        else:
            LOOP_MONITOR = loop_output
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
