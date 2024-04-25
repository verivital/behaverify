import os
import sys

def indent(n):
    return ' '*(4*n)

def create_simple_robot(grid_size):
    condition_ids = ['IC', 'ICE', 'IXS', 'IXB', 'IYS', 'IYB']
    action_ids = ['IURG', 'IARX', 'IARY',  'IGR', 'IGL', 'IGU', 'IGD'] + [('IARX' + str(val)) for val in range(grid_size - 1)] + [('IARY' + str(val)) for val in range(grid_size - 1)]
    return (
        '<?xml version="1.0"?>' + os.linesep
        + '<root _reach_goal="" env="True" expected_execution_time="" global_vars="var dx=0;&#10;var dy=0;&#10;var gx=0;&#10;var gy=0;&#10;var rg=4;" main_tree_to_execute="BehaviorTree" specification="#assert BehaviorTree |= F(IC_s);">' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<BehaviorTree ID="BehaviorTree">' + os.linesep
        + indent(2) + '<Fallback name="FC">' + os.linesep
        + indent(3) + '<Condition ID="IC" failure_guard="rg!=0" name="NC" success_guard="rg==0"/>' + os.linesep
        + indent(3) + '<Sequence name="SE">' + os.linesep
        + indent(4) + '<Fallback name="FE">' + os.linesep
        + indent(5) + '<Condition ID="ICE" failure_guard="dx==gx &amp;&amp; dy==gy" name="NCE" success_guard="dx!=gx || dy!=gy"/>' + os.linesep
        + indent(5) + '<Sequence name="SU">' + os.linesep
        + indent(6) + '<Action ID="IURG" failure_guard="0==1" name="NURG" running_guard="0==1" success_guard="0==0" success_program="rg=rg-1"/>' + os.linesep
        + indent(6) + '<Fallback name="RX">' + os.linesep
        + ''.join([
            (indent(7) + '<Action ID="IARX' + str(x_val) + '" failure_guard="0==0" name="NARX' + str(x_val) + '" running_guard="0==1" success_guard="0==0" success_program="gx=' + str(x_val) + '"/>' + os.linesep)
            for x_val in range(grid_size - 1)
        ])
        + indent(7) + '<Action ID="IARX' + str(grid_size - 1) + '" failure_guard="0==1" name="NARX' + str(grid_size - 1) + '" running_guard="0==1" success_guard="0==0" success_program="gx=' + str(grid_size - 1) + '"/>' + os.linesep
        + indent(6) + '</Fallback>' + os.linesep
        + indent(6) + '<Fallback name="RY">' + os.linesep
        + ''.join([
            (indent(8) + '<Action ID="IARY' + str(y_val) + '" failure_guard="0==0" name="NARY' + str(y_val) + '" running_guard="0==1" success_guard="0==0" success_program="gy=' + str(y_val) + '"/>' + os.linesep)
            for y_val in range(grid_size - 1)
        ])
        + indent(7) + '<Action ID="IARY' + str(grid_size - 1) + '" failure_guard="0==1" name="NARY' + str(grid_size - 1) + '" running_guard="0==1" success_guard="0==0" success_program="gy=' + str(grid_size - 1) + '"/>' + os.linesep
        + indent(6) + '</Fallback>' + os.linesep
        + indent(5) + '</Sequence>' + os.linesep
        + indent(4) + '</Fallback>' + os.linesep
        + indent(4) + '<Fallback name="MR">' + os.linesep
        + indent(5) + '<Sequence name="TR">' + os.linesep
        + indent(6) + '<Condition ID="IXS" failure_guard="dx&gt;=gx" name="NXS" success_guard="dx&lt;gx"/>' + os.linesep
        + indent(6) + '<Action ID="IGR" failure_guard="0==1" name="NGR" running_guard="0==1" success_guard="0==0" success_program="dx=dx+1"/>' + os.linesep
        + indent(5) + '</Sequence>' + os.linesep
        + indent(5) + '<Sequence name="TL">' + os.linesep
        + indent(6) + '<Condition ID="IXB" failure_guard="dx&lt;=gx" name="NXB" success_guard="dx&gt;gx"/>' + os.linesep
        + indent(6) + '<Action ID="IGL" failure_guard="0==1" name="NGL" running_guard="0==1" success_guard="0==0" success_program="dx=dx-1"/>' + os.linesep
        + indent(5) + '</Sequence>' + os.linesep
        + indent(5) + '<Sequence name="TU">' + os.linesep
        + indent(6) + '<Condition ID="IYS" failure_guard="dy&gt;=gy" name="NXS" success_guard="dy&lt;gy"/>' + os.linesep
        + indent(6) + '<Action ID="IGU" failure_guard="0==1" name="NGU" running_guard="0==1" success_guard="0==0" success_program="dy=dy+1"/>' + os.linesep
        + indent(5) + '</Sequence>' + os.linesep
        + indent(5) + '<Sequence name="TD">' + os.linesep
        + indent(6) + '<Condition ID="IYB" failure_guard="dy&lt;=gy" name="NYB" success_guard="dy&gt;gy"/>' + os.linesep
        + indent(6) + '<Action ID="IGD" failure_guard="0==1" name="NGD" running_guard="0==1" success_guard="0==0" success_program="dy=dy-1"/>' + os.linesep
        + indent(5) + '</Sequence>' + os.linesep
        + indent(4) + '</Fallback>' + os.linesep
        + indent(3) + '</Sequence>' + os.linesep
        + indent(2) + '</Fallback>' + os.linesep
        + indent(1) + '</BehaviorTree>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + indent(1) + '<TreeNodesModel>' + os.linesep
        + ''.join([
            (
                indent(2) + '<Condition ID="' + condition_id + '">' + os.linesep
                + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
                + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
                + indent(2) + '</Condition>' + os.linesep
            )
            for condition_id in condition_ids
        ])
        + ''.join([
            (
                indent(2) + '<Action ID="' + action_id + '">' + os.linesep
                + indent(3) + '<inout_port name="success_guard"/>' + os.linesep
                + indent(3) + '<inout_port name="success_program"/>' + os.linesep
                + indent(3) + '<inout_port name="failure_guard"/>' + os.linesep
                + indent(3) + '<inout_port name="running_guard"/>' + os.linesep
                + indent(2) + '</Action>' + os.linesep
            )
            for action_id in action_ids
        ])
        + indent(1) + '</TreeNodesModel>' + os.linesep
        + indent(1) + '<!-- ////////// -->' + os.linesep
        + '</root>' + os.linesep
    )


def write_files(location, min_val, max_val, step_size):
    for x in range(min_val, max_val + 1, step_size):
        with open(location + '/' + 'MoVe4BT_simple_robot_' + str(x) + '.xml', 'w') as f:
            f.write(create_simple_robot(x))


write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
