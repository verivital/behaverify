'''
This file is used as the main entry point for BehaVerify.
It can be used to call the various modes of BehaVerify. If nuXmv has been downloaded, it can also envoke nuXmv.
For usage details, please consult: https://github.com/verivital/behaverify/blob/main/README.md
For instructions on how to create a new model, please consult: https://github.com/verivital/behaverify/blob/main/tutorial_examples/README.md

Original Author: Serena Serafina Serbinowska, serena.serbinowska@vanderbilt.edu
Current Maintainer:
'''
import argparse
import os
import re
import subprocess
import sys
from importlib.resources import files

from behaverify.dsl_to_cpp import dsl_to_cpp
from behaverify.dsl_to_haskell import dsl_to_haskell
from behaverify.dsl_to_latex import dsl_to_latex
from behaverify.dsl_to_nuxmv import dsl_to_nuxmv
from behaverify.dsl_to_python import dsl_to_python
from behaverify.counter_trace import counter_trace
from behaverify.grid_world_draw.parse_nuxmv_output import handle_file as grid_world_draw_nuxmv_output
from behaverify.grid_world_draw.parse_python_output import handle_file as grid_world_draw_python_output
from behaverify.behaverify_gui import main as gui_main

__version__ = '0.0.1'


def error_exit(message, suggestion=None):
    """Print error message and exit gracefully without a stack trace."""
    print(f"\nError: {message}", file=sys.stderr)
    if suggestion:
        print(f"Suggestion: {suggestion}", file=sys.stderr)
    sys.exit(1)


def verify_location(directory_mode, current_location, overwrite):
    """
    Verify and create output location for generated files.

    Args:
        directory_mode: If None or False, current_location is a single file.
                       Otherwise, it's the directory name to create inside current_location.
        current_location: The output location (file path or parent directory).
        overwrite: Whether to allow overwriting existing files/directories.

    Raises:
        FileExistsError: If the output location exists and overwrite is False,
                        or if parent directory is not a directory.
    """
    if directory_mode is None or (not directory_mode):
        if os.path.exists(current_location) and not overwrite:
            error_exit(
                f"Output file already exists: {current_location}",
                "Use --overwrite to replace existing files, or choose a different output location."
            )
        if os.path.exists(os.path.dirname(current_location)) and not os.path.isdir(os.path.dirname(current_location)):
            error_exit(
                f"Parent path is not a directory: {os.path.dirname(current_location)}",
                "Ensure the parent path is a valid directory."
            )
        if os.path.dirname(current_location) and not os.path.isdir(os.path.dirname(current_location)):
            os.makedirs(os.path.dirname(current_location))
        return
    if os.path.exists(current_location) and not os.path.isdir(current_location):
        error_exit(
            f"Output location exists but is not a directory: {current_location}",
            "Provide a directory path, or remove the existing file."
        )
    output_path = os.path.join(current_location, directory_mode)
    if os.path.exists(output_path) and not overwrite:
        error_exit(
            f"Output directory already exists: {output_path}",
            "Use --overwrite to replace existing files, or choose a different output location."
        )
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def verify_input(current_input):
    """
    Verify that input file exists and is a file.

    Args:
        current_input: Path to the input file.

    Raises:
        FileNotFoundError: If the input file doesn't exist or is not a file.
    """
    if os.path.isdir(current_input):
        error_exit(
            f"Input path is a directory, not a file: {current_input}",
            "Provide a path to a .tree file, not a directory."
        )
    if not os.path.exists(current_input):
        # Check for similar files to help with typos
        parent_dir = os.path.dirname(current_input) or '.'
        base_name = os.path.basename(current_input)
        suggestion = "Check that the file path is correct and the file exists."
        if os.path.isdir(parent_dir) and base_name:
            try:
                dir_files = os.listdir(parent_dir)
                # Look for files with similar names or same extension
                similar = []
                base_no_ext = os.path.splitext(base_name)[0]
                for f in dir_files:
                    if f.endswith('.tree') or f.startswith(base_no_ext[:3] if len(base_no_ext) >= 3 else base_no_ext):
                        similar.append(f)
                if similar:
                    suggestion = f"Did you mean one of these? {', '.join(similar[:5])}"
            except OSError:
                pass  # If we can't list the directory, just use the default suggestion
        error_exit(f"Input file not found: {current_input}", suggestion)
    if not os.path.isfile(current_input):
        error_exit(
            f"Input path exists but is not a regular file: {current_input}",
            "Provide a path to a regular .tree file."
        )
    return


