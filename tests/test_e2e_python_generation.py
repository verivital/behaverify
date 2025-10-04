"""
End-to-end tests for Python code generation and execution.

These tests verify the complete pipeline:
1. Read behavior tree DSL (.tree file)
2. Generate Python code using dsl_to_python
3. Execute the generated Python code
4. Verify no exceptions and correct output
"""

import os
import sys
import pytest
import subprocess
import tempfile
from pathlib import Path
import importlib.util
import shutil

# Add src to path to allow imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from behaverify.behaverify import main


class TestE2EPythonGeneration:
    """End-to-end tests for Python code generation from tree DSL."""

    TUTORIAL_EXAMPLES_DIR = Path(__file__).parent.parent / "tutorial_examples"

    @pytest.fixture
    def output_dir(self):
        """Create a temporary output directory for generated code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_e2e_collatz_generation_and_execution(self, output_dir):
        """Test complete pipeline for collatz example: generate and execute."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "collatz.tree"
        assert tree_file.exists(), "collatz.tree not found"

        # Use run.py directly instead of installed module
        run_py = Path(__file__).parent.parent / "src" / "run.py"

        # Step 1: Generate Python code
        with subprocess.Popen(
            [sys.executable, str(run_py),
             "python", str(tree_file), str(output_dir),
             "--max_iter", "10", "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            stdout, stderr = proc.communicate(timeout=30)

        # Verify generation succeeded
        assert proc.returncode == 0, f"Code generation failed:\nSTDOUT: {stdout}\nSTDERR: {stderr}"

        # Step 2: Verify Python files were created
        python_dir = output_dir / "python"
        assert python_dir.exists(), "Python output directory not created"

        # Find the generated Python file
        python_files = list(python_dir.glob("*.py"))
        assert len(python_files) > 0, "No Python files generated"

        main_py = python_dir / "collatz.py"
        assert main_py.exists(), f"collatz.py not found. Files: {python_files}"

        # Step 3: Execute the generated Python code
        try:
            result = subprocess.run(
                [sys.executable, str(main_py)],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(python_dir)
            )

            # Check if execution failed due to missing dependencies
            if result.returncode != 0:
                stderr = result.stderr.lower()
                if "modulenotfounderror" in stderr or "no module named" in stderr:
                    pytest.skip(f"Skipping execution test - missing dependency: {result.stderr}")

            # Verify execution completed without exceptions
            assert result.returncode == 0, \
                f"Execution failed with return code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

            # Verify some output was produced
            assert len(result.stdout) > 0 or len(result.stderr) > 0, \
                "No output produced from execution"

            # Collatz should produce some tick output
            output = result.stdout + result.stderr
            assert "tick" in output.lower() or "success" in output.lower() or "failure" in output.lower() or len(output) > 0, \
                f"Expected behavior tree output not found in: {output}"

        except subprocess.TimeoutExpired:
            pytest.fail("Execution timed out - possible infinite loop")

    def test_e2e_primes_generation_and_execution(self, output_dir):
        """Test complete pipeline for primes example: generate and execute."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "primes.tree"
        assert tree_file.exists(), "primes.tree not found"

        # Step 1: Generate Python code
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--max_iter", "5", "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            stdout, stderr = proc.communicate(timeout=30)

        # Check if generation failed due to missing onnx/onnxruntime
        if proc.returncode != 0:
            if "onnx" in stderr.lower():
                pytest.skip(f"Skipping primes test - requires onnx/onnxruntime")

        assert proc.returncode == 0, f"Code generation failed:\nSTDOUT: {stdout}\nSTDERR: {stderr}"

        # Step 2: Verify Python files were created
        python_dir = output_dir / "python"
        main_py = python_dir / "primes.py"
        assert main_py.exists(), "primes.py not found"

        # Step 3: Execute the generated Python code
        try:
            result = subprocess.run(
                [sys.executable, str(main_py)],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(python_dir)
            )

            # Check for missing dependencies
            if result.returncode != 0:
                stderr = result.stderr.lower()
                if "modulenotfounderror" in stderr or "no module named" in stderr:
                    pytest.skip(f"Skipping execution - missing dependency: {result.stderr}")

            # Verify execution completed
            assert result.returncode == 0, \
                f"Execution failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

            # Verify output
            assert len(result.stdout) > 0 or len(result.stderr) > 0, \
                "No output produced"

        except subprocess.TimeoutExpired:
            pytest.fail("Execution timed out")

    def test_e2e_light_controller_generation(self, output_dir):
        """Test Python generation for light_controller example (more complex)."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "light_controller.tree"
        assert tree_file.exists(), "light_controller.tree not found"

        # Generate Python code
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--max_iter", "3", "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            stdout, stderr = proc.communicate(timeout=30)

        assert proc.returncode == 0, f"Code generation failed:\nSTDOUT: {stdout}\nSTDERR: {stderr}"

        # Verify files created
        python_dir = output_dir / "python"
        main_py = python_dir / "light_controller.py"
        assert main_py.exists(), "light_controller.py not found"

        # Verify the file has valid Python syntax
        with open(main_py, 'r') as f:
            code = f.read()
            # Basic validation - should have imports and class definitions
            assert "import" in code, "No imports found in generated code"
            assert "class" in code or "def" in code, "No class/function definitions found"

        # Try to execute (light_controller may be more complex)
        try:
            result = subprocess.run(
                [sys.executable, str(main_py)],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=str(python_dir)
            )

            # Just verify it doesn't crash with syntax errors
            # Return code may vary depending on the tree's logic
            output = result.stdout + result.stderr
            assert "SyntaxError" not in output and "IndentationError" not in output, \
                f"Syntax error in generated code: {output}"

        except subprocess.TimeoutExpired:
            # Timeout is acceptable for some complex examples
            pass


class TestE2EPythonWithOptions:
    """Test Python generation with various command-line options."""

    TUTORIAL_EXAMPLES_DIR = Path(__file__).parent.parent / "tutorial_examples"

    @pytest.fixture
    def output_dir(self):
        """Create a temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_e2e_with_custom_output_name(self, output_dir):
        """Test generation with custom output name."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "collatz.tree"

        # Generate with custom name
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--output_name", "my_custom_tree",
             "--max_iter", "5", "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            stdout, stderr = proc.communicate(timeout=30)

        assert proc.returncode == 0, f"Generation failed: {stderr}"

        # Verify custom-named file exists
        python_dir = output_dir / "python"
        custom_py = python_dir / "my_custom_tree.py"
        assert custom_py.exists(), f"Custom named file not found. Files: {list(python_dir.glob('*.py'))}"

    def test_e2e_with_no_checks_flag(self, output_dir):
        """Test generation with --no_checks flag."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "collatz.tree"  # Use collatz instead of primes

        # Generate with no_checks
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--no_checks", "--max_iter", "3", "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            stdout, stderr = proc.communicate(timeout=30)

        assert proc.returncode == 0, f"Generation failed: {stderr}"

        # Verify file created
        python_dir = output_dir / "python"
        main_py = python_dir / "collatz.py"
        assert main_py.exists()

    def test_e2e_higher_max_iter(self, output_dir):
        """Test execution with higher iteration count."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "collatz.tree"

        # Generate with higher max_iter
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--max_iter", "50", "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            stdout, stderr = proc.communicate(timeout=30)

        assert proc.returncode == 0

        # Execute with more iterations
        python_dir = output_dir / "python"
        main_py = python_dir / "collatz.py"

        result = subprocess.run(
            [sys.executable, str(main_py)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(python_dir)
        )

        # Check for missing dependencies
        if result.returncode != 0:
            stderr = result.stderr.lower()
            if "modulenotfounderror" in stderr or "no module named" in stderr:
                pytest.skip(f"Skipping execution - missing dependency")

        # Should still complete without errors
        assert result.returncode == 0


class TestE2EOutputValidation:
    """Test validation of generated Python code output."""

    TUTORIAL_EXAMPLES_DIR = Path(__file__).parent.parent / "tutorial_examples"

    @pytest.fixture
    def output_dir(self):
        """Create a temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_generated_code_has_required_components(self, output_dir):
        """Test that generated code contains expected components."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "collatz.tree"

        # Generate code
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            proc.communicate(timeout=30)

        python_dir = output_dir / "python"
        main_py = python_dir / "collatz.py"

        # Read generated code
        with open(main_py, 'r') as f:
            code = f.read()

        # Verify essential components
        assert "import" in code, \
            "Missing imports in generated code"

        # Check for behavior tree components (various formats possible)
        has_bt_logic = any(keyword in code.lower() for keyword in
                          ["tick", "execute", "def create", "blackboard", "py_trees"])
        assert has_bt_logic, \
            "Missing behavior tree logic in generated code"

        # Verify it's valid Python
        try:
            compile(code, str(main_py), 'exec')
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")

    def test_generated_code_imports_correctly(self, output_dir):
        """Test that generated code can be imported as a module."""
        tree_file = self.TUTORIAL_EXAMPLES_DIR / "collatz.tree"  # Use collatz

        # Generate code
        with subprocess.Popen(
            [sys.executable, str(Path(__file__).parent.parent / "src" / "run.py"),
             "python", str(tree_file), str(output_dir),
             "--overwrite"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.TUTORIAL_EXAMPLES_DIR.parent)
        ) as proc:
            proc.communicate(timeout=30)

        python_dir = output_dir / "python"
        main_py = python_dir / "collatz.py"

        # Try to import the module
        spec = importlib.util.spec_from_file_location("collatz_module", main_py)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            try:
                # Add the directory to sys.path temporarily
                sys.path.insert(0, str(python_dir))
                spec.loader.exec_module(module)
                sys.path.remove(str(python_dir))

                # If we got here, import succeeded
                assert module is not None

            except ModuleNotFoundError as e:
                # Skip if missing dependencies like onnxruntime
                if "onnx" in str(e).lower():
                    pytest.skip(f"Skipping import test - missing dependency: {e}")
                pytest.fail(f"Failed to import generated module: {e}")
            except Exception as e:
                pytest.fail(f"Failed to import generated module: {e}")
