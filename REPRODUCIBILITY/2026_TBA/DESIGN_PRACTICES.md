# BehaVerify Design Practices

This document defines the numbered design principles used in commit messages and
code review for `2026_TBA/` folder of the BehaVerify project. When a commit references `DESIGN-XX`, the
number refers to the principle described here.

**Example commit:**
> `Feature GRID-03: Run PGD attacks for 99.5% and 99.6% accurate NNs`

> `Refactor DESIGN-08: Explain what PGD attacks are and why they are needed for compositional verification`

> `Refactor DESIGN-13: Remove stale references to old files in grid world compositional pipeline`

> `Refactor DESIGN-16: Removed unused template tree file and documented changes to the README`

> `Fix GRID-07: Remove hardcoded paths in 2025_NEUS to allow for reproducibility testing`

---

## DESIGN-01 — Multiple Modules

Divide the codebase into modules that each have a single, coherent responsibility. The current structure enforces this: `check_grammar.py` validates, `node_creator.py` builds internal representations, `dsl_to_*.py` modules generate output, and `behaverify_common.py` holds shared utilities.

Avoid large catch-all modules. If a module grows beyond a single concern, split it.

---

## DESIGN-02 — Meaningful Names

Give variables, functions, and modules non-abbreviated, intention-revealing names. Prefer `compute_next_distance` over `cnd`, and `forbidden_advisory` over `fa`.

Abbreviations are acceptable only when they are domain-standard (e.g., `smv`, `ctl`, `ltl`, `onnx`) or when the scope is small (loop variables, list comprehensions).

---

## DESIGN-03 — Named Constants

Never use magic numbers or strings in logic. All tunable values (e.g., normalisation factors, grid dimensions, timing parameters, threshold values) must be declared as named constants at the top of the relevant module or in a configuration file.

In `.tree` files, use the `constants {}` block. In Python scripts, declare module-level constants in `UPPER_SNAKE_CASE` before any functions.

---

## DESIGN-04 — Don't Repeat Yourself (DRY)

The same logic should not appear in multiple places. Shared computation belongs in `behaverify_common.py` or a dedicated helper module. If the same expression or pattern appears in more than two `dsl_to_*.py` generators, extract it.

This principle applies equally to `.tree` files: use `sub_trees {}` to factor out repeated behavior tree structure rather than copy-pasting node hierarchies.

---

## DESIGN-05 — Interact Through Modules

Modules should communicate through well-defined function signatures, not by reading each other's internal state or relying on global variables. Avoid module-level mutable state. Pass context explicitly through function arguments.

The pipeline stages (parse → validate → build → generate) should each receive their inputs as arguments and return their outputs that never reach into a sibling stage's internal data structures directly.

---

## DESIGN-06 — Code Formatting

