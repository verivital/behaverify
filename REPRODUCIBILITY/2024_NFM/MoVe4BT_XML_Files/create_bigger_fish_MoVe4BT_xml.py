import os
import sys

def indent(n):
    return ' '*(4*n)

def create_condition(indent_level, x):
    return indent(indent_level) + '<Condition ID="Is' + str(x) + '" failure_guard="bf&lt;' + str(x) + ' || bf&gt;' + str(x) + '" success_guard="bf==' + str(x) + '"/>' + os.linesep

def create_subtree_selector(indent_level, x):
    return (
        indent(indent_level) + '<Fallback>' + os.linesep
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
        + indent(indent_level + 1) + 'sequence' + str(x) + os.linesep
        + indent(indent_level + 1) + 'sequence' + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
    )


def create_fish_selector(x):
    return (
        '<?xml version="1.0"?>' + os.linesep
        + '<root _reach_goal="" env="True" expected_execution_time="1" global_vars="var bf=0;" main_tree_to_execute="BehaviorTree" specification="#define goal bf==' + str(x + 1) +';&#10;#assert DeadlineProcess reaches goal;">' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<BehaviorTree ID="BehaviorTree">' + os.linesep
        + indent(2) + '<Sequence>' + os.linesep
        + create_subtree_selector(3, x)
        + indent(3) + '<Action ID="BiggerFish" success_guard="bf &gt;= 0" success_program="bf=bf+1"/>' + os.linesep
        + indent(2) + '</Sequence>' + os.linesep
        + indent(1) + '</BehaviorTree>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<TreeNodesModel>' + os.linesep
        + indent(2) + '<Action ID="BiggerFish">' + os.linesep
        + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
        + indent(3) + '<inout_port name="success_program"/>' + os.linesep
        + indent(2) + '</Action>' + os.linesep
        + ''.join(
            [
                (
                    indent(2) + '<Condition ID="Is' + str(cur_x) + '">' + os.linesep
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
        with open(location + '/' + 'MoVE4BT_bigger_fish_selector__' + str(x) + '.xml', 'w') as f:
            f.write(create_fish_selector(x))


write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
