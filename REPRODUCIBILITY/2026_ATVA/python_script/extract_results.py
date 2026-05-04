"""
Extract results from a running or stopped BehaVerify Docker container.

Usage:
    python extract_results.py [output_directory]

If output_directory is not specified, defaults to ./results/
"""
import sys
import os
import tarfile
import io
import docker
from docker_util import CONTAINER_NAME, TEST_DIR

def extract_results(output_dir='./results'):
    """Extract the examples folder (containing all results) from the container."""
    client = docker.from_env()

    try:
        container = client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        print(f'Error: Container "{CONTAINER_NAME}" not found.')
        print('Make sure you have created the container using install.py first.')
        return False

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    source_path = TEST_DIR + '/examples'
    tar_path = os.path.join(output_dir, 'examples.tar')

    print(f'Extracting results from container "{CONTAINER_NAME}"...')
    print(f'  Source: {source_path}')
    print(f'  Destination: {output_dir}')

    # Get archive from container
    try:
        (bits, _) = container.get_archive(source_path)
        with open(tar_path, 'wb') as tar_file:
            for chunk in bits:
                tar_file.write(chunk)
        print(f'  Downloaded archive to: {tar_path}')
    except docker.errors.NotFound:
        print(f'Error: Path "{source_path}" not found in container.')
        print('Make sure you have run the reproducibility tests first.')
        return False

    # Extract the tar file
    print(f'  Extracting archive...')
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(output_dir, filter='data')

    # Clean up tar file
    os.remove(tar_path)

    print(f'Results extracted successfully to: {output_dir}/examples/')
    print('')
    print('Key result files:')

    # List key result files
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            if f.endswith('.png') or f.endswith('.pdf'):
                rel_path = os.path.relpath(os.path.join(root, f), output_dir)
                print(f'  {rel_path}')

    return True

if __name__ == '__main__':
    output_dir = sys.argv[1] if len(sys.argv) > 1 else './results'
    success = extract_results(output_dir)
    sys.exit(0 if success else 1)
