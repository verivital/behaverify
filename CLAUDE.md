# CLAUDE.md - AI Assistant Guide for BehaVerify

## Project Overview

**BehaVerify** is a formal verification tool for Behavior Trees that converts `.tree` specifications into:
- **nuXmv models** for formal verification using temporal logic
- **Executable implementations** in Python, Haskell, and C++
- **LaTeX visualizations** using TikZ diagrams
- **Trace visualizations** for debugging and analysis

**Primary Use Cases:**
- Formal verification of autonomous systems
- Behavior tree specification and implementation
- Neural network integration in behavior trees (ONNX support)
- Runtime monitoring and safety property verification

**Key Research Areas:**
- Neuro-symbolic behavior trees
- Stateful behavior trees
- Contingency monitors
- Temporal logic specifications (LTL, CTL, invariants)

---

## Repository Structure

```
behaverify/
├── src/behaverify/              # Core source code
│   ├── behaverify.py            # Main CLI entry point
│   ├── dsl_to_*.py              # Code generators (nuxmv, python, cpp, haskell, latex)
│   ├── behaverify_common.py     # Shared utilities
│   ├── node_creator.py          # Behavior tree node management
│   ├── check_grammar.py         # DSL validation and type checking
│   ├── data/                    # Templates and grammar files
│   │   ├── metamodel/           # TextX grammar (behaverify.tx)
│   │   ├── haskell_files/       # Haskell templates
│   │   ├── tikz_files/          # LaTeX TikZ templates
│   │   └── tick_overwrite/      # Python tick override behavior
│   ├── monitor/                 # Runtime monitoring code generation
│   └── variations/              # Alternative encodings (naive, etc.)
├── examples/                    # ~30 example behavior trees
├── test_examples/               # Test models (working & broken)
├── tests/                       # Pytest test suite
├── tutorial_examples/           # Tutorial materials
├── REPRODUCIBILITY/             # Research reproducibility (by conference/year)
├── scripts/                     # Build, timing, and testing scripts
├── docker/                      # Docker configurations
└── requirements/                # Dependency files (core, all, drawing, graphing)
```

---

## Key File Formats

### .tree Files (BehaVerify DSL)

The primary input format using TextX grammar. Structure:

```
configuration {
    # Optional: hypersafety, use_reals, neural settings
}

enumerations {
    # Define enumerated types
    # Example: my_enum := {value1, value2, value3}
}

constants {
    # Named constants
    # Example: max_speed := 100
}

variables {
    # Variable declarations with scope (bl/env), type, initial values
    # Example: variable { bl position VAR INT assign{result{0}} }
}

environment_update {
    # Define how environment updates variables
}

monitors {
    # Optional: runtime monitors for safety properties
}

checks {
    # Check node definitions (boolean conditions)
    # Example: check { is_safe arguments {} read_variables {x} condition{(gt, x, 0)} }
}

environment_checks {
    # Environment-triggered condition checks
}

actions {
    # Action node definitions (state updates)
    # Example: action { move_forward ... update { variable_statement {x assign{...}} } }
}

sub_trees {
    # Reusable behavior tree subtrees
}

tree {
    # Main behavior tree structure (composite/decorator/leaf nodes)
}

tick_prerequisite {
    # Pre-tick conditions that must hold
}

specifications {
    # Temporal logic specifications
    # INVARSPEC - Invariant specifications
    # CTLSPEC - Computational Tree Logic
    # LTLSPEC - Linear Temporal Logic
}
```

**Key Features:**
- **Variable Scopes:** `bl` (blackboard), `env` (environment), `local`
- **Types:** `BOOLEAN`, `INT`, ranges `[min, max]`, enumerations, arrays
- **Expressions:** Prefix notation - `(add, x, 1)`, `(eq, a, b)`, `(gt, x, 0)`
- **Control Flow:** `case` statements, `loop` constructs, conditionals
- **Temporal Operators:** `at` (time indexing), `next`, `globally`, `finally`, `until`
- **Node Types:**
  - **Composite:** `sequence`, `selector`, `parallel`
  - **Decorator:** `X_is_Y` patterns (success_on_running, etc.)
  - **Leaf:** `check` (conditions), `action` (updates)

---

## Development Workflow

### Installation & Setup

```bash
# Clone repository
git clone https://github.com/verivital/behaverify
cd behaverify

# Create virtual environment
python3 -m venv ../behaverify_venv
source ../behaverify_venv/bin/activate

# Install package
pip install -e .              # Editable install for development
# OR
pip install -e .[dev]         # Include dev dependencies (pytest, pytest-cov)

# Install nuXmv (required for verification)
wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz -O nuXmv_DL.tar.xz
tar -xf nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
mv nuXmv_DL/bin/nuXmv ../nuXmv
chmod +x ../nuXmv
```

