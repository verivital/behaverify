




import sys

def generate_scaling_obstalces(min_val, max_val):
    for n in range(min_val, max_val + 1):
        list_of_points = []
        now_at = (0, 0)
        if n % 4 == 0:
            now_at = ((n / 2) - 1, n / 2)
        elif n % 4 == 1:
            now_at = ((n - 1) / 2, (n + 1) / 2)
        elif n % 4 == 2:
            now_at = (n / 2, n / 2)
        elif n % 4 == 3:
            now_at = ((n - 1) / 2, (n - 1) / 2)
        direction = 'right'
        count_max = 1
        count_current = count_max
        while (
                now_at[0] != 0 and
                now_at[1] != 0 and
                now_at[0] != n - 1 and
                now_at[1] != n - 1
        ):
            list_of_points.append(now_at)
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
                
            

if __name__ == '__main__':
    generate_scaling_obstalces(int(sys.argv[1]), int(sys.argv[2]))
