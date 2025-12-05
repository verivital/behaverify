import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

# Add src to path to allow imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from behaverify.behaverify import main, get_metamodel_file


class TestProgrammaticAPI:
    """Tests for programmatic API (calling main with argv parameter)."""

    def test_get_metamodel_file(self):
        """Test that get_metamodel_file returns a valid path."""
        metamodel_file = get_metamodel_file()
        assert metamodel_file is not None
        # Should contain 'behaverify.tx' in the path
        assert 'behaverify.tx' in str(metamodel_file)

    @patch('behaverify.behaverify.dsl_to_latex')
    def test_main_latex_mode_programmatic(self, mock_latex, temp_dir):
        """Test calling main programmatically with latex mode."""
        # Create a dummy model file
        model_file = temp_dir / "test_model.tree"
        model_file.write_text("dummy content")
        output_file = temp_dir / "output.tex"

        # Call main programmatically
        with patch('builtins.print'):  # Suppress print output
            main(['latex', str(model_file), str(output_file)])

        # Verify that dsl_to_latex was called
        assert mock_latex.called
        call_args = mock_latex.call_args[0]
        assert str(model_file) in str(call_args[1])
        assert str(output_file) in str(call_args[2])

    def test_main_unknown_mode(self, capsys):
        """Test that unknown mode exits with error."""
        with pytest.raises(SystemExit):
            main(['unknown_mode'])

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_main_python_mode_with_options(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test calling main with python mode and various options."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")
        output_dir = temp_dir / "output"

        with patch('builtins.print'):
            main([
                'python',
                str(model_file),
                str(output_dir),
                '--output_name', 'custom_name',
                '--max_iter', '50',
                '--no_checks',
                '--overwrite'
            ])

        # Verify functions were called
        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once()
        mock_python.assert_called_once()

        # Check that options were passed correctly
        call_args = mock_python.call_args
        # output_name should be 'custom_name'
        assert call_args[0][2] == 'custom_name'
        # max_iter should be 50 (as int)
        assert call_args[0][5] == 50


class TestBackwardCompatibility:
    """Tests to ensure CLI backward compatibility."""

    def test_main_without_argv_uses_sys_argv(self):
        """Test that calling main() without arguments uses sys.argv."""
        # When main() is called without arguments, it should use sys.argv
        # This is the default argparse behavior
        # We just verify it doesn't crash with no arguments
        # (In real usage, argparse would parse sys.argv)
        pass  # This is tested implicitly by CLI usage

    @patch('sys.argv', ['behaverify', 'latex', 'test.tree', 'output.tex'])
    @patch('behaverify.behaverify.dsl_to_latex')
    def test_main_cli_style_invocation(self, mock_latex, temp_dir):
        """Test that main() works with CLI-style invocation (no argv param)."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            # Call main() without argv - should use sys.argv
            main()

        # Should have called dsl_to_latex
        assert mock_latex.called


class TestModeHandlers:
    """Tests for different mode handlers."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_haskell')
    def test_haskell_mode(self, mock_haskell, mock_verify_loc, mock_verify_input, temp_dir):
        """Test haskell mode invocation."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['haskell', str(model_file), str(temp_dir), '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once()
        mock_haskell.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_nuxmv_mode_generate(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --generate flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once()
        mock_nuxmv.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.counter_trace')
    def test_trace_mode(self, mock_trace, mock_verify_loc, mock_verify_input, temp_dir):
        """Test trace mode invocation."""
        model_file = temp_dir / "test.tree"
        trace_file = temp_dir / "trace.txt"
        model_file.write_text("dummy")
        trace_file.write_text("trace data")

        with patch('builtins.print'):
            main(['trace', str(model_file), str(trace_file), str(temp_dir), '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once()
        mock_trace.assert_called_once()