### Running BehaVerify

**Command Structure:**
```bash
behaverify <mode> <model_file> <output_location> [options]
# OR
python3 -m behaverify <mode> <model_file> <output_location> [options]
```

**Common Modes:**

1. **nuXmv Mode** - Generate and verify formal models
```bash
behaverify nuxmv examples/DrunkenDrone/DrunkenDrone.tree ./output \
    --generate --invar --ctl --ltl \
    --simulate 10 \
    --nuxmv_path ../nuXmv
```

2. **Python Mode** - Generate Python implementation
```bash
behaverify python examples/Collatz/collatz.tree ./output \
    --max_iter 1000
```

3. **C++ Mode** - Generate C++ implementation
```bash
behaverify cpp examples/Collatz/collatz.tree ./output
```

4. **Haskell Mode** - Generate Haskell implementation
```bash
behaverify haskell examples/Collatz/collatz.tree ./output
```

5. **LaTeX Mode** - Generate TikZ diagram
```bash
behaverify latex examples/Collatz/collatz_small.tree ./output/diagram.tex
```

6. **Trace Mode** - Visualize verification traces
```bash
# First generate a trace with nuXmv
behaverify nuxmv examples/Collatz/collatz.tree ./output --generate --invar --nuxmv_path ../nuXmv
# Then visualize it
behaverify trace examples/Collatz/collatz.tree ./output/nuxmv/collatz_output.txt ./output/
```

7. **Grid Mode** - Render grid-world traces
```bash
behaverify grid nuxmv ./trace_file.txt ./output 10 10
```

### Important Options

- `--generate` - Generate model from .tree file (nuXmv mode)
- `--invar` - Verify invariant specifications
- `--ctl` - Verify CTL specifications
- `--ltl` - Verify LTL specifications
- `--simulate N` - Simulate for N steps
- `--nuxmv_path PATH` - Path to nuXmv executable
- `--overwrite` - Overwrite existing files
- `--no_checks` - Skip grammar validation (faster but dangerous)
- `--do_not_trim` - Keep unreachable nodes (debugging)
- `--keep_last_stage` - Disable variable stage optimization
- `--use_encoding TYPE` - Choose encoding (fastforwarding/naive)
- `--recursion_limit N` - Increase Python recursion limit for complex models

---

## Testing Infrastructure

### Running Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=behaverify

# Specific test file
pytest tests/test_regression.py

