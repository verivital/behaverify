import ctypes

# Load the shared library
cumulative_sum_lib = ctypes.CDLL('./cumulative_sum.so')  # Assuming the shared library is named cumulative_sum.so

# Define the argument and return types for the C function
cumulative_sum_lib.cum_sum.argtypes = [ctypes.c_int]
cumulative_sum_lib.cum_sum.restype = ctypes.c_int

# Call the C function in a loop with values from 1 to 10
for i in range(1, 11):
    result = cumulative_sum_lib.cum_sum(i)
    print(f"Current sum after adding {i}: {result}")

# Print the final value of cur_sum
final_sum = cumulative_sum_lib.cur_sum
print(f"Final sum: {final_sum}")



