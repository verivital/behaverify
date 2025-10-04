import os
import tempfile
import pytest
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file for testing."""
    test_file = temp_dir / "test_file.txt"
    test_file.write_text("test content")
    return test_file


@pytest.fixture
def nested_temp_dir(temp_dir):
    """Create a nested directory structure for testing."""
    nested = temp_dir / "parent" / "child"
    nested.mkdir(parents=True)
    return nested