# Specific test
pytest tests/test_behaverify.py::test_specific_function
```

### Test Organization

- `tests/test_behaverify.py` - Core utility tests
- `tests/test_regression.py` - Validates working/broken examples (~40 tests)
- `tests/test_all_modes.py` - Tests all generation modes
- `tests/test_e2e_python_generation.py` - End-to-end Python generation
- `tests/test_programmatic_api.py` - API usage tests
- `tests/test_full_coverage.py` - Coverage tests
- `tests/conftest.py` - Pytest fixtures (temp_dir, temp_file, etc.)

### Test Examples

- `test_examples/working/` - Valid models for testing
- `test_examples/intentionally_broken/` - Invalid models for error testing

**Conventions:**
- Tests use pytest fixtures for temporary directories
- Regression tests validate against known-good/known-bad examples
- End-to-end tests generate code and verify compilation/execution

---

## Code Generation Pipeline

### High-Level Flow

1. **Parse** `.tree` file using TextX metamodel (`data/metamodel/behaverify.tx`)
2. **Validate** model using `check_grammar.py` (type checking, scope validation)
3. **Build** internal representation via `node_creator.py`
4. **Generate** target code using `dsl_to_*.py` modules
5. **Execute** (optional) - Run verification or compile generated code

### Key Abstractions

**NEXT_VALUE Pattern:**
- Triple: `(node_name, non_determinism, STAGE)`
- Used for variable update tracking across execution stages

**Node Hierarchy:**
- **Composite Nodes:** sequence, selector, parallel (have children)
- **Decorator Nodes:** Modify child return values
- **Leaf Nodes:** check (conditions), action (updates)

**Variable Management:**
- **Scopes:** blackboard (bl), environment (env), local
- **Stages:** Variables may have multiple staged values for verification
- **Arrays:** Supported with range-based indexing

**Meta Functions:**
- Expression builders in `meta_functions.py`
- Generate code across all target languages
- Examples: `(add, x, 1)`, `(eq, a, b)`, `(index, array, i)`

---

## Important Code Modules

### Core Modules

**`behaverify.py` (284 lines)**
- Main CLI entry point
- Argument parsing for all modes
- Mode dispatch to appropriate generator

**`dsl_to_nuxmv.py` (2,276 lines)**
- Generates nuXmv SMV models
- Handles temporal logic specifications
- Implements fast-forwarding encoding (default) and naive encoding
- Complex variable staging and update logic

**`dsl_to_python.py` (1,633 lines)**
- Generates executable Python code
- Uses `py_trees` library
- Supports neural network evaluation (ONNX)
- Multiple print modes (serene, py_tree, no_var)

**`dsl_to_cpp.py` (1,727 lines)**
- Generates C++ behavior tree implementations
- Compatible with BehaviorTree.CPP library
- Supports neural network integration

**`dsl_to_haskell.py` (1,452 lines)**
- Generates functional Haskell code
- Uses template files from `data/haskell_files/`
- Pure functional implementation of behavior trees

**`dsl_to_latex.py` (835 lines)**
- Generates TikZ diagrams
- Two modes: full LaTeX document or insertable TikZ block
- Visual representation of behavior tree structure

**`behaverify_common.py` (1,042 lines)**
- Shared utility functions
- Type handling and formatting
- Common code generation helpers
- Exception handling (`BTreeException`)

**`node_creator.py` (819 lines)**
- Creates and manages behavior tree nodes
- Builds internal representation from parsed model
- Handles node relationships and hierarchy

**`check_grammar.py` (894 lines)**
- DSL validation and type checking
- Scope checking for variables
- Expression validation
- Provides detailed error messages

### Supporting Modules

- `behaverify_to_smv.py` - SMV format writing utilities
- `counter_trace.py` - Counter-example trace visualization
- `model_to_dsl.py` - Model conversion utilities
- `meta_functions.py` / `meta_functions_neural.py` - Expression evaluation
- `behaverify_gui.py` - GUI interface (see `READMEs/gui_pdf.pdf`)

---

## Common Development Tasks

### Adding Support for a New Node Type

1. Update grammar in `src/behaverify/data/metamodel/behaverify.tx`
2. Add parsing logic in `node_creator.py`
3. Add code generation in relevant `dsl_to_*.py` files
4. Add tests in `test_examples/working/`
5. Update documentation

### Adding a New Meta Function

1. Add function definition to `meta_functions.py`
2. Update code generators to handle the new function
3. Add test cases
4. Update grammar if needed

### Debugging Generation Issues

1. Use `--no_checks` flag to skip validation (if confident model is correct)
2. Use `--do_not_trim` to keep all nodes (see unreachable nodes)
3. Use `--keep_last_stage` to see all variable stages
4. Check generated intermediate files in output directory
5. Run with verbose pytest (`pytest -v -s`) to see detailed output

### Adding New Examples

1. Create `.tree` file in appropriate `examples/` subdirectory
2. Add to test suite if it should be validated
3. Update example documentation if tutorial-worthy

---

## Key Conventions & Patterns

### Naming Conventions

- **Variables:** Descriptive names, scoped prefixes common (e.g., `bl_position`, `env_velocity`)
- **Constants:** UPPER_CASE or descriptive (e.g., `MAX_SPEED`, `threshold`)
- **Node Names:** Descriptive strings (e.g., `check_obstacle`, `move_forward`)
- **Files:** snake_case for Python, PascalCase for Haskell modules

### Code Style

- **Python:** PEP 8 compliant (enforced by pylint in CI)
- Heavy use of list comprehensions and functional patterns
- String-based code generation with indentation helpers
- Extensive use of f-strings for templating

### Expression Format (Prefix Notation)

All expressions in `.tree` files use prefix notation:
```
# Arithmetic
(add, x, 1)           # x + 1
(mult, 3, x)          # 3 * x
(sub, a, b)           # a - b
(idiv, x, 2)          # x / 2 (integer division)
(mod, x, 2)           # x % 2

# Comparison
(eq, x, 0)            # x == 0
(gt, x, 0)            # x > 0
(lt, x, max)          # x < max
(lte, a, b)           # a <= b

# Logical
(and, cond1, cond2)   # cond1 && cond2
(or, cond1, cond2)    # cond1 || cond2
(not, cond)           # !cond

# Temporal (in specifications)
(next, expr)          # Next state
(globally, expr)      # Always holds
(finally, expr)       # Eventually holds
(until, expr1, expr2) # Holds until

