import ctypes

monitor_lib = ctypes.CDLL('./monitor.so')
monitor_lib.driver.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
monitor_lib.driver.restypes = ctypes.c_bool

states = [
    [0, 6, 1, 0, 2],
    [2, 6, 0, -1, 2],
    [2, 4, 0, -1, 1], #crash inevitable
    [2, 3, 0, -1, 1], #crash occurs
    [2, 4, -1, 0, 1], # reset
    [1, 4, 0, -1, 2]
]
for state in states:
    print(state)
    monitor_lib.driver(state[0], state[1], state[2], state[3])
