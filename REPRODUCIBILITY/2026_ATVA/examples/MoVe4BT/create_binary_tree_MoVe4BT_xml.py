import os
import sys

def indent(n):
    return ' '*(4*n)

def create_tree_struct(indent_level, levels_left, node_number):
    if levels_left == 0:
        return (
            indent(indent_level) + '<Condition ID="AtVal' + str(node_number) + '" failure_guard="vv!=' + str(node_number) + '" success_guard="vv==' + str(node_number) + '"/>' + os.linesep,
            indent(2) + '<Condition ID="AtVal' + str(node_number) + '">' + os.linesep
            + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
            + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
            + indent(2) + '</Condition>' + os.linesep,
            node_number + 1
        )
    (left_child, later1, node_number) = create_tree_struct(indent_level + 1, levels_left - 1, node_number)
    (right_child, later2, node_number) = create_tree_struct(indent_level + 1, levels_left - 1, node_number)
    return (
        indent(indent_level) + '<Fallback>' + os.linesep
        + left_child
        + right_child
        + indent(indent_level) + '</Fallback>' + os.linesep,
        later1 + later2,
        node_number
    )


def create_tree(levels):
    (tree, post, max_val) = create_tree_struct(3, levels, 0)
    return (
        '<?xml version="1.0"?>' + os.linesep
        + '<root _reach_goal="" env="True" expected_execution_time="" global_vars="var vv=0;" main_tree_to_execute="BehaviorTree" specification="#assert BehaviorTree |= G(AtMaxA_s -&gt; G(!(AtMaxA_f) &amp;&amp; !(At0A_s) &amp;&amp; !(Dec_s) &amp;&amp; !(Dec_f) &amp;&amp; !(Inc_s) &amp;&amp; !(Inc_f)));">' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<BehaviorTree ID="BehaviorTree">' + os.linesep
        + indent(2) + '<Sequence>' + os.linesep
        + indent(3) + '<Fallback>' + os.linesep
        + indent(4) + '<Condition ID="At0A" failure_guard="vv!=0" success_guard="vv==0"/>' + os.linesep
        + indent(4) + '<Condition ID="AtMaxA" failure_guard="vv!=' + str(max_val) + '" success_guard="vv==' + str(max_val) + '"/>' + os.linesep
        + indent(4) + '<Action ID="Dec" failure_guard="0==0" failure_program="vv=vv-1" success_guard="0==0" success_program="vv=vv" running_guard="0==1"/>' + os.linesep
        + indent(3) + '</Fallback>' + os.linesep
        + tree
        + indent(3) + '<Fallback>' + os.linesep
        + indent(4) + '<Condition ID="AtMaxB" failure_guard="vv!=' + str(max_val) + '" success_guard="vv==' + str(max_val) + '"/>' + os.linesep
        + indent(4) + '<Action ID="Inc" failure_guard="0==0" failure_program="vv=vv" success_guard="0==0" success_program="vv=vv+1" running_guard="0==1"/>' + os.linesep
        + indent(3) + '</Fallback>' + os.linesep
        + indent(2) + '</Sequence>' + os.linesep
        + indent(1) + '</BehaviorTree>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<TreeNodesModel>' + os.linesep
        + indent(2) + '<Action ID="Dec">' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_program"/>' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="failure_program"/>' + os.linesep
        + indent(3) + '<inout_port name="running_guard"/>' + os.linesep
        + indent(2) + '</Action>' + os.linesep
        + indent(2) + '<Action ID="Inc">' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_program"/>' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="failure_program"/>' + os.linesep
        + indent(3) + '<inout_port name="running_guard"/>' + os.linesep
        + indent(2) + '</Action>' + os.linesep
        + indent(2) + '<Condition ID="At0A">' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(2) + '</Condition>' + os.linesep
        + indent(2) + '<Condition ID="AtMaxA">' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(2) + '</Condition>' + os.linesep
        + indent(2) + '<Condition ID="AtMaxB">' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(2) + '</Condition>' + os.linesep
        + post
        + indent(1) + '</TreeNodesModel>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + '</root>' + os.linesep
    )


def write_files(location, min_val, max_val, step_size):
    for x in range(min_val, max_val + 1, step_size):
        with open(location + '/' + 'MoVe4BT_binary_tree_' + str(x) + '.xml', 'w') as f:
            f.write(create_tree(x))


write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
