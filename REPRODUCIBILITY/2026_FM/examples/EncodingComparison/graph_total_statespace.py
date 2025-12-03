import sys
import os
import re
import matplotlib.pyplot as plt


def extract_total_statespace(results_dir, prefix, count=10):
    '''Extract total state space from nuXmv output files.
    Format: "reachable states: 9 (2^3.16993) out of 24 (2^4.58496)"
    Or with scientific notation: "out of 3.34611e+06 (2^21.6741)"
    We want the number after "out of".'''
    values = []
    hit_timeout = False

    for i in range(1, count + 1):
        file_path = os.path.join(results_dir, f'{prefix}_binary_tree_{i}.txt')
        if not os.path.exists(file_path):
            hit_timeout = True
            break

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for "out of X" pattern - handles both integer and scientific notation
        match = re.search(r'out of ([\d.]+(?:e[+\-]?\d+)?)', content)
        if match:
            val_str = match.group(1)
            # Convert to integer (handles scientific notation)
            values.append(int(float(val_str)))
        else:
            # No match means timeout or error
            hit_timeout = True
            break

    return values, hit_timeout


def number_of_nodes(val):
    '''Calculate number of nodes in a binary tree of given level.
    Formula: 7 + 2^(level+1) where val is 0-indexed level.'''
    val = val + 1
    return 7 + (2**(val + 1))


# Extract total state space from existing results
results_dir = 'results'
total_ff, total_ff_timeout = extract_total_statespace(results_dir, 'STATES_FF', 10)
total_naive, total_naive_timeout = extract_total_statespace(results_dir, 'STATES_NAIVE', 10)


def create_total_statespace_figure():
    '''Create total state space comparison figure as a line graph.'''
    if not total_ff and not total_naive:
        print('No total state space data available.')
        return

    plt.figure(figsize=(12, 8))

    # Plot fastforwarding results (solid line)
    if total_ff:
        x_ff = list(map(number_of_nodes, range(len(total_ff))))
        plt.plot(x_ff, total_ff,
                 color='green', marker='^', linewidth=2, markersize=8, linestyle='-',
                 label='BehaVerify Fastforwarding')

    # Plot naive results (dashed line)
    if total_naive:
        x_naive = list(map(number_of_nodes, range(len(total_naive))))
        plt.plot(x_naive, total_naive,
                 color='red', marker='s', linewidth=2, markersize=8, linestyle='--',
                 label='BehaVerify Naive' + (' *' if total_naive_timeout else ''))

    plt.ylabel('Total State Space Size', fontsize=12)
    plt.xlabel('Number of Nodes in Behavior Tree', fontsize=12)
    plt.title('Total State Space Size: BehaVerify Fastforwarding vs Naive Encoding', fontsize=14)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)

    if total_naive_timeout:
        plt.figtext(0.99, 0.01, '* Line stops at timeout', ha='right', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('processed_data/2026-FM-TotalStateSpace-Comparison.png', bbox_inches='tight', dpi=150)
    print('Graph saved to processed_data/2026-FM-TotalStateSpace-Comparison.png')

    # Also create a log-scale version
    plt.yscale('log')
    plt.savefig('processed_data/2026-FM-TotalStateSpace-Comparison-Log.png', bbox_inches='tight', dpi=150)
    print('Log-scale graph saved to processed_data/2026-FM-TotalStateSpace-Comparison-Log.png')
    plt.clf()


if __name__ == '__main__':
    # Ensure output directory exists
    os.makedirs('processed_data', exist_ok=True)

    # Create figure
    create_total_statespace_figure()

    # Print summary
    print('\nTotal state space summary:')
    max_len = max(len(total_ff) if total_ff else 0,
                  len(total_naive) if total_naive else 0)

    for i in range(max_len):
        nodes = number_of_nodes(i)
        ff_val = total_ff[i] if total_ff and i < len(total_ff) else 'N/A'
        naive_val = total_naive[i] if total_naive and i < len(total_naive) else 'TIMEOUT'
        print(f'  {nodes} nodes: FF={ff_val}, Naive={naive_val}')

    print('\nTotal state space graph generated successfully.')
