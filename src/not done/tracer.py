import argparse
import sys
import os
import re
import pprint
import copy


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_file') 
    arg_parser.add_argument('--output_file', default = None)
    
    arg_parser.add_argument('--interactive_mode', action = 'store_true')
    arg_parser.add_argument('--instruction_file', default = None)
    
    arg_parser.add_argument('--force_parallel_unsynch', action = 'store_true')
    arg_parser.add_argument('--force_parallel_synch', action = 'store_true')
    arg_parser.add_argument('--force_selector_memory', action = 'store_true')
    arg_parser.add_argument('--force_selector_memoryless', action = 'store_true')
    arg_parser.add_argument('--force_sequence_memory', action = 'store_true')
    arg_parser.add_argument('--force_sequence_memoryless', action = 'store_true')
    arg_parser.add_argument('--use_next_checks', action = 'store_true')
    arg_parser.add_argument('--use_current_checks', action = 'store_true')
    arg_parser.add_argument('--best_guess_checks', action = 'store_true')

    
    args = arg_parser.parse_args()



    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']

    node_name_to_id = {}
    for node_id in nodes:
        #print(node_id)
        node_name_to_id[nodes[node_id]['name']] = node_id

    #---------------------------------------------actual code rather than references for how to successfully make an argparser

    violated_property = something
    trace = something_else

    #ok so we could represent the BTrees state and then test what changes keep violating the property
    #hmmm. this seems like a very large amount of work tbh.
    #
    #the other main option would seemingly be to literally trace the path out, but i'm not quite sure how helpful that would be.
    #what could be reasonable would be to build out a dependancy graph of the entire tree, then walk backwards through it?

    
main()