# Arrays
(index, array, i)     # array[i]

# Control Flow
case { condition } result { value }  # If-then-else chains
loop, i, [start, end] such_that condition, body  # Loops
```

### Error Handling

- Use `BTreeException` for domain-specific errors
- Validation in `check_grammar.py` provides detailed error messages
- Grammar errors show line numbers and context
- Type errors explain expected vs actual types

### Optimization Strategies

1. **Fast-forwarding encoding** (default for nuXmv) - More efficient state space
2. **Node trimming** - Removes unreachable nodes (disable with `--do_not_trim`)
3. **Stage optimization** - Removes unnecessary variable stages (disable with `--keep_last_stage`)
4. **Grammar checking** - Skip with `--no_checks` for faster generation (risky)

---

## Dependencies & Requirements

### Core Dependencies (requirements/core.txt)

- `py-trees>=2.2.3` - Behavior tree library for Python generation
- `textX>=4.1.0` - DSL parsing framework
- `onnx>=1.18.0` - Neural network model format
- `onnxruntime>=1.22.1` - ONNX model execution
- `graphviz>=0.20.3` - Graph visualization
- `pillow>=11.1.0` - Image processing
- `pandas>=2.2.3` - Data handling
- `Jinja2>=3.1.5` - Templating engine
- `matplotlib>=3.10.0` - Plotting and visualization

### Development Dependencies

- `pytest>=8.0.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `pylint` - Code quality (CI)

### External Tools

- **nuXmv 2.1.0** - Model checker (not included, must download separately)
  - Required for formal verification
  - Download from https://nuxmv.fbk.eu/
  - Cannot be redistributed per license

### Python Version

- Requires Python 3.10+
- Tested on Python 3.10, 3.11, 3.12

---

## CI/CD & Automation

### GitHub Actions

**Pylint Workflow** (`.github/workflows/pylint.yml`)
- Runs on every push
- Python 3.12
- Lints all Python files in repository

### Scripts

- `scripts/` contains various automation:
  - Build scripts
  - Timing measurements
  - Batch processing
  - Result analysis

---

## Common Pitfalls & Tips for AI Assistants

### Understanding the Codebase

1. **DSL is Prefix Notation:** All expressions use prefix notation, not infix
   - `(add, x, 1)` NOT `x + 1`
   - `(gt, x, 0)` NOT `x > 0`

2. **Variable Staging:** Variables may have multiple staged values
   - Used for verification encoding
   - `_stage_0`, `_stage_1`, etc. in generated code
   - Can be disabled with `--keep_last_stage`

3. **Node Trimming:** Unreachable nodes removed by default
   - May cause confusion when debugging
   - Use `--do_not_trim` to see all nodes

4. **Grammar Validation:** Errors are caught early
   - Type checking is strict
   - Scope checking enforces variable declarations
   - Can skip with `--no_checks` but risky

### Working with Examples

1. **Start with Simple Examples:**
   - `examples/Collatz/` - Simple behavior tree
   - `examples/Minimal-Example/` - Minimal working example
   - `tutorial_examples/` - Tutorial materials

2. **Broken Examples are Intentional:**
   - `test_examples/intentionally_broken/` contains invalid models
   - Used for testing error handling
   - Don't "fix" these unless specifically asked

3. **Large Examples:**
   - Some examples are very complex (e.g., ANSR_ONNX)
   - May require increased recursion limits
   - May take significant time to process

### Code Generation

1. **String-Based Generation:**
   - Most code generators build strings with indentation
   - Be careful with indentation levels
   - Use helper functions from `behaverify_common.py`

2. **Template Files:**
   - Haskell and LaTeX use template files
   - Located in `src/behaverify/data/`
   - Modified via string replacement

3. **Testing Generated Code:**
   - Python: Can be executed directly
   - Haskell: Needs GHC compiler
   - C++: Needs BehaviorTree.CPP library
   - nuXmv: Needs nuXmv executable

### Debugging

1. **Check Generated Files:**
   - Outputs are written to specified location
   - Inspect intermediate files for issues
   - nuXmv output includes verification results

2. **Use Verbose Testing:**
   - `pytest -v -s` shows all output
   - Helps identify specific failures
   - Shows generated file contents

3. **Grammar Errors:**
   - Read error messages carefully
   - Show line numbers and context
   - Check `data/metamodel/README.md` for grammar details

### File Locations

