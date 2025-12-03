#!/usr/bin/env python3
"""
Run BehaVerify on a local .tree file using the Docker container.

Usage:
    python run_behaverify.py input.tree                    # Generate .smv file
    python run_behaverify.py input.tree --verify           # Generate and verify with nuXmv
    python run_behaverify.py input.tree -o ./my_output     # Custom output directory
    python run_behaverify.py input.tree --verify --ctl     # Run CTL verification
    python run_behaverify.py input.tree --verify --ltl     # Run LTL verification
    python run_behaverify.py input.tree --verify --invar   # Run INVAR verification

This script:
1. Copies your .tree file into the Docker container
2. Runs BehaVerify to generate nuXmv model (.smv file)
3. Optionally runs nuXmv verification
4. Copies all results back to your local machine
"""
import argparse
import os
import sys
import tarfile
import tempfile
import shutil

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from docker_util import CONTAINER_NAME, TEST_DIR, BEHAVERIFY_VENV, copy_into, copy_out_of
import docker


def run_behaverify(input_file, output_dir, verify=False, ctl=False, ltl=False, invar=False,
                   keep_last_stage=False, do_not_trim=False, behave_only=False,
                   recursion_limit=10000):
    """
    Run BehaVerify on a .tree file and optionally verify with nuXmv.

    Args:
        input_file: Path to .tree file on host
        output_dir: Directory to store results on host
        verify: Whether to run nuXmv verification
        ctl: Run CTL specification check
        ltl: Run LTL specification check
        invar: Run INVAR specification check
        keep_last_stage: Keep last stage optimization
        do_not_trim: Do not trim the model
        behave_only: Behavior only mode
        recursion_limit: Python recursion limit for large trees
    """
    client = docker.from_env()

    # Get container
    try:
        container = client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        print(f'Error: Container "{CONTAINER_NAME}" not found.')
        print('Run setup.py first to create the container.')
        return False

    # Start container if not running
    if container.status != 'running':
        print('Starting container...')
        container.start()

    # Validate input file
    if not os.path.exists(input_file):
        print(f'Error: Input file not found: {input_file}')
        return False

    if not input_file.endswith('.tree'):
        print(f'Warning: Input file does not have .tree extension: {input_file}')

    # Get base name for output files
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Paths inside container
    container_work_dir = '/tmp/behaverify_work'
    container_input = f'{container_work_dir}/{os.path.basename(input_file)}'
    container_output = f'{container_work_dir}/{base_name}.smv'
    metamodel_path = f'{TEST_DIR}/metamodel/behaverify.tx'

    print(f'Input file: {input_file}')
    print(f'Output directory: {output_dir}')
    print()

    # Create work directory in container
    print('Setting up container workspace...')
    container.exec_run(f'mkdir -p {container_work_dir}')

    # Copy input file to container
    print(f'Copying {os.path.basename(input_file)} to container...')
    if not copy_into(container, input_file, container_work_dir + '/'):
        print('Error: Failed to copy input file to container')
        return False

    # Build command
    cmd_parts = [
        BEHAVERIFY_VENV,
        f'{TEST_DIR}/src/dsl_to_nuxmv.py',
        metamodel_path,
        container_input,
        container_output,
        f'--recursion_limit {recursion_limit}'
    ]

    if keep_last_stage:
        cmd_parts.append('--keep_last_stage')
    if do_not_trim:
        cmd_parts.append('--do_not_trim')
    if behave_only:
        cmd_parts.append('--behave_only')

    cmd = ' '.join(cmd_parts)

    # Run BehaVerify
    print('Running BehaVerify...')
    print(f'  Command: {cmd}')
    print()

    exit_code, output = container.exec_run(cmd, demux=True)
    stdout, stderr = output if output else (b'', b'')

    if stdout:
        print(stdout.decode())
    if stderr:
        stderr_text = stderr.decode()
        # Filter out onnxruntime warnings
        for line in stderr_text.split('\n'):
            if 'onnxruntime' not in line and line.strip():
                print(f'stderr: {line}')

    if exit_code != 0:
        print(f'Error: BehaVerify failed with exit code {exit_code}')
        return False

    print('BehaVerify completed successfully.')

    # Run nuXmv verification if requested
    if verify:
        nuxmv_path = f'{TEST_DIR}/nuXmv'

        # Determine which verification to run
        if not (ctl or ltl or invar):
            # Default: run all available
            ctl = ltl = invar = True

        verification_commands = []
        if ctl:
            verification_commands.append(('CTL', 'check_ctlspec'))
        if ltl:
            verification_commands.append(('LTL', 'check_ltlspec'))
        if invar:
            verification_commands.append(('INVAR', 'check_invar'))

        for spec_type, check_cmd in verification_commands:
            print()
            print(f'Running nuXmv {spec_type} verification...')

            # Create nuXmv command file
            nuxmv_cmds = f'read_model -i {container_output}\ngo\n{check_cmd}\nquit\n'
            cmd_file = f'{container_work_dir}/nuxmv_cmd_{spec_type.lower()}'
            container.exec_run(f'bash -c "echo \'{nuxmv_cmds}\' > {cmd_file}"')

            # Run nuXmv
            result_file = f'{container_work_dir}/{base_name}_{spec_type}.txt'
            nuxmv_cmd = f'{nuxmv_path} -source {cmd_file} > {result_file} 2>&1'
            exit_code, _ = container.exec_run(f'bash -c "{nuxmv_cmd}"')

            # Read and display results
            _, result_output = container.exec_run(f'cat {result_file}')
            if result_output:
                result_text = result_output.decode()
                print(f'  {spec_type} Results:')
                # Show relevant lines
                for line in result_text.split('\n'):
                    if 'specification' in line.lower() or 'true' in line.lower() or 'false' in line.lower():
                        print(f'    {line}')

    # Copy results back to host
    print()
    print('Copying results to host...')

    # Create tar of work directory
    tar_path = os.path.join(output_dir, 'results.tar')
    copy_out_of(container, container_work_dir, tar_path)

    # Extract tar
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(output_dir, filter='data')

    # Move files from extracted subdirectory to output_dir
    extracted_dir = os.path.join(output_dir, 'behaverify_work')
    if os.path.exists(extracted_dir):
        for f in os.listdir(extracted_dir):
            src = os.path.join(extracted_dir, f)
            dst = os.path.join(output_dir, f)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
        os.rmdir(extracted_dir)

    # Clean up tar file
    os.remove(tar_path)

    # Clean up container work directory
    container.exec_run(f'rm -rf {container_work_dir}')

    # List output files
    print()
    print('Output files:')
    for f in sorted(os.listdir(output_dir)):
        fpath = os.path.join(output_dir, f)
        size = os.path.getsize(fpath)
        print(f'  {f} ({size} bytes)')

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Run BehaVerify on a .tree file using Docker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Generate .smv file only
    python run_behaverify.py my_tree.tree

    # Generate and verify with nuXmv (all specs)
    python run_behaverify.py my_tree.tree --verify

    # Run specific verification
    python run_behaverify.py my_tree.tree --verify --ctl
    python run_behaverify.py my_tree.tree --verify --ltl
    python run_behaverify.py my_tree.tree --verify --invar

    # Custom output directory
    python run_behaverify.py my_tree.tree -o ./results --verify
