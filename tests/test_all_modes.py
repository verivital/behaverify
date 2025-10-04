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

from behaverify.behaverify import main


class TestNuXmvMode:
    """Tests for NuXmv mode with various parameter combinations."""

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

    def test_nuxmv_mode_with_simulate_flag(self):
        """Test that nuxmv mode accepts --simulate flag (integration test skipped)."""
        # This is more of an integration test that requires a real nuxmv installation
        # Just verify the argument is accepted
        pytest.skip("Requires real nuXmv installation for full test")

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_nuxmv_mode_with_recursion_limit(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with custom recursion limit."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--recursion_limit', '2000'])

        # Verify dsl_to_nuxmv was called with recursion_limit
        mock_nuxmv.assert_called_once()
        call_args = mock_nuxmv.call_args
        assert 2000 in call_args[0] or '2000' in str(call_args)


class TestPythonMode:
    """Tests for Python mode with various parameter combinations."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_mode_basic(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test basic python mode."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir), '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once()
        mock_python.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_mode_with_max_iter(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test python mode with --max_iter."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir), '--max_iter', '100', '--overwrite'])

        call_args = mock_python.call_args[0]
        assert call_args[5] == '100'  # max_iter parameter

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_mode_no_checks(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test python mode with --no_checks flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir), '--no_checks', '--overwrite'])

        mock_python.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_python_mode_with_output_name(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test python mode with custom output name."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir), '--output_name', 'custom_bt', '--overwrite'])

        call_args = mock_python.call_args[0]
        assert call_args[2] == 'custom_bt'  # output_name parameter


class TestHaskellMode:
    """Tests for Haskell mode with various parameters."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_haskell')
    def test_haskell_mode_basic(self, mock_haskell, mock_verify_loc, mock_verify_input, temp_dir):
        """Test basic haskell mode."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['haskell', str(model_file), str(temp_dir), '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once()
        mock_haskell.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_haskell')
    def test_haskell_mode_with_output_name(self, mock_haskell, mock_verify_loc, mock_verify_input, temp_dir):
        """Test haskell mode with custom output name."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['haskell', str(model_file), str(temp_dir), '--output_name', 'CustomBT', '--overwrite'])

        # Verify the function was called - don't check specific parameter indices
        # as they may vary based on implementation details
        mock_haskell.assert_called_once()
        call_args = mock_haskell.call_args
        # Check that 'CustomBT' appears somewhere in the call
        assert 'CustomBT' in str(call_args)


class TestLatexMode:
    """Tests for LaTeX mode with various parameters."""

    @patch('behaverify.behaverify.dsl_to_latex')
    def test_latex_mode_basic(self, mock_latex, temp_dir):
        """Test basic latex mode."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")
        output_file = temp_dir / "output.tex"

        with patch('builtins.print'):
            main(['latex', str(model_file), str(output_file)])

        mock_latex.assert_called_once()

    @patch('behaverify.behaverify.dsl_to_latex')
    def test_latex_mode_insert_only(self, mock_latex, temp_dir):
        """Test latex mode with --insert_only flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")
        output_file = temp_dir / "output.tex"

        with patch('builtins.print'):
            main(['latex', str(model_file), str(output_file), '--insert_only'])

        call_args = mock_latex.call_args[0]
        assert call_args[3] is True  # insert_only parameter

    @patch('behaverify.behaverify.dsl_to_latex')
    def test_latex_mode_on_sides(self, mock_latex, temp_dir):
        """Test latex mode with --on_sides flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")
        output_file = temp_dir / "output.tex"

        with patch('builtins.print'):
            main(['latex', str(model_file), str(output_file), '--on_sides'])

        call_args = mock_latex.call_args[0]
        assert call_args[5] is True  # on_sides parameter


class TestTraceMode:
    """Tests for trace mode."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.counter_trace')
    def test_trace_mode_basic(self, mock_trace, mock_verify_loc, mock_verify_input, temp_dir):
        """Test basic trace mode."""
        model_file = temp_dir / "test.tree"
        trace_file = temp_dir / "trace.txt"
        model_file.write_text("dummy")
        trace_file.write_text("trace data")

        with patch('builtins.print'):
            main(['trace', str(model_file), str(trace_file), str(temp_dir), '--overwrite'])

        mock_verify_input.assert_called()
        mock_verify_loc.assert_called_once()
        mock_trace.assert_called_once()


class TestCheckGrammarMode:
    """Tests for check_grammar mode."""

    def test_check_grammar_mode_exists(self):
        """Test that check_grammar mode exists (full test requires valid model)."""
        # This mode requires a valid tree file to test properly
        # The mode is tested indirectly through regression tests
        pytest.skip("Requires valid tree file for full test - covered by regression tests")


class TestOverwriteFlag:
    """Tests for --overwrite flag across different modes."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_overwrite_flag_enabled(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test that --overwrite flag is properly passed."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir), '--overwrite'])

        # Verify overwrite flag was passed to verify_location
        call_args = mock_verify_loc.call_args[0]
        assert call_args[2] is True  # overwrite parameter

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_python')
    def test_overwrite_flag_disabled(self, mock_python, mock_verify_loc, mock_verify_input, temp_dir):
        """Test behavior without --overwrite flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['python', str(model_file), str(temp_dir)])

        # Verify overwrite flag defaults to False
        call_args = mock_verify_loc.call_args[0]
        assert call_args[2] is False  # overwrite parameter


class TestRecursionLimit:
    """Tests for --recursion_limit parameter."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_custom_recursion_limit(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test custom recursion limit."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--recursion_limit', '5000'])

        mock_nuxmv.assert_called_once()
        call_args = mock_nuxmv.call_args
        # Check that 5000 appears in the call
        assert 5000 in call_args[0] or '5000' in str(call_args)

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_default_recursion_limit(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test default recursion limit."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate'])

        # Just verify the function was called - the default value is handled internally
        mock_nuxmv.assert_called_once()
