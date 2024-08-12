import pytest
from datetime import datetime
from pyls import gather_file_info, format_file_info, display_results

# Sample data
FILE_INFO_LIST = [
    {"filename": "file.txt", "filetype": "f", "modtime": datetime.now(), "filesize": 1024},
    {"filename": "script.sh", "filetype": "x", "modtime": datetime.now(), "filesize": 2048},
    {"filename": "directory", "filetype": "d", "modtime": datetime.now(), "filesize": 0}
]

# Test for gather_file_info
def test_gather_file_info():
    """Test gathering file info from the current directory."""
    results = gather_file_info(".", False, False)  # Reads from the current directory
    assert isinstance(results, list), "Expected a list of dictionaries"
    assert all(isinstance(item, dict) for item in results), "Each item should be a dictionary"

# Tests for format_file_info
def test_format_file_info_long_format():
    """Test formatting file info with the long format flag."""
    formatted = format_file_info(FILE_INFO_LIST, True, False)
    assert all(isinstance(line, str) for line in formatted), "Each line of formatted output should be a string."
    assert "1024" in formatted[0], "The formatted output should include the file size for the first file."

def test_format_file_info_filetype():
    """Test formatting file info with the filetype flag."""
    formatted = format_file_info(FILE_INFO_LIST, False, True)
    assert formatted[0] == "file.txt", "Regular files should not have a type indicator appended."
    assert "*" in formatted[1], "Executable files should be marked with an asterisk (*)."
    assert "/" in formatted[2], "Directories should be marked with a slash (/)."
    assert formatted[2].endswith("/"), "Directory should end with a slash (/) to indicate it is a directory."

def test_format_file_info_long_format_and_filetype():
    """Test format_file_info with both long_format and filetype flags enabled."""
    formatted = format_file_info(FILE_INFO_LIST, True, True)
    
    # Check the first entry for long format details
    assert isinstance(formatted[0], str), "Output should be a string."
    assert "1024" in formatted[0], "The file size should be included in the output."
    assert formatted[0].startswith(datetime.now().strftime('%Y-%m-%d')), "The modification time should be included in long format output."
    
    # Check that the first entry has no filetype indicator (regular file)
    assert formatted[0].endswith("file.txt"), "Regular file should not have a type indicator appended."
    
    # Check that the second entry (script.sh) is formatted correctly with both long format and filetype indicator
    assert "2048" in formatted[1], "The file size should be included in the output for the executable file."
    assert formatted[1].endswith("script.sh *"), "Executable files should be marked with an asterisk (*) in the long format output."

def test_display_results(capsys):
    """ Test display_results by capturing output and verifying content. """
    display_results(["test line"])
    captured = capsys.readouterr()
    assert "test line" in captured.out, "The display function should output the string exactly."
