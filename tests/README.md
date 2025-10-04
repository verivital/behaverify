# BehaVerify Test Suite

This directory contains the test suite for the BehaVerify project.

## Test Files

### test_behaverify.py
Unit tests for core CLI functions:
- **TestVerifyLocation** (8 tests): Tests for the `verify_location` function
  - Directory creation
  - File existence checking with/without overwrite
  - Directory mode operations
  - Error handling for invalid paths

- **TestVerifyInput** (3 tests): Tests for the `verify_input` function
  - Valid file input validation
  - Missing file error handling
  - Directory vs file distinction

### test_regression.py
Regression tests for example behavior tree models:

- **TestWorkingExamples**: Tests for working example models (6 models)
  - Structural validation of .tree files
  - Checks for required sections (tree, actions/checks, specifications, variables)
  - Handles multiple format versions (old and new variable syntax)
  - Optional metamodel parsing when textX is available

- **TestBrokenExamples**: Tests for intentionally broken models (12 models)
  - Validates that broken examples fail as expected
  - Tests include bad conditions, functions, values, ranges, templates, enums, and variables
  - Ensures error detection mechanisms work correctly

- **TestExampleModelStructure**: Tests for directory organization (4 tests)
  - Verifies test_examples directory structure
  - Ensures .tree files exist in both working and broken directories

## Running Tests

### Install Test Dependencies

```bash
# Install package with dev dependencies
pip install -e .[dev]

# Or install pytest manually
pip install pytest pytest-cov
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_behaverify.py
pytest tests/test_regression.py

# Run specific test class
pytest tests/test_regression.py::TestWorkingExamples

# Run specific test
pytest tests/test_behaverify.py::TestVerifyLocation::test_verify_location_creates_parent_directory
```

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=behaverify

# Generate HTML coverage report
pytest --cov=behaverify --cov-report=html

# View HTML report (opens in browser)
# The report will be in htmlcov/index.html
```

## Test Statistics

- **Total Tests**: 51
- **Unit Tests**: 11
- **Regression Tests**: 40
  - Working examples: 12 tests (6 models × 2 test types)
  - Broken examples: 24 tests (12 models × 2 test types)
  - Structure tests: 4 tests

## Notes

- Regression tests are designed to be flexible across different metamodel versions
- Tests gracefully handle missing dependencies (e.g., textX for metamodel parsing)
- Working examples support both old (`variables`) and new (`blackboard_variables`) formats
- Broken example tests verify that validation properly catches errors
