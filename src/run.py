#!/usr/bin/env python3
"""
BehaVerify CLI Entry Point

This script provides command-line access to the BehaVerify behavior tree tool.

USAGE EXAMPLES:

1. Generate NuXmv model for verification:
   python run.py nuxmv model.tree ./output --generate

2. Generate Python code:
   python run.py python model.tree ./output --max_iter 100

3. Generate LaTeX documentation:
   python run.py latex model.tree output.tex

4. Generate Haskell code:
   python run.py haskell model.tree ./output

5. Process counter-example trace:
   python run.py trace model.tree trace.txt ./output

6. Launch GUI for interactive visualization:
   python run.py gui

7. Check grammar only:
   python run.py check_grammar model.tree

8. Generate grid world visualization from NuXmv trace:
   python run.py grid nuxmv trace.txt ./output 9 22

EXAMPLE WITH test_examples:
   python run.py check_grammar test_examples/working/array.tree

EXAMPLE WITH tutorial_examples:
   python run.py python tutorial_examples/collatz.tree ./output --max_iter 50

For more information, see the documentation in the examples/ directory.
"""

from behaverify.behaverify import main

if __name__ == '__main__':
    main()
