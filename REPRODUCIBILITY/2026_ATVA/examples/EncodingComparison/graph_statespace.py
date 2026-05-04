import sys
import os
import re
import matplotlib.pyplot as plt


def handle_file(file_name):
    '''Read state space values from a file, one value per line.
    Returns (values, hit_timeout) where hit_timeout is True if TIMEOUT was encountered.'''
    values = []
    hit_timeout = False
    if not os.path.exists(file_name):
        return values, hit_timeout
    with open(file_name, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            if line.strip() == '':
                continue
            val = line.strip()
            if val == 'TIMEOUT':
                hit_timeout = True
                break  # Stop reading when we hit timeout
            else:
                values.append(int(val))
    return values, hit_timeout


def extract_reachable_states(results_dir, prefix, count=10):
    '''Extract reachable states from nuXmv output files.
    Format: "reachable states: 9 (2^3.16993) out of 24 (2^4.58496)"
    We want the first number after "reachable states:".'''
    values = []
    hit_timeout = False

    for i in range(1, count + 1):
        file_path = os.path.join(results_dir, f'{prefix}_binary_tree_{i}.txt')
        if not os.path.exists(file_path):
            hit_timeout = True
            break

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for "reachable states: X" pattern
        match = re.search(r'reachable states: (\d+)', content)
        if match:
            values.append(int(match.group(1)))
        else:
            # No match means timeout or error
            hit_timeout = True
            break

    return values, hit_timeout


def parse_move4bt_visited_states(file_name):
    '''Parse MoVe4BT results file to extract visited states per level.'''
    values = []
    hit_timeout = False
    if not os.path.exists(file_name):
        return values, hit_timeout

    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by level markers --1--, --2--, etc.
    sections = re.split(r'--(\d+)--', content)

    # Parse each section
    for i in range(1, len(sections), 2):
        level = int(sections[i])
        section_content = sections[i + 1] if i + 1 < len(sections) else ''

        # Check if this section has a timeout (process destroyed)
        if 'Destroyed while process' in section_content or 'QProcess' in section_content:
            hit_timeout = True
            break

        # Extract visited states
        match = re.search(r'Visited States:\s*(\d+)', section_content)
        if match:
            values.append(int(match.group(1)))
        else:
            # If no visited states found, assume timeout
            hit_timeout = True
            break

    return values, hit_timeout


def number_of_nodes(val):
    '''Calculate number of nodes in a binary tree of given level.
    Formula: 7 + 2^(level+1) where val is 0-indexed level.'''
    val = val + 1
    return 7 + (2**(val + 1))


# Read reachable states from nuXmv result files
results_dir = 'results'
states_ff, states_ff_timeout = extract_reachable_states(results_dir, 'STATES_FF', 10)
states_naive, states_naive_timeout = extract_reachable_states(results_dir, 'STATES_NAIVE', 10)

# Read MoVe4BT visited states
move4bt_path = '../../results/examples/MoVe4BT/MoVe4BT-Results'
states_move4bt, states_move4bt_timeout = parse_move4bt_visited_states(move4bt_path)


def create_statespace_comparison_figure():
    '''Create state space comparison figure as a line graph.'''
    if not states_ff and not states_naive and not states_move4bt:
        print('No state space data available.')
        return

    plt.figure(figsize=(12, 8))

    # Plot fastforwarding results (solid line)
    if states_ff:
        x_ff = list(map(number_of_nodes, range(len(states_ff))))
        plt.plot(x_ff, states_ff,
                 color='green', marker='^', linewidth=2, markersize=8, linestyle='-',
                 label='BehaVerify Fastforwarding')

    # Plot naive results (dashed line)
    if states_naive:
        x_naive = list(map(number_of_nodes, range(len(states_naive))))
        plt.plot(x_naive, states_naive,
                 color='red', marker='s', linewidth=2, markersize=8, linestyle='--',
                 label='BehaVerify Naive' + (' *' if states_naive_timeout else ''))

    # Plot MoVe4BT results (dotted line)
    if states_move4bt:
        x_move4bt = list(map(number_of_nodes, range(len(states_move4bt))))
        plt.plot(x_move4bt, states_move4bt,
                 color='purple', marker='o', linewidth=2, markersize=8, linestyle=':',
                 label='MoVe4BT Visited States' + (' *' if states_move4bt_timeout else ''))

    plt.ylabel('Number of Reachable/Visited States', fontsize=12)
    plt.xlabel('Number of Nodes in Behavior Tree', fontsize=12)
    plt.title('State Space Comparison: BehaVerify Encodings vs MoVe4BT', fontsize=14)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)

    if any([states_naive_timeout, states_move4bt_timeout]):
        plt.figtext(0.99, 0.01, '* Line stops at timeout', ha='right', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('processed_data/2026-FM-StateSpace-Comparison.png', bbox_inches='tight', dpi=150)
    print('Graph saved to processed_data/2026-FM-StateSpace-Comparison.png')

    # Also create a log-scale version
    plt.yscale('log')
    plt.savefig('processed_data/2026-FM-StateSpace-Comparison-Log.png', bbox_inches='tight', dpi=150)
    print('Log-scale graph saved to processed_data/2026-FM-StateSpace-Comparison-Log.png')
    plt.clf()


if __name__ == '__main__':
    # Ensure output directory exists
    os.makedirs('processed_data', exist_ok=True)

    # Create figure
    create_statespace_comparison_figure()

    # Print summary
    print('\nState space summary:')
    max_len = max(len(states_ff) if states_ff else 0,
                  len(states_naive) if states_naive else 0,
                  len(states_move4bt) if states_move4bt else 0)

    for i in range(max_len):
        nodes = number_of_nodes(i)
        ff_val = states_ff[i] if states_ff and i < len(states_ff) else 'N/A'
        naive_val = states_naive[i] if states_naive and i < len(states_naive) else 'TIMEOUT'
        m4bt_val = states_move4bt[i] if states_move4bt and i < len(states_move4bt) else 'TIMEOUT'
        print(f'  {nodes} nodes: FF={ff_val}, Naive={naive_val}, MoVe4BT={m4bt_val}')

    print('\nAll state space graphs generated successfully.')
