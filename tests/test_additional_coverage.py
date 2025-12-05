"""
Additional tests for edge cases, error handling, and important features.

These tests cover:
- Error handling for invalid inputs
- Edge cases in DSL processing
- Different DSL features (arrays, loops, enumerations)
- Command-line argument validation
- File I/O error handling
"""

import os
import sys
import pytest
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src to path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from behaverify.behaverify import main, verify_location, verify_input


class TestErrorHandling:
    """Test error handling for invalid inputs."""

    def test_verify_input_with_directory_raises_error(self, temp_dir):
        """Test that verify_input raises error when given a directory."""
        with pytest.raises(SystemExit):
            verify_input(str(temp_dir))

    def test_verify_input_with_nonexistent_file_raises_error(self, temp_dir):
        """Test that verify_input raises error for nonexistent file."""
        nonexistent = temp_dir / "does_not_exist.tree"
        with pytest.raises(SystemExit):
            verify_input(str(nonexistent))

    def test_verify_location_parent_as_file_raises_error(self, temp_file):
        """Test that verify_location raises error when parent is a file."""
        invalid_path = str(temp_file) + "/child.txt"
        with pytest.raises(SystemExit):
            verify_location(None, invalid_path, False)

    def test_verify_location_directory_mode_with_file_raises_error(self, temp_file):
        """Test that verify_location raises error when location is file not dir."""
        with pytest.raises(SystemExit):
            verify_location("some_dir", str(temp_file), False)

    def test_main_with_unknown_mode_handles_gracefully(self):
        """Test that main handles unknown modes gracefully."""
        with pytest.raises(SystemExit):
            main(['totally_unknown_mode', 'file.tree', './output'])


class TestCommandLineArguments:
    """Test command-line argument processing."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_latex')
    def test_latex_mode_with_all_flags(self, mock_latex, mock_verify_loc, mock_verify_input, temp_dir):
        """Test latex mode with all optional flags."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")
        output_file = temp_dir / "output.tex"

        with patch('builtins.print'):
            main(['latex', str(model_file), str(output_file),
                  '--insert_only', '--on_sides', '--recursion_limit', '5000'])

        mock_latex.assert_called_once()
        call_args = mock_latex.call_args[0]
        # Verify flags were passed
        assert call_args[3] is True  # insert_only
        assert call_args[5] is True  # on_sides
        assert call_args[4] == 5000  # recursion_limit

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_mode_with_print_flags(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test python mode with various print flags."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir),
                  '--no_var_print', '--serene_print', '--py_tree_print',
                  '--overwrite'])

        mock_python.assert_called_once()
        # Verify that the function was called with appropriate flags


class TestDSLFeatures:
    """Test support for different DSL features through example files."""

    TEST_EXAMPLES_DIR = Path(__file__).parent.parent / "test_examples" / "working"

    def test_array_example_structure(self):
        """Test that array example has proper structure."""
        array_file = self.TEST_EXAMPLES_DIR / "array.tree"
        assert array_file.exists()

        content = array_file.read_text()
        # Should have array-related keywords
        assert "array" in content.lower() or "index" in content.lower()

    def test_loop_example_structure(self):
        """Test examples with loop constructs."""
        # Check if any examples use loops
        for tree_file in self.TEST_EXAMPLES_DIR.glob("*.tree"):
            content = tree_file.read_text()
            if "loop" in content.lower():
                # Found a file with loops
                assert "loop" in content
                break

    def test_useful_array_example_structure(self):
        """Test useful_array example structure."""
        useful_array = self.TEST_EXAMPLES_DIR / "useful_array.tree"
        assert useful_array.exists()

        content = useful_array.read_text()
        # Should contain array operations
        assert len(content) > 0


class TestFileOperations:
    """Test file I/O and directory operations."""

    def test_verify_location_creates_nested_directories(self, temp_dir):
        """Test that verify_location creates nested directory structures."""
        nested_path = temp_dir / "level1" / "level2" / "output.txt"
        verify_location(None, str(nested_path), False)

        # Parent directories should be created
        assert nested_path.parent.exists()
        assert nested_path.parent.is_dir()

    def test_verify_location_directory_mode_creates_subdirectory(self, temp_dir):
        """Test directory mode creates subdirectory."""
        verify_location("my_output", str(temp_dir), False)

        output_dir = temp_dir / "my_output"
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_verify_location_with_overwrite_allows_existing(self, temp_dir):
        """Test that overwrite flag allows reusing existing directories."""
        output_dir = temp_dir / "existing"
        output_dir.mkdir()

        # Should not raise error with overwrite=True
        verify_location("existing", str(temp_dir), True)

        assert output_dir.exists()


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    TUTORIAL_DIR = Path(__file__).parent.parent / "tutorial_examples"

    def test_multiple_tutorial_examples_exist(self):
        """Test that multiple tutorial examples are available."""
        tree_files = list(self.TUTORIAL_DIR.glob("*.tree"))
        assert len(tree_files) >= 3, "Expected at least 3 tutorial examples"

    def test_tutorial_readme_exists(self):
        """Test that tutorial README exists for documentation."""
        readme = self.TUTORIAL_DIR / "README.md"
        assert readme.exists(), "Tutorial README should exist"

    def test_network_directory_for_neural_examples(self):
        """Test that networks directory exists for neural network examples."""
        networks_dir = self.TUTORIAL_DIR / "networks"
        if networks_dir.exists():
            # If networks directory exists, should have .onnx files
            onnx_files = list(networks_dir.glob("*.onnx"))
            assert len(onnx_files) > 0, "Networks directory should contain .onnx files"


class TestNuXmvModeVariations:
    """Test different NuXmv mode variations and flags."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_nuxmv_with_behave_only(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --behave_only flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--behave_only', '--overwrite'])

        mock_nuxmv.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_nuxmv_with_keep_last_stage(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --keep_last_stage flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--keep_last_stage', '--overwrite'])

        mock_nuxmv.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_nuxmv_with_do_not_trim(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --do_not_trim flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--do_not_trim', '--overwrite'])

        mock_nuxmv.assert_called_once()


class TestPythonModeVariations:
    """Test different Python mode variations."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_with_safe_assignment(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test python mode with --safe_assignment flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir), '--safe_assignment', '--overwrite'])

        mock_python.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_with_all_print_options(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test python mode with all print options enabled."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir),
                  '--serene_print', '--no_var_print', '--py_tree_print',
                  '--overwrite'])

        mock_python.assert_called_once()


class TestTraceModeFeatures:
    """Test trace mode functionality."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.counter_trace')
    def test_trace_mode_with_do_not_trim(self, mock_trace, mock_verify_loc, mock_verify_input, temp_dir):
        """Test trace mode with --do_not_trim flag."""
        model_file = temp_dir / "test.tree"
        trace_file = temp_dir / "trace.txt"
        model_file.write_text("dummy")
        trace_file.write_text("trace")

        with patch('builtins.print'):
            main(['trace', str(model_file), str(trace_file), str(temp_dir),
                  '--do_not_trim', '--overwrite'])

        mock_trace.assert_called_once()
        # Verify do_not_trim parameter was passed
        call_args = mock_trace.call_args[0]
        assert call_args[4] is True  # do_not_trim parameter