def get_metamodel_file():
    """
    Get the path to the metamodel file.

    Returns:
        Path to the behaverify.tx metamodel file.
    """
    try:
        return files('behaverify').joinpath('data', 'metamodel', 'behaverify.tx')
    except ModuleNotFoundError:
        metamodel_file = os.path.dirname(os.path.realpath(__file__)) + '/data/metamodel/behaverify.tx'
        print('did not find module; attempted to find files directly')
        return metamodel_file


def verify_nuxmv_path(nuxmv_path):
    """
    Verify that the nuXmv executable exists and is runnable.

    Args:
        nuxmv_path: Path to the nuXmv executable.

    Returns:
        Absolute path to the nuXmv executable.
    """
    if nuxmv_path is None:
        error_exit(
            "nuXmv path not specified but required for verification/simulation.",
            "Use --nuxmv_path to specify the path to the nuXmv executable. "
            "Download nuXmv from https://nuxmv.fbk.eu/"
        )

    # Convert to absolute path to ensure subprocess.run can find the executable
    # (relative paths like './nuXmv' become 'nuXmv' with normpath, which fails on Linux)
    nuxmv_path = os.path.abspath(nuxmv_path)

    # Check if file exists
    if not os.path.exists(nuxmv_path):
        # Check common locations
        common_paths = [
            '../nuXmv', '../nuXmv.exe',
            'nuXmv', 'nuXmv.exe',
            os.path.expanduser('~/nuXmv'),
        ]
        existing = [p for p in common_paths if os.path.exists(p)]
        if existing:
            error_exit(
                f"nuXmv executable not found: {nuxmv_path}",
                f"Found nuXmv at: {existing[0]}. Use --nuxmv_path {existing[0]}"
            )
        error_exit(
            f"nuXmv executable not found: {nuxmv_path}",
            "Download nuXmv from https://nuxmv.fbk.eu/ and specify the correct path with --nuxmv_path"
        )

    if not os.path.isfile(nuxmv_path):
        error_exit(
            f"nuXmv path is not a file: {nuxmv_path}",
            "Provide the path to the nuXmv executable file, not a directory."
        )

    # Check if executable (Unix only - Windows doesn't use execute bit)
    if os.name != 'nt' and not os.access(nuxmv_path, os.X_OK):
        error_exit(
            f"nuXmv file is not executable: {nuxmv_path}",
            f"Run: chmod +x {nuxmv_path}"
        )

    return nuxmv_path


def extract_brace_content(text, start_pos):
    """
    Extract content between matching braces starting from start_pos.
    Returns (content, end_pos) or (None, -1) if no match found.
    """
    if start_pos >= len(text) or text[start_pos] != '{':
        return None, -1

    depth = 1
    pos = start_pos + 1
    while pos < len(text) and depth > 0:
        if text[pos] == '{':
            depth += 1
        elif text[pos] == '}':
            depth -= 1
        pos += 1

    if depth == 0:
        return text[start_pos + 1:pos - 1], pos
    return None, -1