1. **Source Code:** All in `src/behaverify/`
2. **Tests:** All in `tests/`
3. **Examples:** Various subdirectories in `examples/`
4. **Grammar:** `src/behaverify/data/metamodel/behaverify.tx`
5. **Templates:** `src/behaverify/data/{haskell_files,tikz_files}/`

---

## Research Context

BehaVerify is actively used in academic research. Key publications:

1. **Neuro-Symbolic Behavior Trees** (NeuS 2025)
2. **Formalizing Stateful Behavior Trees** (FMAS 2024)
3. **Verification with Contingency Monitors** (FMAS 2024)
4. **BehaVerify: Temporal Logic for Behavior Trees** (SEFM 2022)

**Reproducibility:**
- `REPRODUCIBILITY/` contains materials organized by conference/year
- Includes timing scripts and result processing
- Ensures research results can be replicated

---

## Quick Reference

### File Extensions

- `.tree` - BehaVerify DSL model files
- `.smv` - nuXmv model files (generated)
- `.py` - Python implementations (generated or source)
- `.hs` - Haskell implementations (generated)
- `.cpp/.h` - C++ implementations (generated)
- `.tex` - LaTeX diagrams (generated)

### Key Commands

```bash
# Generate and verify
behaverify nuxmv model.tree output/ --generate --ctl --nuxmv_path ../nuXmv

# Generate Python
behaverify python model.tree output/

# Generate C++
behaverify cpp model.tree output/

# Generate LaTeX
behaverify latex model.tree output/diagram.tex

# Run tests
pytest
pytest -v --cov=behaverify

# Install for development
pip install -e .[dev]
```

### Important Directories

- `src/behaverify/` - All source code
- `examples/` - Example behavior trees
- `tests/` - Test suite
- `test_examples/working/` - Valid test models
- `test_examples/intentionally_broken/` - Invalid test models (for error testing)

---

## When Working on This Codebase

### DO:

- Read example `.tree` files to understand DSL syntax
- Use existing tests as templates for new tests
- Check `behaverify_common.py` for utility functions before writing new ones
- Use `--do_not_trim` and `--keep_last_stage` when debugging
- Run tests after making changes
- Follow prefix notation for all expressions
- Use appropriate variable scopes (bl/env/local)
- Document complex algorithms or non-obvious code

### DON'T:

- Mix infix and prefix notation in expressions
- Skip grammar validation unless necessary (`--no_checks`)
- Modify intentionally broken test examples
- Assume variables are global (check scope)
- Generate files without checking for existing content (use `--overwrite` flag)
- Ignore type errors from grammar checker
- Commit without running tests

### When Asked to:

1. **"Add a feature"** - Check if similar functionality exists, update grammar if needed, add tests
2. **"Fix a bug"** - Reproduce with test, identify root cause, fix, verify with test
3. **"Generate code"** - Use appropriate mode, check generated output, verify it compiles/runs
4. **"Add an example"** - Create `.tree` file, test generation in multiple modes, add to test suite
5. **"Debug verification"** - Check specifications, verify model validity, inspect nuXmv output

---

## Additional Resources

- **Main README:** `/home/user/behaverify/README.md`
- **Grammar Documentation:** `/home/user/behaverify/src/behaverify/data/metamodel/README.md`
- **Tutorial:** `/home/user/behaverify/tutorial_examples/README.md`
- **Reproducibility:** `/home/user/behaverify/REPRODUCIBILITY/README.md`
- **GUI Documentation:** `/home/user/behaverify/READMEs/gui_pdf.pdf`
- **Examples:** `/home/user/behaverify/examples/`
- **GitHub:** https://github.com/verivital/behaverify
- **nuXmv:** https://nuxmv.fbk.eu/

---

## Summary for AI Assistants

**BehaVerify** is a sophisticated tool bridging formal verification and practical behavior tree implementation. When working with this codebase:

1. **Understand the DSL:** Prefix notation, strict typing, scoped variables
2. **Follow the Pipeline:** Parse → Validate → Build → Generate
3. **Use Examples:** Learn from existing `.tree` files
4. **Test Thoroughly:** Use pytest, validate generated code
5. **Respect Conventions:** Naming, indentation, error handling
6. **Leverage Utilities:** Use `behaverify_common.py` functions
7. **Debug Systematically:** Check grammar, inspect generated files, use debug flags
8. **Document Changes:** Update tests, examples, and docs

The codebase is well-structured but complex due to the nature of formal verification and multi-language code generation. Take time to understand the existing patterns before making changes.

---

*Last Updated: 2025-11-17*
*BehaVerify Version: 0.0.1*
*Repository: https://github.com/verivital/behaverify*
