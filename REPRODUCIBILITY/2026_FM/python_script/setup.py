#!/usr/bin/env python3
"""
Simple setup script for FM 2026 reproducibility.

Usage:
    python setup.py                          # Download nuXmv automatically
    python setup.py --nuxmv path/to/nuXmv    # Use local nuXmv file
    python setup.py --nuxmv-url URL          # Download from custom URL

This script:
1. Builds the Docker image (behaverify_2026_fm_img)
2. Creates the Docker container (behaverify_2026_fm)
3. Installs nuXmv inside the container
"""
import argparse
import os
import sys

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from reinstall import reinstall

# Default nuXmv download URL
DEFAULT_NUXMV_URL = 'https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz'

def main():
    parser = argparse.ArgumentParser(
        description='Set up BehaVerify Docker environment for FM 2026 reproducibility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python setup.py                          # Download nuXmv automatically
    python setup.py --nuxmv ./nuXmv          # Use local nuXmv binary
    python setup.py --nuxmv-url "https://..."  # Download from custom URL
'''
    )
    parser.add_argument('--nuxmv', type=str, default=None,
                        help='Path to local nuXmv binary (optional)')
    parser.add_argument('--nuxmv-url', type=str, default=DEFAULT_NUXMV_URL,
                        help='URL to download nuXmv from (default: official nuXmv site)')
    parser.add_argument('--skip-nuxmv', action='store_true',
                        help='Skip nuXmv installation (container can still generate .smv files)')
    args = parser.parse_args()

    # Determine dockerfile path (parent of python_script directory)
    dockerfile_path = os.path.dirname(script_dir)

    print('='*60)
    print('BehaVerify FM 2026 - Docker Setup')
    print('='*60)
    print(f'Dockerfile location: {dockerfile_path}')

    if args.skip_nuxmv:
        print('nuXmv: SKIPPED (container will not run verification)')
        nuxmv_loc = None
        local = False
    elif args.nuxmv:
        if not os.path.exists(args.nuxmv):
            print(f'Error: nuXmv file not found at: {args.nuxmv}')
            sys.exit(1)
        print(f'nuXmv: Local file ({args.nuxmv})')
        nuxmv_loc = args.nuxmv
        local = True
    else:
        print(f'nuXmv: Will download from URL')
        print(f'  URL: {args.nuxmv_url}')
        nuxmv_loc = args.nuxmv_url
        local = False

    print('='*60)
    print()

    try:
        reinstall(dockerfile_path, nuxmv_loc, local)
        print()
        print('='*60)
        print('Setup completed successfully!')
        print()
        print('Next step: Run the experiments with:')
        print('    python python_script/reproduce.py')
        print('='*60)
    except Exception as e:
        print(f'Error during setup: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
