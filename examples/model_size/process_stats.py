import matplotlib.pyplot as plt
import re
import sys

vals_size=[]
vals_diameter=[]
vals_reachable=[]
vals_reachable_pow=[]
vals_total=[]
vals_total_pow=[]

reach=re.compile("reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)")
with open(sys.argv[1]+'/stats', 'r') as cur_file:
    for line in cur_file:
        if "Number of BDD variables:" in line:
            val=line.split(':')[1]
            val=int(val.strip())
            vals_size.append(val)
        if "system diameter:" in line:
            val=line.split(':')[1]
            val=int(val.strip())
            vals_diameter.append(val)
        match=reach.search(line)
        if match:
            #vals_reachable.append(int(match.group('val1')))
            vals_reachable_pow.append(float(match.group('val2')))
            #vals_total.append(int(match.group('val3')))
            vals_total_pow.append(float(match.group('val4')))
            
plt.plot(vals_size)
plt.savefig(sys.argv[1]+'/sizes.png')
print(vals_size)
plt.close()
plt.plot(vals_diameter)
plt.savefig(sys.argv[1]+'/system_diameter.png')
print(vals_diameter)
plt.close()
"""
plt.plot(vals_reachable, label='reachable')
plt.plot(vals_total, label='total')
plt.savefig('./size_models/reachable_total_states.png')
print(vals_reachable)
plt.close()
"""
plt.plot(vals_reachable_pow, label='reachable')
plt.plot(vals_total_pow, label='total')
plt.savefig(sys.argv[1]+'/reachable_total_states_pow.png')
print(vals_reachable_pow)
plt.close()
