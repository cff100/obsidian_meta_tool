from pathlib import Path
import pytest

# Replace 'seu_modulo_read' with your actual file/module name
from obsidian_meta_tool.io.read import read_lines, read_file_paths


# ==============================================================================
# FIXTURES (Reusable Mock Data)
# ==============================================================================

@pytest.fixture
def sample_text_file(tmp_path):
    """Creates a temporary file containing a mix of paths and empty lines."""
    file_path = tmp_path / "test_paths.txt"
    content = (
        "/vault/notes/note1.md\n"
        "/vault/notes/note2.md\n"
        "   \n"  # Line with spaces to test trimming/stripping
        "/vault/notes/note3.md\n"  # Windows-style carriage return
    )
    file_path.write_text(content, encoding="utf-8")
    return file_path


# ==============================================================================
# TESTS FOR: read_lines
# ==============================================================================

def test_read_lines_preserves_newlines(sample_text_file):
    """Should read lines exactly as they are on disk, keeping trailing newlines."""
    lines = read_lines(sample_text_file, without_newline_character=False)
    
    assert len(lines) == 4
    assert lines[0] == "/vault/notes/note1.md\n"
    assert lines[2] == "   \n"
    assert lines[3] == "/vault/notes/note3.md\n"


def test_read_lines_strips_newlines(sample_text_file):
    """Should seamlessly strip both Unix (\\n) and Windows (\\r\\n) line endings."""
    lines = read_lines(sample_text_file, without_newline_character=True)
    
    assert len(lines) == 4
    assert lines[0] == "/vault/notes/note1.md"
    assert lines[1] == "/vault/notes/note2.md"
    assert lines[2] == "   "  # Keeps spaces but drops the newline character
    assert lines[3] == "/vault/notes/note3.md"


# ==============================================================================
# TESTS FOR: read_file_paths
# ==============================================================================

def test_read_file_paths_converts_to_path_objects(sample_text_file):
    """Should return a list of Path objects and automatically skip blank/empty entries."""
    paths = read_file_paths(sample_text_file)
    
    assert len(paths) == 3  # The whitespace-only line was cleanly filtered out
    assert all(isinstance(p, Path) for p in paths)
    assert paths[0] == Path("/vault/notes/note1.md")
    assert paths[1] == Path("/vault/notes/note2.md")
    assert paths[2] == Path("/vault/notes/note3.md")


# ==============================================================================
# TESTS FOR: Error Boundaries and System Exceptions
# ==============================================================================

def test_read_functions_raise_file_not_found():
    """Should let FileNotFoundError bubble up naturally if the target file does not exist."""
    missing_file = Path("/invalid/location/non_existent_file.txt")
    
    with pytest.raises(FileNotFoundError):
        read_lines(missing_file)
        
    with pytest.raises(FileNotFoundError):
        read_file_paths(missing_file)


def test_read_functions_raise_permission_error(sample_text_file, monkeypatch):
    """Should bubble up PermissionError instead of silently catching it and returning an empty list."""
    def mock_open_permission_error(*args, **kwargs):
        raise PermissionError("Mocked OS Access Denied")
        
    # Intercepting Path's native open call using monkeypatch
    monkeypatch.setattr(Path, "open", mock_open_permission_error)
    
    with pytest.raises(PermissionError):
        read_lines(sample_text_file)
        
    with pytest.raises(PermissionError):
        read_file_paths(sample_text_file)