import sys
import os

location = sys.argv[1]

with open(location + 'template.tree', 'r') as f:
    template = f.read()

root = [('selector', 'sel'), ('sequence', 'seq'), ('parallel policy success_on_all', 'p_all'), ('parallel policy success_on_one', 'p_one')]
child = ['f', 's', 'r']

for (root_type, root_name) in root:
    for child1 in child:
        for child2 in child:
            with open(location + root_name + '_' + child1 + '_' + child2 + '.tree', 'w') as f:
                f.write(template + os.linesep
                        + 'tree {' + os.linesep
	                + 'composite {' + root_name + ' ' + root_type + ' children { ' + child1 + ' ' + child2 + '}}' + os.linesep
                        + '}' + os.linesep
                        + 'specifications { #comment# INVAR, LTL, and CTL specs go here #end_comment# } end_specifications'
                        )