'''
    )
    parser.add_argument('input_file', help='Path to .tree file')
    parser.add_argument('-o', '--output', default=None,
                        help='Output directory (default: same as input file)')
    parser.add_argument('--verify', action='store_true',
                        help='Run nuXmv verification after generating .smv')
    parser.add_argument('--ctl', action='store_true',
                        help='Run CTL specification check')
    parser.add_argument('--ltl', action='store_true',
                        help='Run LTL specification check')
    parser.add_argument('--invar', action='store_true',
                        help='Run INVAR specification check')
    parser.add_argument('--keep-last-stage', action='store_true',
                        help='Keep last stage optimization')
    parser.add_argument('--do-not-trim', action='store_true',
                        help='Do not trim the model')
    parser.add_argument('--behave-only', action='store_true',
                        help='Behavior only mode')
    parser.add_argument('--recursion-limit', type=int, default=10000,
                        help='Python recursion limit for large trees (default: 10000)')

    args = parser.parse_args()

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        # Default: create output directory next to input file
        input_dir = os.path.dirname(os.path.abspath(args.input_file))
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_dir = os.path.join(input_dir, f'{base_name}_output')

    # Make output_dir absolute
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)

    print('='*60)
    print('BehaVerify - Run via Docker')
    print('='*60)

    success = run_behaverify(
        args.input_file,
        output_dir,
        verify=args.verify,
        ctl=args.ctl,
        ltl=args.ltl,
        invar=args.invar,
        keep_last_stage=args.keep_last_stage,
        do_not_trim=args.do_not_trim,
        behave_only=args.behave_only,
        recursion_limit=args.recursion_limit
    )

    if success:
        print()
        print('='*60)
        print('Done!')
        print(f'Results saved to: {output_dir}')
        print('='*60)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
