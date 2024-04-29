import os
import sys

def indent(n):
    return ' '*(4*n)

def create_condition(indent_level, x):
    #return indent(indent_level) + '<Condition ID="IIs' + str(x) + '" failure_guard="bf&lt;' + str(x) + ' || bf&gt;' + str(x) + '" name="NIs' + str(x) + '" success_guard="bf==' + str(x) + '"/>' + os.linesep
    return indent(indent_level) + '<Condition ID="IIs' + str(x) + '" failure_guard="bf!=' + str(x) + '" name="NIs' + str(x) + '" success_guard="bf==' + str(x) + '"/>' + os.linesep

def create_subtree_selector(indent_level, x):
    return (
        indent(indent_level) + '<Fallback name="F' + str(x) + '">' + os.linesep
        + ''.join(
            [
                (create_condition(indent_level + 1, y))
                for y in range(max(0, x-3), x+1)
            ]
        )
        + (
            (
                create_condition(indent_level + 1, 0)
                if x == 4 else
                (
                    ('')
                    if x < 4 else
                    (create_subtree_selector(indent_level + 1, x-4))
                )
            )
        )
        + indent(indent_level) + '</Fallback>' + os.linesep
    )


def create_fish_selector(x):
    number_of_checks = x - 5
    return (
        '<?xml version="1.0"?>' + os.linesep
        + '<root _reach_goal="" env="True" expected_execution_time="" global_vars="var bf=0;" main_tree_to_execute="BehaviorTree" specification="#assert BehaviorTree |= F(IC_s);">' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<BehaviorTree ID="BehaviorTree">' + os.linesep
        + indent(2) + '<Fallback name="FF">' + os.linesep
        + indent(3) + '<Sequence name="BFS">' + os.linesep
        + indent(4) + '<Fallback name="FBF">' + os.linesep
        + ''.join([create_condition(5, y) for y in range(number_of_checks)])
        + indent(4) + '</Fallback>' + os.linesep
        # + create_subtree_selector(4, x)
        + indent(4) + '<Action ID="IBF" failure_guard="0==1" name="NBF" success_guard="bf &gt;= 0" success_program="bf=bf+1" running_guard="0==1"/>' + os.linesep
        + indent(3) + '</Sequence>' + os.linesep
        + indent(3) + '<Condition ID="IC" failure_guard="bf!=' + str(number_of_checks) + '" name="NC" success_guard="bf==' + str(number_of_checks) + '"/>' + os.linesep
        # + indent(3) + '<Condition ID="IC" failure_guard="bf&lt;' + str(x + 1) + ' || bf&gt;' + str(x + 1) + '" name="NC" success_guard="bf==' + str(x + 1) + '"/>' + os.linesep
        + indent(2) + '</Fallback>' + os.linesep
        + indent(1) + '</BehaviorTree>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<TreeNodesModel>' + os.linesep
        + indent(2) + '<Action ID="IBF">' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_program"/>' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="running_guard"/>' + os.linesep
        + indent(2) + '</Action>' + os.linesep
        + indent(2) + '<Condition ID="IC">' + os.linesep
        + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(2) + '</Condition>' + os.linesep
        + ''.join(
            [
                (
                    indent(2) + '<Condition ID="IIs' + str(cur_x) + '">' + os.linesep
                    + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
                    + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
                    + indent(2) + '</Condition>' + os.linesep
                )
                for cur_x in range(x + 1)
            ]
        )
        + indent(1) + '</TreeNodesModel>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + '</root>' + os.linesep
    )


def write_files(location, min_val, max_val, step_size):
    for x in range(min_val, max_val + 1, step_size):
        with open(location + '/' + 'MoVe4BT_bigger_fish_' + str(x) + '.xml', 'w') as f:
            f.write(create_fish_selector(x))


write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
