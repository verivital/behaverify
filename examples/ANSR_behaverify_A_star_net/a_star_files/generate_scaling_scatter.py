import sys
import os
from misc_util import create_tail_end, handle_path

def generate_scaling_obstalces(min_val, max_val):
    for n in range(min_val, max_val + 1):
        lines_start = []
        lines_end = []
        index = 0
        for x in range(0, n):
            for y in range(0, n):
                if (
                        ((x == y) and ((x % 2) == 1)) or
                        ((x != 0) and (y != 0) and (x != y) and (y > 1) and ((x % y) == 0)) or
                        ((x != 0) and (y != 0) and (x != y) and (x > 1) and ((y % x) == 0)) or
                        ((x == 1) and (y % 2) == 0) or
                        ((y == 1) and (x % 2) == 0) or
                        (x == 0 and y == 0)
                ):
                    lines_start.append(
                        'condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(x) + '}}'
                        + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(y) + '}}' + os.linesep
                    )
                    lines_end.append('condition {(eq, index_var, ' + str(index) + ')} assign{result{0}}' + os.linesep)
                    index = index + 1
        tail_end = create_tail_end(n - 1, None, len(lines_start), 0)
        lines = lines_start + ['##################################################################' + os.linesep] + lines_end
        with open(handle_path('scaling_scatter/obstacles' + tail_end + '.txt'), 'w', encoding = 'utf-8') as output_file:
            output_file.writelines(lines)

if __name__ == '__main__':
    generate_scaling_obstalces(int(sys.argv[1]), int(sys.argv[2]))