All Python code must follow [PEP 8](https://peps.python.org/pep-0008/) conventions. The CI pipeline runs `pylint` on every push; new code must not introduce new lint
violations.

Key conventions for this codebase:
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Classes: `PascalCase`
- `.tree` DSL node names: descriptive strings, underscored (`check_obstacle`, `move_forward`)

---

## DESIGN-07 — Tightly Scoped Functions

Each function should do one thing and be short enough to read without scrolling. Long code generation functions in `dsl_to_*.py` should be decomposed into named helper functions that reflect the stage of generation they perform.

A function that both computes a value and formats it for output is doing two things. Instead, split it.

---

## DESIGN-08 — Comments

Public functions and modules should have docstrings that describe:
1. What the function does (not how)
2. What each argument represents and its expected type/domain
3. What the return value represents

Inline comments should explain *why*, not *what*. Self-explanatory code is preferred. Do not leave commented-out code blocks; use `git` history to recover old code instead.

---

## DESIGN-09 — Pipeline Stage Separation

The four stages of the BehaVerify pipeline...

1. **parse**
2. **validate**
3. **build**
4. **generate**

... must remain cleanly separated:

- Parsing (TextX) must not perform validation
- Validation (`check_grammar.py`) must not perform code generation
- Code generation (`dsl_to_*.py`) must not re-validate grammar

This makes each stage independently testable and allows the `--no_checks` flag to skip validation without touching the generator.

You can think of this design principle like Model View Separation for developing the backend and frontend separately from one another.

---

## DESIGN-10 — Encapsulation

Target-language formatting details belong in `dsl_to_<target>.py` only. The internal representation (built by `node_creator.py`) must be target-agnostic. A change to how nuXmv formats a case expression should never require touching the Python generator.

---

## DESIGN-11 — Make and Use Abstractions

Before writing a new helper, check `behaverify_common.py` and `meta_functions.py`. Duplicating utility logic across generators causes silent divergence when one copy is updated and others are not.

When adding a new expression type or meta-function, implement it once in `meta_functions.py` and propagate to all generators that need it.

---

## DESIGN-12 — Automated Testing

All new functionality must be covered by tests in `tests/`. Use `pytest`.

The test hierarchy:
1. **Unit tests:** individual functions in `tests/test_behaverify.py`
2. **Regression tests:** valid models in `test_examples/working/`, invalid models
   in `test_examples/intentionally_broken/`
3. **End-to-end tests:** generate code and verify it compiles or produces the
   expected nuXmv output

Do not modify files in `test_examples/intentionally_broken/` to make them valid, as they are intentionally broken and test error-handling paths.

---

## DESIGN-13 — Programs Should Not Crash

The tool must never crash with an unhandled exception when given bad user input. Grammar errors, missing files, unsupported configurations, and type mismatches must produce a clear error message via `BTreeException` that identifies the problem and, where possible, the location in the `.tree` file.

Reserve Python exceptions for genuine programmer errors (bugs), not user mistakes.

---

## DESIGN-14 — Handle Errors Using Exception Flows

Use `BTreeException` (defined in `behaverify_common.py`) for all domain-specific errors. Do not return `None` or sentinel values to signal failure, but instead raise explicitly.

Error messages must include enough context for the user to locate the problem: variable name, node name, line number (when available), and expected vs. actual type.

---

## DESIGN-15 — Externalize Configuration

Hardcoded parameters, file paths, and environment-specific values do not belong in source code. Instead:

- **Tool parameters** → CLI flags or YAML configuration files (e.g.,
  `verify_contracts.yaml`, `verify_acas_contracts.yaml`)
- **Behavior tree models** → `.tree` DSL files, not generated code
- **Reproducibility materials** → self-contained subdirectories under `REPRODUCIBILITY/`,
  isolated from the core `src/` tree
- **nuXmv commands** → `scripts/nuxmv_commands/` command files, not hardcoded strings
- **NN weights** → ONNX files referenced by path, not embedded in code

A `REPRODUCIBILITY/<year>_<venue>/` directory is itself a configuration artifact: it captures the exact scripts, models, and parameters used to produce a specific paper's results. It should be independently reproducible from a clean checkout.

---

## DESIGN-16 — No Dead Code

The codebase must not contain unused variables, unreachable branches, or obsolete functions. Do not comment out blocks of code to preserve them. `git` history serves that purpose.

Unused imports trigger `pylint` warnings and must be removed. If a function is experimental and not yet wired up, note this in a `TODO.md` entry rather than leaving orphaned code.

---

## DESIGN-17 — Explicit Immutability

Prefer immutable data structures for values that should not change after construction. In Python, use tuples over lists for fixed-length sequences, and avoid mutating function arguments.

In `.tree` files, values declared in `constants {}` are compile-time constants and must not be used as mutable variables. Respect the distinction between `VAR` and `DEFINE` variables.

---

## DESIGN-18 — APIs

`behaverify.py` and the programmatic API tested in `tests/test_programmatic_api.py` are public interfaces. Breaking changes to argument names, return types, or behaviour
require a version bump and a note in the changelog.

Internal functions (prefixed with `_` by convention) may change freely.

---

## DESIGN-19 — Apply Design Patterns

When the BehaVerify DSL supports a construct (expression type, node kind, variable scope), all code generators that claim to support it must handle it identically in semantics, even if the syntax differs across target languages.

A construct that works in the nuXmv generator but silently produces wrong output in the Python generator is a bug, not a limitation.

---

## DESIGN-20 — Reflect, not Hardcode

Do not use long `if/elif` chains to dispatch on string tags or type names if a dictionary lookup, `match` statement, or polymorphic call achieves the same result more clearly. Hardcoded dispatch chains are fragile when new cases are added.

---

## DESIGN-21 — Logging

Use Python's `logging` module instead of `print()` for diagnostic output. Reserve `print()` for user-facing output (progress messages, results).

Log levels:
- `DEBUG`: internal state useful for diagnosing generation issues
- `INFO`: high-level pipeline progress (file written, stage completed)
- `WARNING`: recoverable issues (node trimmed, stage optimised away)
- `ERROR`: unrecoverable issues before raising `BTreeException`

---

## Credits

The BehaVerify design practices were inspired by Professor Robert Duvall (Duke University, COMPSCI308).
