import argparse
import os
from datetime import datetime

# Create the parser

epilog = """
Examples:
  Basic usage to list files in the current directory:
    $ pyls

  To list files in a specific directory:
    $ pyls /path/to/directory

  To list files with detailed information (long format):
    $ pyls -l
    $ pyls --long-format /path/to/directory

  To list files with type indicators:
    $ pyls -F
    $ pyls --filetype /path/to/directory

  Combine options to display detailed information and file type indicators:
    $ pyls -lF /path/to/directory
    $ pyls --long-format --filetype /path/to/directory

The 'pyls' tool is designed to mimic some functionalities of the unix 'ls' command, for simplicity and use in Python. 
"""

def gather_file_info(dirname, long_format, filetype):
    """
    Collects detailed information about each file and directory within the given directory.
    
    Args:
        dirname (str): Directory path to list contents from.
        long_format (bool): Flag to indicate if detailed information like file size and modification time should be included.
        filetype (bool): Flag to indicate if file type indicators (e.g., directory or executable) should be appended.
    
    Returns:
        list of dict: Each dictionary contains details about a file or directory (e.g., name, type, modification time, size).
    """
    
    assert isinstance(dirname, str), f"Expected dirname to be a string, got {type(dirname)}"
    assert isinstance(long_format, bool), f"Expected long_format to be a boolean, got {type(long_format)}"
    assert isinstance(filetype, bool), f"Expected filetype to be a boolean, got {type(filetype)}"
    
    results = []
    try:
        for entry in os.scandir(dirname):
            filetype_char = 'f'
            if entry.is_dir(follow_symlinks=False):
                filetype_char = 'd'  # It's a directory
            elif os.access(entry.path, os.X_OK):
                filetype_char = 'x'  # It's executable

            file_info = {
                "filename": entry.name,
                "filetype": filetype_char,
                "modtime": datetime.fromtimestamp(entry.stat().st_mtime),
                "filesize": entry.stat().st_size if not entry.is_dir(follow_symlinks=False) else 0
            }
            
            assert isinstance(file_info['modtime'], datetime), "Modification time should be a datetime object"
            assert isinstance(file_info['filesize'], int), "File size should be an integer"
            results.append(file_info)
            
    except Exception as e:
        print(f"Error accessing directory {dirname}: {e}")

    return results


def format_file_info(file_info_list, long_format, filetype):
    """
    Formats the file information into strings based on the specified flags for display.
    
    Args:
        file_info_list (list of dict): File information to format, as returned by `gather_file_info`.
        long_format (bool): True if additional file details should be shown.
        filetype (bool): True if file type indicators are to be appended to file names.
    
    Returns:
        list of str: Formatted file information strings ready for display.
    """
    # Assert to check the input types
    assert isinstance(file_info_list, list), "Expected file_info_list to be a list"
    assert all(isinstance(info, dict) for info in file_info_list), "All items in file_info_list should be dictionaries"
    assert isinstance(long_format, bool), "Expected long_format to be a boolean"
    assert isinstance(filetype, bool), "Expected filetype to be a boolean"
    
    
    formatted_lines = []
    for file_info in file_info_list: 
        # Filename
        line = file_info['filename']
        
        # If long format
        if long_format: 
            assert isinstance(file_info['modtime'], datetime), "modtime should be a datetime object"  # checks if the modtime field in each file information dictionary (file_info) is an instance of the `datetime` class.
            assert isinstance(file_info['filesize'], int), "filesize should be an integer" # checks if the if the filesize field in each file information dictionary is an integer.
            
            line = f"{file_info['modtime'].strftime('%Y-%m-%d %H:%M:%S')} {str(file_info['filesize']).rjust(6)} {line}"
            
        # If filetype
        if filetype:
            line += ' *' if file_info['filetype'] == 'x' else ''
            line += ' /' if file_info['filetype'] == 'd' else ''

        formatted_lines.append(line)    
    
    return formatted_lines
    
    
def display_results(lines):
    """
    Outputs the formatted file information strings to the console.
    
    Args:
        formatted_lines (list of str): Strings that have been formatted for display.
    """
    for line in lines:
        print(line)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
    prog='pyls',
    description='Lists files in the given directory',
    epilog=epilog,
    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('dirname',
                        help="Name of directory to list the contents of",
                        nargs='?',
                        default=".")

    parser.add_argument('-l', '--long-format',
                        help="Presents more details about files in columnar format",
                        action='store_true')

    parser.add_argument('-F', '--filetype',
                        help="Adds an extra character to the end of the printed filename that indicates its type.",
                        action='store_true')

    args = parser.parse_args()

    # Use the parsed arguments in your functions
    file_info_list = gather_file_info(args.dirname, args.long_format, args.filetype)
    formatted_lines = format_file_info(file_info_list, args.long_format, args.filetype)
    display_results(formatted_lines)