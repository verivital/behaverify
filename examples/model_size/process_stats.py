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

if 'wide' in sys.argv[1]:
    x_vals=[*range(3, 22)]
else:
    x_vals=[*range(1, 5)]
    x_vals=[2**(i+1)-1 for i in x_vals]

#fig_sizes = plt.figure()
plt.plot(x_vals, vals_size)
plt.xlabel('number of nodes')
plt.ylabel('number of BDD variables')
plt.savefig(sys.argv[1]+'/sizes.png')
plt.close()
print(vals_size)

plt.plot(x_vals, vals_diameter)
plt.xlabel('number of nodes')
plt.ylabel('system diameter')
plt.savefig(sys.argv[1]+'/system_diameter.png')
print(vals_diameter)
plt.close()

plt.plot(x_vals, vals_reachable_pow, label='reachable')
plt.plot(x_vals, vals_total_pow, label='total')
plt.xlabel('number of nodes')
plt.ylabel('log2(number of states)')
plt.savefig(sys.argv[1]+'/reachable_total_states_pow.png')
plt.close()


plt.plot(x_vals, vals_reachable_pow, label='reachable')
plt.xlabel('number of nodes')
plt.ylabel('log2(number of reachable states)')
plt.savefig(sys.argv[1]+'/reachable_states_pow.png')
print(vals_reachable_pow)
plt.close()


plt.plot(x_vals, vals_total_pow, label='total')
plt.xlabel('number of nodes')
plt.ylabel('log2(number of total states)')
plt.savefig(sys.argv[1]+'/total_states_pow.png')
print(vals_total_pow)
plt.close()
