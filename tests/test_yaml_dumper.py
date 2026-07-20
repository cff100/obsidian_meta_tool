import datetime
from pathlib import Path
import pytest
from ruamel.yaml import YAML

from obsidian_meta_tool.frontmatter.yaml_dumper import (
    DatetimeWithT,
    prepare_datetime_with_t,
    dump_yaml,
    decide_goal_path,
    replace_data
)

# Initialize a basic safe loader to verify dumper outputs natively
yaml_loader = YAML(typ="safe")


# ==============================================================================
# FIXTURES (Reusable Test Data)
# ==============================================================================

@pytest.fixture
def sample_frontmatter_dict():
    """Returns a standard frontmatter data dictionary."""
    return {
        "title": "My Obsidian Note",
        "tags": ["ideas", "coding"],
        "status": "draft"
    }


@pytest.fixture
def mock_dependencies(monkeypatch):
    """Mocks file I/O operations to avoid actual disk writes during testing."""
    read_lines_log = []
    write_lines_log = {}

    def mock_read_lines(path: Path) -> list[str]:
        return [
            "---\n",
            "title: Old Title\n",
            "status: archive\n",
            "---\n",
            "# Actual Content\n",
            "Some markdown body lines here.\n"
        ]

    def mock_replace_lines(lines, start, end, new_lines):
        # Emulates the behavior of cutting out old lines and splicing new ones
        updated = lines[:start] + new_lines + lines[end + 1:]
        return updated

    def mock_write_lines(path: Path, lines: list[str], create_parents: bool = True):
        write_lines_log[path] = lines

    # Injecting the mocked utilities into the module namespaces
    # Adjust target path strings to match your real folder infrastructure package names
    monkeypatch.setattr("obsidian_meta_tool.frontmatter.yaml_dumper.read_lines", mock_read_lines)
    monkeypatch.setattr("obsidian_meta_tool.frontmatter.yaml_dumper.replace_lines", mock_replace_lines)
    monkeypatch.setattr("obsidian_meta_tool.frontmatter.yaml_dumper.write_lines", mock_write_lines)

    return write_lines_log


# ==============================================================================
# TESTS FOR: Datetime Formatting & Mutation Prevention
# ==============================================================================

def test_prepare_datetime_with_t_prevents_mutation():
    """Ensures that wrapping tracking timestamps creates a deep copy and leaves the original untouched."""
    # Importing constants dynamically for precision setup
    from obsidian_meta_tool.config.constants import FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES
    
    if not FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES:
        pytest.skip("FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES is empty. Skipping tracking key verification.")

    test_key = FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES[0]
    test_date = datetime.datetime(2026, 6, 6, 12, 0, 0)
    
    original_dict = {test_key: test_date, "keep_int": 100}
    processed_dict = prepare_datetime_with_t(original_dict)

    # Verification: original dictionary state must not be corrupted/mutated
    assert isinstance(original_dict[test_key], datetime.datetime)
    assert original_dict[test_key] == test_date
    
    # Verification: processed copy must safely encapsulate custom class wrappers
    assert isinstance(processed_dict[test_key], DatetimeWithT)
    assert processed_dict[test_key].dt == test_date


def test_dump_yaml_formats_datetime_with_t():
    from obsidian_meta_tool.config.constants import FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES
    
    if not FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES:
        pytest.skip("Tracking keys empty.")

    test_key = FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES[0]
    raw_data = {test_key: datetime.datetime(2026, 6, 6, 15, 30, 45)}
    
    yaml_lines = dump_yaml(raw_data)
    yaml_output_string = "".join(yaml_lines)
    
    assert f'{test_key}: "2026-06-06T15:30:45"' in yaml_output_string


# ==============================================================================
# TESTS FOR: Obsidian Wikilinks Parsing
# ==============================================================================

def test_replace_single_with_double_quotes_on_wikilinks():
    """Confirms single quotes automatically switch over to double-quotes around embedded Obsidian Wikilinks."""
    cleaned_lines = dump_yaml({"related": "[[2026-06-06 Note]]"})
    cleaned_output = "".join(cleaned_lines)
        
    # Ajustado: Chave limpa e Wikilink com aspas duplas
    assert 'related: "[[2026-06-06 Note]]"' in cleaned_output


# ==============================================================================
# TESTS FOR: Core Execution Logic (Goal Paths & In-Place Replacement)
# ==============================================================================

def test_decide_goal_path_resolution():
    """Verifies targeted target routing logic patterns match expected returns cleanly."""
    origin = Path("/vault/note.md")
    custom_goal = Path("/vault/backups/note_backup.md")

    assert decide_goal_path(origin, None) == origin
    assert decide_goal_path(origin, custom_goal) == custom_goal


def test_replace_data_executes_properly(sample_frontmatter_dict, mock_dependencies):
    """Verifies frontmatter gets completely replaced inside boundaries using pre-calculated line indices."""
    write_logger = mock_dependencies
    origin = Path("my_note.md")
    
    # Pre-calculated line indices (excluding '---' markers based on previous tool logic rules)
    # The layout provided by mock_read_lines has the text data content on lines 1 and 2
    fm_start = 1
    fm_end = 2

    replace_data(
        origin_path=origin,
        new_frontmatter=sample_frontmatter_dict,
        fm_start=fm_start,
        fm_end=fm_end,
        goal_path=None
    )

    # Confirm write happened back to the original destination target
    assert origin in write_logger
    resulting_lines = write_logger[origin]

    # Verify boundaries: Structure check for the newly placed layout contents
    assert resulting_lines[0] == "---\n"
    assert resulting_lines[-2] == "# Actual Content\n" # Content stays safely preserved below boundary limits
    
    # Join output strings to verify serialization parsing matches safely
    serialized_yaml_content = "".join(resulting_lines[1:resulting_lines.index("---\n", 1)])
    parsed_back_dict = yaml_loader.load(serialized_yaml_content)
    
    assert parsed_back_dict["title"] == "My Obsidian Note"
    assert parsed_back_dict["status"] == "draft"
    assert parsed_back_dict["tags"] == ["ideas", "coding"]