#!/usr/bin/env python3
"""
Simple reproduction script for FM 2026 experiments.

Usage:
    python reproduce.py                  # Run experiments, output to ./results/
    python reproduce.py ./MyOutput       # Run experiments, output to specified directory
    python reproduce.py --extract-only   # Only extract results (don't re-run tests)

This script:
1. Runs all FM 2026 experiments inside the Docker container
2. Extracts results to the specified output directory
"""
import argparse
import os
import sys
import tarfile

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from docker_util import CONTAINER_NAME, TEST_DIR, USER, BEHAVERIFY_VENV, RESULTS_VENV, serene_exec, copy_out_of
import docker


def extract_results(output_dir):
    """Extract results from the container without running tests."""
    client = docker.from_env()

    try:
        container = client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        print(f'Error: Container "{CONTAINER_NAME}" not found.')
        print('Run setup.py first to create the container.')
        return False

    os.makedirs(output_dir, exist_ok=True)
    source_path = TEST_DIR + '/examples'
    tar_path = os.path.join(output_dir, 'examples.tar')

    print(f'Extracting results from container...')
    print(f'  Source: {source_path}')
    print(f'  Destination: {output_dir}')

    try:
        (bits, _) = container.get_archive(source_path)
        with open(tar_path, 'wb') as tar_file:
            for chunk in bits:
                tar_file.write(chunk)
    except docker.errors.NotFound:
        print(f'Error: No results found in container.')
        print('Run the experiments first (without --extract-only).')
        return False

    # Extract and cleanup
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(output_dir, filter='data')
    os.remove(tar_path)

    print(f'Results extracted to: {output_dir}/examples/')
    return True


def run_experiments(output_dir):
    """Run all experiments and extract results."""
    client = docker.from_env()

    try:
        container = client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        print(f'Error: Container "{CONTAINER_NAME}" not found.')
        print('Run setup.py first to create the container.')
        sys.exit(1)

    print('Starting container...')
    container.start()

    print('Running FM 2026 experiments...')
    print('(This may take 30-60 minutes depending on your system)')
    print()

    command = f'{TEST_DIR}/{USER}.sh {TEST_DIR} {BEHAVERIFY_VENV} {RESULTS_VENV}'
    serene_exec(container, command, 'FM 2026 Experiments', True)

    # Extract results
    print()
    print('Extracting results...')

    os.makedirs(output_dir, exist_ok=True)
    tar_path = output_dir + '.tar'
    copy_out_of(container, TEST_DIR + '/examples', tar_path)

    # Extract the tar file
    print(f'Extracting results to: {output_dir}/')
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(output_dir, filter='data')

    # Clean up tar file
    if os.path.exists(tar_path):
        os.remove(tar_path)

    # List key output files
    print()
    print('Key output files:')
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            if f.endswith('.png') or f.endswith('.pdf'):
                rel_path = os.path.relpath(os.path.join(root, f), output_dir)
                print(f'  {rel_path}')

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Run FM 2026 reproducibility experiments',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python reproduce.py                  # Run experiments, output to ./results/
    python reproduce.py ./MyOutput       # Run experiments, output to ./MyOutput/
    python reproduce.py --extract-only   # Only extract existing results
'''
    )
    parser.add_argument('output_dir', nargs='?', default='./results',
                        help='Output directory for results (default: ./results)')
    parser.add_argument('--extract-only', action='store_true',
                        help='Only extract results without running experiments')
    args = parser.parse_args()

    # Resolve output directory relative to REPRODUCIBILITY/2026_FM/
    base_dir = os.path.dirname(script_dir)
    if not os.path.isabs(args.output_dir):
        output_dir = os.path.join(base_dir, args.output_dir)
    else:
        output_dir = args.output_dir

    print('='*60)
    print('BehaVerify FM 2026 - Reproduce Experiments')
    print('='*60)
    print(f'Output directory: {output_dir}')
    print()

    if args.extract_only:
        success = extract_results(output_dir)
    else:
        success = run_experiments(output_dir)

    if success:
        print()
        print('='*60)
        print('Done!')
        print()
        print(f'Results are in: {output_dir}/examples/')
        print()
        print('Key directories:')
        print('  examples/MoVe4BT/       - Binary tree benchmarks')
        print('  examples/BT2BIP/        - MarsRover, TrainControl comparisons')
        print('  examples/BT2Fiacre/     - Drone3 comparisons')
        print('  examples/NetworkExample/- Neural network examples')
        print('='*60)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
