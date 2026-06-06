from pathlib import Path
import pytest
from obsidian_meta_tool.io.write import write_lines  # Replace with your actual import path


# ==============================================================================
# TESTS FOR OVERWRITE ONLY BEHAVIOR (DEFAULT BEHAVIOR)
# ==============================================================================

def test_write_lines_overwrites_successfully_when_file_exists(tmp_path):
    """Should succeed with overwrite_only=True if the file already exists on disk."""
    target_file = tmp_path / "existing.txt"
    target_file.write_text("old\n", encoding="utf-8")
    
    # Executing with stricter validation enabled
    write_lines(target_file, ["new\n"], overwrite_only=True)
    
    assert target_file.read_text(encoding="utf-8") == "new\n"


def test_write_lines_raises_error_when_file_does_not_exist(tmp_path):
    """Should raise FileNotFoundError if overwrite_only=True but the file is missing."""
    non_existent_file = tmp_path / "ghost_file.txt"
    
    # Validation: Ensure it raises the exact intended error
    with pytest.raises(FileNotFoundError) as exc_info:
        write_lines(non_existent_file, ["content\n"], overwrite_only=True)
        
    # Optional: Verify our custom error message is inside the exception
    assert "Target file does not exist for overwrite" in str(exc_info.value)
    # Ensure the file was NOT created as a side effect
    assert not non_existent_file.exists()


# ==============================================================================
# TESTS FOR CREATION ALLOWED
# ==============================================================================

def test_write_lines_creates_new_file_by_default(tmp_path):
    """Should successfully create a brand new file if it does not exist (default)."""
    target_file = tmp_path / "new_file.md"
    
    write_lines(target_file, ["hello\n"], overwrite_only=False)
    
    assert target_file.exists()
    assert target_file.read_text(encoding="utf-8") == "hello\n"