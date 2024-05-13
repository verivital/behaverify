import ctypes

monitor_lib = ctypes.CDLL('./monitor.so')

class RV_reset(ctypes.c_int):
    pass

class RV_value(ctypes.c_int):
    pass

# RV_value monitor_ex (long *states, size_t width, RV_reset reset, int *current_loc);
monitor_lib.monitor_ex.argtypes = [ctypes.POINTER(ctypes.c_long), ctypes.c_size_t, RV_reset, ctypes.POINTER(ctypes.c_int)]
monitor_lib.monitor_ex.restype = RV_value

no_reset = RV_reset(0)
current_loc = ctypes.c_int(1)

for i in range(10):
    k = monitor_lib.monitor_ex(ctypes.c_long(i), 1, no_reset, ctypes.byref(current_loc))
    print(k.value)