def parse_dsl_specifications(model_file):
    """
    Parse BehaVerify DSL specifications from a .tree file.

    Uses brace-matching to properly handle nested braces in specifications.

    Args:
        model_file: Path to the .tree file.

    Returns:
        List of tuples: (spec_type, spec_text)
    """
    specs = []
    try:
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the specifications block using brace matching
        spec_start = content.find('specifications')
        if spec_start == -1:
            return specs

        # Find the opening brace after 'specifications'
        brace_pos = content.find('{', spec_start)
        if brace_pos == -1:
            return specs

        spec_block, _ = extract_brace_content(content, brace_pos)
        if spec_block is None:
            return specs

        # Find individual specifications using brace matching, preserving order
        spec_types = ('INVARSPEC', 'CTLSPEC', 'LTLSPEC')
        pos = 0
        while pos < len(spec_block):
            # Find the next spec type
            next_type = None
            next_pos = len(spec_block)
            for stype in spec_types:
                type_pos = spec_block.find(stype, pos)
                if type_pos != -1 and type_pos < next_pos:
                    next_pos = type_pos
                    next_type = stype

            if next_type is None:
                break

            # Find the opening brace for this spec
            brace_start = spec_block.find('{', next_pos)
            if brace_start == -1:
                break

            spec_content, end_pos = extract_brace_content(spec_block, brace_start)
            if spec_content is not None:
                specs.append((next_type, spec_content.strip()))
                pos = end_pos
            else:
                pos = next_pos + len(next_type)

    except OSError:
        pass  # If we can't read the file, return empty specs

    return specs


def parse_nuxmv_results(output_file):
    """
    Parse nuXmv output file and extract verification results.

    Args:
        output_file: Path to nuXmv output file.

    Returns:
        List of tuples: (spec_type, spec_text, result, has_counterexample)
    """
    results = []
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match specification results
        # Example: "-- specification AG (EF (...))  is true"
        # Example: "-- specification G (x > 0)  is false"
        spec_pattern = re.compile(
            r'-- specification\s+(.+?)\s+is\s+(true|false)',
            re.IGNORECASE
        )

        for match in spec_pattern.finditer(content):
            spec_text = match.group(1).strip()
            result = match.group(2).lower() == 'true'

            # Determine spec type from the specification text
            spec_type = 'SPEC'
            spec_upper = spec_text.upper()
            if spec_upper.startswith('AG') or spec_upper.startswith('AF') or \
               spec_upper.startswith('EG') or spec_upper.startswith('EF') or \
               spec_upper.startswith('A [') or spec_upper.startswith('E ['):
                spec_type = 'CTLSPEC'
            elif spec_upper.startswith('G ') or spec_upper.startswith('F ') or \
                 spec_upper.startswith('X ') or spec_upper.startswith('U ') or \
                 ' U ' in spec_upper:
                spec_type = 'LTLSPEC'
            else:
                spec_type = 'INVARSPEC'

            # Check if there's a counterexample following this spec
            has_counterexample = False
            match_end = match.end()
            remaining = content[match_end:match_end + 200]
            if 'as demonstrated by' in remaining.lower() or 'counterexample' in remaining.lower():
                has_counterexample = True

            results.append((spec_type, spec_text, result, has_counterexample))

    except OSError:
        pass  # If we can't read the file, return empty results

    return results


def print_verification_summary(output_file, model_file=None):
    """
    Print a summary of nuXmv verification results.

    Args:
        output_file: Path to nuXmv output file.
        model_file: Optional path to the original .tree file (for DSL specs).
    """
    results = parse_nuxmv_results(output_file)

    if not results:
        print("\nNo specification results found in output.")
        print(f"Check {output_file} for details.")
        return

    # Parse DSL specifications if model file provided
    dsl_specs = []
    if model_file and model_file.endswith('.tree'):
        dsl_specs = parse_dsl_specifications(model_file)

    # Count results
    passed = sum(1 for _, _, r, _ in results if r)
    failed = sum(1 for _, _, r, _ in results if not r)

    print("\n" + "=" * 70)
    print("VERIFICATION RESULTS")
    print("=" * 70)

    for i, (spec_type, spec_text, result, has_ce) in enumerate(results, 1):
        status = "PASS" if result else "FAIL"
        symbol = "[OK]" if result else "[X] "

        print(f"\n{symbol} {spec_type} #{i}: {status}")

        # Show DSL specification if available
        if i <= len(dsl_specs):
            dsl_type, dsl_text = dsl_specs[i - 1]
            print(f"     DSL:   {dsl_type} {{{dsl_text}}}")

        # Show full nuXmv specification
        print(f"     nuXmv: {spec_text}")

        if has_ce and not result:
            print("     (counter-example available in output file)")

    print("\n" + "-" * 70)
    print(f"Summary: {passed} passed, {failed} failed out of {len(results)} specifications")
    print(f"Full results: {output_file}")
    print("=" * 70)


