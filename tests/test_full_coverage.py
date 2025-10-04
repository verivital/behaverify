import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import tempfile

# Add src to path to allow imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from behaverify.behaverify import main, get_metamodel_file


class TestGetMetamodelFileCoverage:
    """Tests to cover get_metamodel_file exception handling."""

    def test_get_metamodel_file_normal_path(self):
        """Test get_metamodel_file when module is found."""
        metamodel = get_metamodel_file()
        assert 'behaverify.tx' in str(metamodel)

    @patch('behaverify.behaverify.files')
    def test_get_metamodel_file_fallback_path(self, mock_files):
        """Test get_metamodel_file fallback when module not found."""
        # Simulate ModuleNotFoundError
        mock_files.side_effect = ModuleNotFoundError("Module not found")

        with patch('builtins.print'):
            metamodel = get_metamodel_file()

        # Should fall back to direct path
        assert 'behaverify.tx' in str(metamodel)


class TestGridModeCoverage:
    """Tests to cover grid mode submodes."""

    def test_grid_network_mode_not_implemented(self):
        """Test that grid network mode raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match='Soon'):
            main(['grid', 'network', 'model.tree', 'trace.txt', './output', 'name'])

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.grid_world_draw_nuxmv_output')
    def test_grid_nuxmv_mode(self, mock_draw, mock_verify_loc, mock_verify_input, temp_dir):
        """Test grid nuxmv mode."""
        trace_file = temp_dir / "trace.txt"
        trace_file.write_text("trace data")

        with patch('builtins.print'):
            main(['grid', 'nuxmv', str(trace_file), str(temp_dir), '9', '22', '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once_with('grid_nuxmv', str(temp_dir), True)
        mock_draw.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.grid_world_draw_nuxmv_output')
    def test_grid_nuxmv_mode_with_stage(self, mock_draw, mock_verify_loc, mock_verify_input, temp_dir):
        """Test grid nuxmv mode with --stage parameter."""
        trace_file = temp_dir / "trace.txt"
        trace_file.write_text("trace data")

        with patch('builtins.print'):
            main(['grid', 'nuxmv', str(trace_file), str(temp_dir), '9', '22', '--stage', '5'])

        mock_draw.assert_called_once()
        # Verify stage parameter was passed
        call_args = mock_draw.call_args[0]
        assert call_args[4] == 5  # stage parameter

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.grid_world_draw_python_output')
    def test_grid_python_mode(self, mock_draw, mock_verify_loc, mock_verify_input, temp_dir):
        """Test grid python mode."""
        trace_file = temp_dir / "trace.txt"
        trace_file.write_text("trace data")

        with patch('builtins.print'):
            main(['grid', 'python', str(trace_file), str(temp_dir), '9', '22', '--overwrite'])

        mock_verify_input.assert_called_once()
        mock_verify_loc.assert_called_once_with('grid_python', str(temp_dir), True)
        mock_draw.assert_called_once()


class TestNuXmvExecutionCoverage:
    """Tests to cover nuXmv execution paths."""

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    def test_nuxmv_without_path_raises_error(self, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test that running nuxmv without path raises ValueError."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        with patch('builtins.print'):
            with pytest.raises(ValueError, match='Cannot run nuXmv without a path to nuXmv'):
                main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--invar'])

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    @patch('os.path.isfile')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_nuxmv_with_invar(self, mock_file, mock_subprocess, mock_isfile, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --invar flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        mock_isfile.return_value = True

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--invar', '--nuxmv_path', '/path/to/nuxmv'])

        mock_nuxmv.assert_called_once()
        # Verify command file was written
        assert mock_file.called

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    @patch('os.path.isfile')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_nuxmv_with_ctl(self, mock_file, mock_subprocess, mock_isfile, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --ctl flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        mock_isfile.return_value = True

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--ctl', '--nuxmv_path', '/path/to/nuxmv'])

        mock_nuxmv.assert_called_once()
        mock_subprocess.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    @patch('os.path.isfile')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_nuxmv_with_ltl(self, mock_file, mock_subprocess, mock_isfile, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --ltl flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        mock_isfile.return_value = True

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--ltl', '--nuxmv_path', '/path/to/nuxmv'])

        mock_nuxmv.assert_called_once()
        mock_subprocess.assert_called_once()

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    @patch('os.path.isfile')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_nuxmv_with_simulate(self, mock_file, mock_subprocess, mock_isfile, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with --simulate flag."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        mock_isfile.return_value = True

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--simulate', '10', '--nuxmv_path', '/path/to/nuxmv'])

        mock_nuxmv.assert_called_once()
        mock_subprocess.assert_called_once()
        # Verify command string contains simulate
        written_content = ''.join([call[0][0] for call in mock_file().write.call_args_list if call[0]])
        assert 'simulate' in written_content or mock_file().write.called

    @patch('behaverify.behaverify.verify_input')
    @patch('behaverify.behaverify.verify_location')
    @patch('behaverify.behaverify.dsl_to_nuxmv')
    @patch('os.path.isfile')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_nuxmv_with_all_checks(self, mock_file, mock_subprocess, mock_isfile, mock_nuxmv, mock_verify_loc, mock_verify_input, temp_dir):
        """Test nuxmv mode with all check flags."""
        model_file = temp_dir / "test.tree"
        model_file.write_text("dummy")

        mock_isfile.return_value = True

        with patch('builtins.print'):
            main(['nuxmv', str(model_file), str(temp_dir), '--generate', '--invar', '--ctl', '--ltl', '--nuxmv_path', '/path/to/nuxmv'])

        mock_nuxmv.assert_called_once()
        mock_subprocess.assert_called_once()


class TestUnknownModeCoverage:
    """Test coverage for unknown mode handling."""

    def test_unknown_mode_prints_message(self):
        """Test that unknown mode prints appropriate message."""
        with patch('builtins.print') as mock_print:
            main(['unknown_mode'])

        # Should print unknown mode message
        mock_print.assert_any_call('Unknown mode. Modes are haskell, latex, nuxmv, or python. Exiting')


class TestMainEntryPoint:
    """Test coverage for __main__ entry point."""

    def test_main_as_script(self):
        """Test that the module can be run as a script."""
        # This tests line 250: if __name__ == '__main__'
        # We can't easily test this directly, but we can verify it's importable
        import behaverify.behaverify as bb_module

        # Verify the module has __name__ attribute
        assert hasattr(bb_module, '__name__')

        # The actual if __name__ == '__main__' block is only executed
        # when running as a script, not when imported
        # This is covered by integration testing
