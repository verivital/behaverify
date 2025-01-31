import sys
import os
from misc_util import create_tail_end, handle_path

def generate_scaling_obstalces(min_val, max_val):
    for n in range(min_val, max_val + 1):
        lines_start = []
        lines_end = []
        now_at = (0, 0)
        if n % 4 == 0:
            now_at = ((n // 2) - 1, n // 2)
        elif n % 4 == 1:
            now_at = ((n - 1) // 2, (n + 1) // 2)
        elif n % 4 == 2:
            now_at = (n // 2, n // 2)
        elif n % 4 == 3:
            now_at = ((n - 1) // 2, (n - 1) // 2)
        direction = 'right'
        count_max = 1
        count_current = count_max
        index = 0
        while (
                now_at[0] != 0 and
                now_at[1] != 0 and
                now_at[0] != n - 1 and
                now_at[1] != n - 1
        ):
            lines_start.append(
                'condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(now_at[0]) + '}}'
                + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(now_at[1]) + '}}' + os.linesep
            )
            lines_end.append('condition {(eq, index_var, ' + str(index) + ')} assign{result{0}}' + os.linesep)
            index = index + 1
            count_current = count_current - 1
            if direction == 'right':
                now_at = (now_at[0] + 1, now_at[1])
                if count_current == 0:
                    direction = 'down'
            elif direction == 'left':
                now_at = (now_at[0] - 1, now_at[1])
                if count_current == 0:
                    direction = 'up'
            elif direction == 'up':
                now_at = (now_at[0], now_at[1] + 1)
                if count_current == 0:
                    direction = 'right'
            elif direction == 'down':
                now_at = (now_at[0], now_at[1] - 1)
                if count_current == 0:
                    direction = 'left'
            if count_current == 0:
                count_max = count_max + 1
                count_current = count_max
        tail_end = create_tail_end(n - 1, None, len(lines_start), 0)
        lines = lines_start + ['##################################################################' + os.linesep] + lines_end
        with open(handle_path('scaling_maze/obstacles' + tail_end + '.txt'), 'w', encoding = 'utf-8') as output_file:
            output_file.writelines(lines)

if __name__ == '__main__':
    generate_scaling_obstalces(int(sys.argv[1]), int(sys.argv[2]))