def run_nuxmv(nuxmv_path, command_file, input_file, output_file, error_file):
    """
    Run nuXmv with proper error handling.

    Args:
        nuxmv_path: Path to nuXmv executable.
        command_file: Path to command script file.
        input_file: Path to input SMV file.
        output_file: Path for stdout output.
        error_file: Path for stderr output.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            with open(error_file, 'w', encoding='utf-8') as error_obj:
                subprocess.run(
                    [nuxmv_path, '-source', command_file, input_file],
                    check=True,
                    stdout=output_obj,
                    stderr=error_obj,
                    text=True,
                    timeout=600  # 10 minute timeout
                )
    except subprocess.TimeoutExpired:
        error_exit(
            "nuXmv verification timed out after 10 minutes.",
            "The model may be too complex. Try simplifying or reducing the state space."
        )
    except subprocess.CalledProcessError as e:
        # Read error file for details
        error_content = ""
        if os.path.exists(error_file):
            try:
                with open(error_file, 'r', encoding='utf-8') as f:
                    error_content = f.read().strip()
            except OSError:
                pass
        msg = f"nuXmv execution failed with exit code {e.returncode}."
        if error_content:
            msg += f"\nDetails: {error_content[:500]}"  # Limit error output
        error_exit(msg, f"Check {error_file} for full error details.")
    except FileNotFoundError:
        error_exit(
            f"nuXmv executable not found or not runnable: {nuxmv_path}",
            "Verify the nuXmv path is correct and the file has execute permissions."
        )
    except PermissionError:
        error_exit(
            f"Permission denied when running nuXmv: {nuxmv_path}",
            "Check file permissions and try running with appropriate privileges."
        )


def main(argv=None):
    """
    Main entry point for behaverify.

    Args:
        argv: Optional list of command-line arguments. If None, uses sys.argv.
              Allows programmatic invocation.

    Example programmatic usage:
        main(['nuxmv', 'model.tree', './output', '--generate'])
        main(['python', 'model.tree', './output'])
    """
    metamodel_file = get_metamodel_file()
    print(metamodel_file)

    # Main help text with mode descriptions
    main_help = '''BehaVerify: Formal verification tool for Behavior Trees

Available modes:
  cpp       Generate C++ implementation (BehaviorTree.CPP compatible)
  grid      Render grid-world traces as images
  gui       Launch graphical user interface
  haskell   Generate functional Haskell implementation
  latex     Generate TikZ diagram for behavior tree visualization
  nuxmv     Generate nuXmv model and run formal verification
  python    Generate executable Python implementation
  trace     Visualize nuXmv counter-example traces

Examples:
  behaverify nuxmv model.tree ./output --generate --ltl --nuxmv_path ../nuXmv
  behaverify python model.tree ./output
  behaverify latex model.tree ./output/diagram.tex
  behaverify nuxmv model.tree ./output --generate --invar --ctl --nuxmv_path ../nuXmv

Use "behaverify <mode> --help" for mode-specific options.
For detailed documentation: https://github.com/verivital/behaverify
'''

    # Determine which help to show:
    # - If no args or just --help/--version, show main help
    # - If valid mode with --help, let mode parser handle it
    effective_argv = argv if argv is not None else sys.argv[1:]
    valid_modes = ('cpp', 'grid', 'gui', 'haskell', 'latex', 'nuxmv', 'python', 'trace')

    # Check if we should show main help (no mode specified, or --help/--version before mode)
    show_main_help = (
        len(effective_argv) == 0 or
        effective_argv[0] in ('-h', '--help', '--version') or
        (len(effective_argv) >= 1 and effective_argv[0].lower() not in valid_modes)
    )

    if show_main_help:
        arg_parser = argparse.ArgumentParser(
            prog='behaverify',
            description='BehaVerify: Formal verification tool for Behavior Trees',
            epilog=main_help,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
        arg_parser.add_argument('mode',
            help='Operation mode (cpp, grid, gui, haskell, latex, nuxmv, python, trace)')
        args = arg_parser.parse_args(argv)
        # If we get here with an invalid mode, the unknown mode handler below will catch it

    # Simple mode detection without triggering help
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument('mode', nargs='?', default='')
    (args, _) = arg_parser.parse_known_args(argv)
    main_mode = args.mode.lower()
    if main_mode == 'cpp':
        arg_parser = argparse.ArgumentParser(
            prog='behaverify cpp',
            description='Generate C++ implementation from .tree specification (BehaviorTree.CPP compatible)',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('model_file', help='Input .tree file')
        arg_parser.add_argument('location', help='Output directory')
        arg_parser.add_argument('--output_name', type=str, default=None,
            help='Custom output filename (default: derived from input filename)')
        arg_parser.add_argument('--max_iter', type=int, default=100,
            help='Maximum iterations for execution (default: 100)')
        arg_parser.add_argument('--no_var_print', action='store_true',
            help='Suppress variable printing during execution')
        arg_parser.add_argument('--serene_print', action='store_true',
            help='Use reduced (serene) output mode')
        arg_parser.add_argument('--py_tree_print', action='store_true',
            help='Use py_trees format for output')
        arg_parser.add_argument('--recursion_limit', type=int, default=0,
            help='Increase Python recursion limit for complex models (default: 0 = no change)')
        arg_parser.add_argument('--safe_assignment', action='store_true',
            help='Use safe variable assignment mode')
        arg_parser.add_argument('--no_checks', action='store_true',
            help='Skip grammar validation (faster but risky)')
        arg_parser.add_argument('--overwrite', action='store_true',
            help='Overwrite existing output files/directories')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('cpp', args.location, args.overwrite)
        output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        dsl_to_cpp(metamodel_file, args.model_file, output_name, os.path.join(args.location, 'cpp'), args.serene_print, args.max_iter, args.no_var_print, args.py_tree_print, args.recursion_limit, args.safe_assignment, args.no_checks)
    elif main_mode == 'grid':
        arg_parser = argparse.ArgumentParser(
            prog='behaverify grid',
            description='Render grid-world traces as images',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('submode',
            help='Submode: nuxmv (render nuXmv traces), python (render Python traces), network (not implemented)')
        (args, _) = arg_parser.parse_known_args(argv)
        if args.submode.lower() == 'network':
            arg_parser = argparse.ArgumentParser(
                prog='behaverify grid network',
                description='Render network traces (NOT YET IMPLEMENTED)',
                formatter_class=argparse.RawDescriptionHelpFormatter
            )
            arg_parser.add_argument('mode', help=argparse.SUPPRESS)
            arg_parser.add_argument('submode', help=argparse.SUPPRESS)
            arg_parser.add_argument('model_file', help='Input .tree file')
            arg_parser.add_argument('trace_file', help='Input trace file')
            arg_parser.add_argument('location', help='Output directory')
            arg_parser.add_argument('name', help='Output name')
            arg_parser.add_argument('--do_not_trim', action='store_true',
                help='Disable node trimming optimization')
            arg_parser.add_argument('--recursion_limit', type=int, default=0,
                help='Increase Python recursion limit for complex models')
            raise NotImplementedError('Grid network mode is not yet implemented')
        elif args.submode.lower() == 'nuxmv':
            arg_parser = argparse.ArgumentParser(
                prog='behaverify grid nuxmv',
                description='Render grid-world traces from nuXmv output as images',
                formatter_class=argparse.RawDescriptionHelpFormatter
            )
            arg_parser.add_argument('mode', help=argparse.SUPPRESS)
            arg_parser.add_argument('submode', help=argparse.SUPPRESS)
            arg_parser.add_argument('trace_file', help='Input nuXmv trace file')
            arg_parser.add_argument('location', help='Output directory')
            arg_parser.add_argument('x_size', type=int, help='Grid width')
            arg_parser.add_argument('y_size', type=int, help='Grid height')
            arg_parser.add_argument('--stage', type=int, default=-1,
                help='Which stage to render (default: -1 = all stages)')
            arg_parser.add_argument('--overwrite', action='store_true',
                help='Overwrite existing output files/directories')
            args = arg_parser.parse_args(argv)
            verify_input(args.trace_file)
            verify_location('grid_nuxmv', args.location, args.overwrite)
            grid_world_draw_nuxmv_output(args.trace_file, os.path.join(args.location, 'grid_nuxmv', 'img'), args.x_size, args.y_size, args.stage)
        elif args.submode.lower() == 'python':
            arg_parser = argparse.ArgumentParser(
                prog='behaverify grid python',
                description='Render grid-world traces from Python output as images',
                formatter_class=argparse.RawDescriptionHelpFormatter
            )
            arg_parser.add_argument('mode', help=argparse.SUPPRESS)
            arg_parser.add_argument('submode', help=argparse.SUPPRESS)
            arg_parser.add_argument('trace_file', help='Input Python trace file')
            arg_parser.add_argument('location', help='Output directory')
            arg_parser.add_argument('x_size', type=int, help='Grid width')
            arg_parser.add_argument('y_size', type=int, help='Grid height')
            arg_parser.add_argument('--overwrite', action='store_true',
                help='Overwrite existing output files/directories')
            args = arg_parser.parse_args(argv)
            verify_input(args.trace_file)
            verify_location('grid_python', args.location, args.overwrite)
            grid_world_draw_python_output(args.trace_file, os.path.join(args.location, 'grid_python', 'img'), args.x_size, args.y_size)
        else:
            error_exit(
                f"Unknown grid submode: '{args.submode}'",
                "Available submodes: nuxmv, python"
            )
    elif main_mode == 'haskell':
        arg_parser = argparse.ArgumentParser(
            prog='behaverify haskell',
            description='Generate functional Haskell implementation from .tree specification',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('model_file', help='Input .tree file')
        arg_parser.add_argument('location', nargs='?', default='./',
            help='Output directory (default: ./)')
        arg_parser.add_argument('--output_name', type=str, default=None,
            help='Custom output filename (default: derived from input filename)')
        arg_parser.add_argument('--max_iter', type=int, default=100,
            help='Maximum iterations for execution (default: 100)')
        arg_parser.add_argument('--recursion_limit', type=int, default=0,
            help='Increase Python recursion limit for complex models (default: 0 = no change)')
        arg_parser.add_argument('--no_checks', action='store_true',
            help='Skip grammar validation (faster but risky)')
        arg_parser.add_argument('--overwrite', action='store_true',
            help='Overwrite existing output files/directories')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('haskell', args.location, args.overwrite)
        output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        dsl_to_haskell(metamodel_file, args.model_file, os.path.join(args.location, 'haskell'), output_name, args.max_iter, args.recursion_limit, args.no_checks)
    elif main_mode == 'latex':
        arg_parser = argparse.ArgumentParser(
            prog='behaverify latex',
            description='Generate TikZ diagram for behavior tree visualization',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('model_file', help='Input .tree file')
        arg_parser.add_argument('output_file', help='Output .tex file path')
        arg_parser.add_argument('--insert_only', action='store_true',
            help='Generate only TikZ block (not full LaTeX document)')
        arg_parser.add_argument('--recursion_limit', type=int, default=0,
            help='Increase Python recursion limit for complex models (default: 0 = no change)')
        arg_parser.add_argument('--on_sides', action='store_true',
            help='Place variable info on sides of the diagram')
        args = arg_parser.parse_args(argv)
        dsl_to_latex(metamodel_file, args.model_file, args.output_file, args.insert_only, args.recursion_limit, args.on_sides)
    elif main_mode == 'nuxmv':
        nuxmv_epilog = '''
Examples:
  # Generate SMV model only:
  behaverify nuxmv model.tree ./output --generate

  # Generate and verify with LTL:
  behaverify nuxmv model.tree ./output --generate --ltl --nuxmv_path ../nuXmv

  # Verify existing SMV file with invariants and CTL:
  behaverify nuxmv model.smv ./output --invar --ctl --nuxmv_path ../nuXmv

  # Generate and simulate for 10 steps:
  behaverify nuxmv model.tree ./output --generate --simulate 10 --nuxmv_path ../nuXmv
'''
        arg_parser = argparse.ArgumentParser(
            prog='behaverify nuxmv',
            description='Generate nuXmv SMV model and/or run formal verification',
            epilog=nuxmv_epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('model_file', help='Input .tree or .smv file')
        arg_parser.add_argument('location', nargs='?', default='./',
            help='Output directory (default: ./)')
        arg_parser.add_argument('--output_name', type=str, default=None,
            help='Custom output filename (default: derived from input filename)')
        arg_parser.add_argument('--out2', type=str, default=None, help=argparse.SUPPRESS)  # Deprecated
        arg_parser.add_argument('--generate', action='store_true',
            help='Generate nuXmv SMV model from .tree file')
        arg_parser.add_argument('--invar', action='store_true',
            help='Verify invariant (INVARSPEC) specifications')
        arg_parser.add_argument('--ctl', action='store_true',
            help='Verify CTL (CTLSPEC) specifications')
        arg_parser.add_argument('--ltl', action='store_true',
            help='Verify LTL (LTLSPEC) specifications')
        arg_parser.add_argument('--simulate', type=int, default=0, metavar='N',
            help='Simulate for N steps (default: 0 = no simulation)')
        arg_parser.add_argument('--nuxmv_path', type=str, default=None, metavar='PATH',
            help='Path to nuXmv executable (required for --invar/--ctl/--ltl/--simulate)')
        # arg_parser.add_argument('--keep_stage_0', action = 'store_true') # removed due to a bug.
        arg_parser.add_argument('--keep_last_stage', action='store_true',
            help='Disable variable stage optimization')
        arg_parser.add_argument('--do_not_trim', action='store_true',
            help='Disable node trimming optimization')
        arg_parser.add_argument('--behave_only', action='store_true',
            help='Generate behavior-only model')
        arg_parser.add_argument('--recursion_limit', type=int, default=0,
            help='Increase Python recursion limit for complex models (default: 0 = no change)')
        arg_parser.add_argument('--no_checks', action='store_true',
            help='Skip grammar validation (faster but risky)')
        arg_parser.add_argument('--record_times', type=str, default=None, metavar='FILE',
            help='Record execution times to file')
        arg_parser.add_argument('--use_encoding', type=str, default='fastforwarding',
            choices=['fastforwarding', 'naive'],
            help='Encoding type: fastforwarding (default) or naive')
        arg_parser.add_argument('--overwrite', action='store_true',
            help='Overwrite existing output files/directories')
        arg_parser.add_argument('-v', '--verbose', action='store_true',
            help='Print verification results summary to console')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('nuxmv', args.location, args.overwrite)
        input_file = args.model_file
        # output_file = set_output(args.location, input_file, args.output_name, extra_directory = 'nuxmv', extension = ('.smv' if args.generate else '.txt'))
        output_file = os.path.join(args.location, 'nuxmv', (args.output_name if args.output_name is not None else (os.path.splitext(os.path.basename(input_file))[0] + ('.smv' if args.generate else '.txt'))))
        if args.use_encoding.lower() not in ('fastforwarding', 'naive'):
            error_exit(
                f"Unknown encoding: {args.use_encoding.lower()}",
                "Encoding must be 'fastforwarding' or 'naive' (case insensitive)."
            )
        if args.generate:
            dsl_to_nuxmv(metamodel_file, args.model_file, output_file, True, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False, args.no_checks, args.record_times, args.use_encoding)
            input_file = output_file
            output_file = os.path.splitext(input_file)[0] + '_output.txt'
        if any((args.invar, args.ctl, args.ltl, args.simulate > 0)):
            nuxmv_path = verify_nuxmv_path(args.nuxmv_path)
            command_file = os.path.splitext(input_file)[0] + '_input.txt'
            error_file = os.path.splitext(input_file)[0] + '_error.txt'
            command_string = (
                'go' + os.linesep
                + (('check_invar' + os.linesep) if args.invar else '')
                + (('check_ctlspec' + os.linesep) if args.ctl else '')
                + (('check_ltlspec' + os.linesep) if args.ltl else '')
                + ('pick_state -r' + os.linesep + ('simulate -r -v -k ' + str(args.simulate) + os.linesep) if args.simulate > 0 else '')
                + 'quit' + os.linesep
            )
            with open(command_file, 'w', encoding = 'utf-8') as command_file_obj:
                command_file_obj.write(command_string)
            run_nuxmv(nuxmv_path, command_file, input_file, output_file, error_file)
            if args.verbose:
                print_verification_summary(output_file, args.model_file)
    elif main_mode == 'python':
        arg_parser = argparse.ArgumentParser(
            prog='behaverify python',
            description='Generate executable Python implementation from .tree specification (uses py_trees library)',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('model_file', help='Input .tree file')
        arg_parser.add_argument('location', help='Output directory')
        arg_parser.add_argument('--output_name', type=str, default=None,
            help='Custom output filename (default: derived from input filename)')
        arg_parser.add_argument('--max_iter', type=int, default=100,
            help='Maximum iterations for execution (default: 100)')
        arg_parser.add_argument('--no_var_print', action='store_true',
            help='Suppress variable printing during execution')
        arg_parser.add_argument('--serene_print', action='store_true',
            help='Use reduced (serene) output mode')
        arg_parser.add_argument('--py_tree_print', action='store_true',
            help='Use py_trees format for output')
        arg_parser.add_argument('--recursion_limit', type=int, default=0,
            help='Increase Python recursion limit for complex models (default: 0 = no change)')
        arg_parser.add_argument('--safe_assignment', action='store_true',
            help='Use safe variable assignment mode')
        arg_parser.add_argument('--no_checks', action='store_true',
            help='Skip grammar validation (faster but risky)')
        arg_parser.add_argument('--overwrite', action='store_true',
            help='Overwrite existing output files/directories')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('python', args.location, args.overwrite)
        output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        dsl_to_python(metamodel_file, args.model_file, output_name, os.path.join(args.location, 'python'), args.serene_print, args.max_iter, args.no_var_print, args.py_tree_print, args.recursion_limit, args.safe_assignment, args.no_checks)
    elif main_mode == 'trace':
        arg_parser = argparse.ArgumentParser(
            prog='behaverify trace',
            description='Visualize nuXmv counter-example traces as images',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        arg_parser.add_argument('mode', help=argparse.SUPPRESS)
        arg_parser.add_argument('model_file', help='Input .tree file')
        arg_parser.add_argument('trace_file', help='Input nuXmv trace file')
        arg_parser.add_argument('location', help='Output directory')
        arg_parser.add_argument('--do_not_trim', action='store_true',
            help='Disable node trimming optimization')
        arg_parser.add_argument('--recursion_limit', type=int, default=0,
            help='Increase Python recursion limit for complex models (default: 0 = no change)')
        arg_parser.add_argument('--overwrite', action='store_true',
            help='Overwrite existing output files/directories')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('trace', args.location, args.overwrite)
        # output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        counter_trace(metamodel_file, args.model_file, args.trace_file, os.path.join(args.location, 'trace'), args.do_not_trim, args.recursion_limit)
    elif main_mode == 'gui':
        gui_main()
    else:
        error_exit(
            f"Unknown mode: '{main_mode}'",
            "Available modes: cpp, grid, gui, haskell, latex, nuxmv, python, trace\n"
            "Use 'behaverify <mode> --help' for mode-specific options."
        )


if __name__ == '__main__':
    main()
