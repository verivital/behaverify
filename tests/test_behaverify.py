import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile

# Add src to path to allow imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import the functions we want to test from the source
from behaverify.behaverify import verify_location, verify_input


class TestVerifyLocation:
    """Tests for verify_location function."""

    def test_verify_location_creates_parent_directory(self, temp_dir):
        """Test that verify_location creates parent directory when it doesn't exist."""
        output_file = temp_dir / "new_dir" / "output.txt"
        verify_location(None, str(output_file), False)
        assert output_file.parent.exists()
        assert output_file.parent.is_dir()

    def test_verify_location_raises_error_when_file_exists_without_overwrite(self, temp_file):
        """Test that verify_location raises error when file exists and overwrite is False."""
        with pytest.raises(FileExistsError, match="already exists"):
            verify_location(None, str(temp_file), False)

    def test_verify_location_allows_existing_file_with_overwrite(self, temp_file):
        """Test that verify_location allows existing file when overwrite is True."""
        # Should not raise an exception
        verify_location(None, str(temp_file), True)

    def test_verify_location_raises_error_when_parent_is_not_directory(self, temp_file):
        """Test that verify_location raises error when parent exists but is not a directory."""
        # Create a path where parent is a file, not a directory
        invalid_path = str(temp_file) + "/child.txt"
        with pytest.raises(FileExistsError, match="is not a directory"):
            verify_location(None, invalid_path, False)

    def test_verify_location_directory_mode_creates_directory(self, temp_dir):
        """Test that verify_location creates directory in directory mode."""
        verify_location("output_dir", str(temp_dir), False)
        assert (temp_dir / "output_dir").exists()
        assert (temp_dir / "output_dir").is_dir()

    def test_verify_location_directory_mode_raises_error_when_exists_without_overwrite(self, temp_dir):
        """Test that verify_location raises error in directory mode when directory exists."""
        output_dir = temp_dir / "existing_dir"
        output_dir.mkdir()
        with pytest.raises(FileExistsError, match="contains an element named"):
            verify_location("existing_dir", str(temp_dir), False)

    def test_verify_location_directory_mode_allows_existing_with_overwrite(self, temp_dir):
        """Test that verify_location allows existing directory with overwrite."""
        output_dir = temp_dir / "existing_dir"
        output_dir.mkdir()
        # Should not raise an exception
        verify_location("existing_dir", str(temp_dir), True)

    def test_verify_location_directory_mode_raises_error_when_location_is_not_directory(self, temp_file):
        """Test that verify_location raises error when location exists but is a file."""
        with pytest.raises(FileExistsError, match="cannot be used as it exists and is not a folder"):
            verify_location("some_dir", str(temp_file), False)


class TestVerifyInput:
    """Tests for verify_input function."""

    def test_verify_input_succeeds_with_existing_file(self, temp_file):
        """Test that verify_input succeeds when file exists."""
        # Should not raise an exception
        verify_input(str(temp_file))

    def test_verify_input_raises_error_when_file_does_not_exist(self, temp_dir):
        """Test that verify_input raises error when file doesn't exist."""
        nonexistent_file = temp_dir / "nonexistent.txt"
        with pytest.raises(FileNotFoundError, match="could not be found"):
            verify_input(str(nonexistent_file))

    def test_verify_input_raises_error_when_path_is_directory(self, temp_dir):
        """Test that verify_input raises error when path is a directory."""
        with pytest.raises(FileNotFoundError):
            verify_input(str(temp_dir))
