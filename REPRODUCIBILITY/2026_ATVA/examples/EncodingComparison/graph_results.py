import sys
import os
import matplotlib.pyplot as plt


# Configurable timeout value (default 30s for quick runs)
# Can be changed to 300s (5 minutes) for paper results
TIMEOUT_VALUE = 30.0
if len(sys.argv) > 1:
    TIMEOUT_VALUE = float(sys.argv[1])


def handle_file(file_name):
    '''Read timing values from a file, one value per line.
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
                values.append(float(val))
    return values, hit_timeout


def number_of_nodes(val):
    '''Calculate number of nodes in a binary tree of given level.
    Formula: 7 + 2^(level+1) where val is 0-indexed level.'''
    val = val + 1
    return 7 + (2**(val + 1))


# Read all encoding comparison timing files
ltl_ff, ltl_ff_timeout = handle_file('LTL-Fastforwarding-Concise')
ctl_ff, ctl_ff_timeout = handle_file('CTL-Fastforwarding-Concise')
ltl_naive, ltl_naive_timeout = handle_file('LTL-Naive-Concise')
ctl_naive, ctl_naive_timeout = handle_file('CTL-Naive-Concise')

# Read MoVe4BT timing files (from results directory)
move4bt_path = '../../results/examples/MoVe4BT/'
b_ctl, _ = handle_file(move4bt_path + 'CTL-BehaVerify-Concise')
b_ltl, _ = handle_file(move4bt_path + 'LTL-BehaVerify-Concise')
m_ltl, m_ltl_timeout = handle_file(move4bt_path + 'LTL-MoVe4BT-Concise')


def create_single_combined_figure():
    '''Create a single figure with ALL data: encoding comparison + MoVe4BT.'''
    plt.figure(figsize=(12, 8))

    # BehaVerify Fastforwarding (solid lines)
    if ctl_ff:
        x = list(map(number_of_nodes, range(len(ctl_ff))))
        plt.plot(x, ctl_ff, color='green', marker='^', linewidth=2, markersize=8,
                 linestyle='-', label='BehaVerify CTL (Fastforwarding)')
    if ltl_ff:
        x = list(map(number_of_nodes, range(len(ltl_ff))))
        plt.plot(x, ltl_ff, color='blue', marker='v', linewidth=2, markersize=8,
                 linestyle='-', label='BehaVerify LTL (Fastforwarding)' + (' *' if ltl_ff_timeout else ''))

    # BehaVerify Naive (dashed lines)
    if ctl_naive:
        x = list(map(number_of_nodes, range(len(ctl_naive))))
        plt.plot(x, ctl_naive, color='orange', marker='D', linewidth=2, markersize=8,
                 linestyle='--', label='BehaVerify CTL (Naive)' + (' *' if ctl_naive_timeout else ''))
    if ltl_naive:
        x = list(map(number_of_nodes, range(len(ltl_naive))))
        plt.plot(x, ltl_naive, color='red', marker='s', linewidth=2, markersize=8,
                 linestyle='--', label='BehaVerify LTL (Naive)' + (' *' if ltl_naive_timeout else ''))

    # MoVe4BT (dotted line)
    if m_ltl:
        x = list(map(number_of_nodes, range(len(m_ltl))))
        plt.plot(x, m_ltl, color='purple', marker='o', linewidth=2, markersize=8,
                 linestyle=':', label='MoVe4BT LTL' + (' *' if m_ltl_timeout else ''))

    plt.ylabel('Verification Time (seconds)', fontsize=12)
    plt.xlabel('Number of Nodes in Behavior Tree', fontsize=12)
    plt.title('Verification Time Comparison: BehaVerify Encodings vs MoVe4BT', fontsize=14)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)

    # Add footnote for timeout
    if any([ctl_ff_timeout, ltl_ff_timeout, ctl_naive_timeout, ltl_naive_timeout, m_ltl_timeout]):
        plt.figtext(0.99, 0.01, '* Line stops at timeout', ha='right', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('processed_data/2026-FM-All-Comparison.png', bbox_inches='tight', dpi=150)
    print('Combined graph saved to processed_data/2026-FM-All-Comparison.png')

    # Log scale version
    plt.yscale('log')
    plt.savefig('processed_data/2026-FM-All-Comparison-Log.png', bbox_inches='tight', dpi=150)
    print('Log-scale combined graph saved to processed_data/2026-FM-All-Comparison-Log.png')
    plt.clf()


def create_encoding_comparison_figure():
    '''Create encoding comparison only (fastforwarding vs naive).'''
    plt.figure(figsize=(12, 8))

    # Plot fastforwarding results (solid lines)
    if ltl_ff:
        x_ltl_ff = list(map(number_of_nodes, range(len(ltl_ff))))
        plt.plot(x_ltl_ff, ltl_ff,
                 color='blue', marker='v', linewidth=2, markersize=8, linestyle='-',
                 label='LTL Fastforwarding' + (' *' if ltl_ff_timeout else ''))
    if ctl_ff:
        x_ctl_ff = list(map(number_of_nodes, range(len(ctl_ff))))
        plt.plot(x_ctl_ff, ctl_ff,
                 color='green', marker='^', linewidth=2, markersize=8, linestyle='-',
                 label='CTL Fastforwarding')

    # Plot naive results (dashed lines)
    if ltl_naive:
        x_ltl_naive = list(map(number_of_nodes, range(len(ltl_naive))))
        plt.plot(x_ltl_naive, ltl_naive,
                 color='red', marker='s', linewidth=2, markersize=8, linestyle='--',
                 label='LTL Naive' + (' *' if ltl_naive_timeout else ''))
    if ctl_naive:
        x_ctl_naive = list(map(number_of_nodes, range(len(ctl_naive))))
        plt.plot(x_ctl_naive, ctl_naive,
                 color='orange', marker='D', linewidth=2, markersize=8, linestyle='--',
                 label='CTL Naive' + (' *' if ctl_naive_timeout else ''))

    plt.ylabel('Verification Time (seconds)', fontsize=12)
    plt.xlabel('Number of Nodes in Behavior Tree', fontsize=12)
    plt.title('BehaVerify Encoding Comparison: Fastforwarding vs Naive', fontsize=14)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)

    if any([ltl_ff_timeout, ctl_ff_timeout, ltl_naive_timeout, ctl_naive_timeout]):
        plt.figtext(0.99, 0.01, '* Line stops at timeout', ha='right', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('processed_data/2026-FM-Encoding-Comparison.png', bbox_inches='tight', dpi=150)
    print('Graph saved to processed_data/2026-FM-Encoding-Comparison.png')

    # Also create a log-scale version
    plt.yscale('log')
    plt.savefig('processed_data/2026-FM-Encoding-Comparison-Log.png', bbox_inches='tight', dpi=150)
    print('Log-scale graph saved to processed_data/2026-FM-Encoding-Comparison-Log.png')
    plt.clf()


if __name__ == '__main__':
    # Ensure output directory exists
    os.makedirs('processed_data', exist_ok=True)

    # Create figures
    create_encoding_comparison_figure()
    create_single_combined_figure()

    print(f'\nTimeout value used: {TIMEOUT_VALUE}s')
    print('All graphs generated successfully.')
