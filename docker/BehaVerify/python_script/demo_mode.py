import os
import sys
import argparse
import docker
from docker_util import copy_into, copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, USER_DIR, BEHAVERIFY_VENV, RESULTS_VENV
from generate import move_files, generate, evaluate


def demo_mode(demo, output_path, additional_input):
    if os.path.exists(output_path):
        raise ValueError('Output Path exists.')
    if not os.path.isdir(os.path.split(output_path)[0]):
        raise ValueError('Output Path is in a directory that does not exist.')
    current_demos = {'grid_net', 'moving_target'}
    uses_networks = {'grid_net', 'moving_target'}
    if demo not in current_demos:
        raise ValueError('Unknown demo: ' + demo + '. Current demos are: ' + str(current_demos) + '.')
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    to_generate = ''
    flags = ''
    command = ''
    ansr_x_size = 0
    ansr_y_size = 0
    if demo in ('grid_net',):
        to_generate = 'nuXmv'
        flags = ''
        command = 'ctl'
    elif demo in ('moving_target'):
        to_generate = 'nuXmv'
        flags = ''
        command = 'ctl'
        ansr_x_size = 11
        ansr_y_size = 11
        if additional_input != '':
            serene_exec(behaverify, ' '.join([
                BEHAVERIFY_VENV,
                HOME_DIR + '/behaverify/demos/' + demo + '/edit_constants.py',
                USER_DIR + '/' + demo + '/' + demo + '.tree',
                '\'' + additional_input + '\'']), 'Modifying constants for ' + demo + '.', True)
            try:
                ansr_vals = [0, 0, 0, 0]
                for (index, ansr_code) in enumerate(('x_min', 'x_max', 'y_min', 'y_max')):
                    val = additional_input.split(ansr_code)[1]
                    val = val.split(',')[0]
                    val = val.replace(':=', '')
                    ansr_vals[index] = int(val.strip())
                ansr_x_size = (ansr_vals[1] - ansr_vals[0]) + 1
                ansr_y_size = (ansr_vals[3] - ansr_vals[2]) + 1
            except:
                pass
    move_files(behaverify, demo, 'yes' if demo in uses_networks else '-', True)
    generate(behaverify, demo + '.tree', demo, to_generate, flags)
    if command != 'generate':
        evaluate(behaverify, demo, to_generate, command)
    ##### SPECIAL ZONE
    special_command = None
    if demo == 'moving_target':
        special_command = ' '.join([
            RESULTS_VENV,
            HOME_DIR + '/behaverify/demos/moving_target/parse_nuxmv_output.py',
            USER_DIR + '/' + demo + '/output/nuxmv_ctl_results.txt',
            USER_DIR + '/' + demo + '/output/' + demo,
            str(ansr_x_size),
            str(ansr_y_size)
        ])
    if special_command is not None:
        serene_exec(behaverify, special_command, 'Execution of extra commands necessary for Demo.', True)
    ##### END SPECIAL ZONE
    print('Start: Copy output to source.')
    copy_out_of(behaverify, USER_DIR + '/' + demo, output_path + '.tar')
    print('End: Copy output to source.')
    behaverify.stop()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('demo')
    arg_parser.add_argument('output_path')
    arg_parser.add_argument('--additional_input', default = '')
    args = arg_parser.parse_args()
    demo_mode(args.demo.lower(), args.output_path, args.additional_input)
