# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import argparse
# import os

def handle_file(file_name):
    values = []
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        for line in input_file:
            if line.strip() == '':
                continue
            values.append(float(line.strip()))
    return values

def number_of_nodes(val):
    val = val + 1 # because range starts from 0
    # return val
    return 7 + (2**(val + 1))

encoding_mark = {
    'LTL-MoVe4BT' : ('red', 'o'),
    'CTL-BehaVerify' : ('blue', 'v'),
    'LTL-BehaVerify' : ('black', '*')
}

b_ctl = handle_file('CTL-BehaVerify-Concise')
b_ltl = handle_file('LTL-BehaVerify-Concise')
m_ltl = handle_file('LTL-MoVe4BT-Concise')
plt.plot(list(map(number_of_nodes, range(len(b_ctl)))), b_ctl, color = 'blue', marker = 'v')
plt.plot(list(map(number_of_nodes, range(len(b_ltl)))), b_ltl, color = 'black', marker = '*')
plt.plot(list(map(number_of_nodes, range(len(m_ltl)))), m_ltl, color = 'red', marker = 'o')
plt.ylabel('Time in Seconds to Verify')
plt.xlabel('Number of Nodes in Tree')
plt.title('BehaVerify vs MoVe4BT Verification Times')
plt.legend(['BehaVerify-CTL', 'BehaVerify-LTL', 'MoVe4BT-LTL'])
plt.tight_layout()
plt.savefig('processed_data/2026-FM-MoVe4BT-Timing.png', bbox_inches = 'tight')

plt.clf()
