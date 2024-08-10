import argparse
import os

# Create the parser
parser = argparse.ArgumentParser(
    prog='pyls',
    description='Lists files in the given directory',
    epilog="That's it!"
)

# Add an argument
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

def main(args):
    """
    Main function that gathers and displays the list of files and directories
    in the specified directory.
    
    Args:
        args: Command line arguments containing the directory name.
    """
    results = gather_inputs(args.dirname)
    display_results(results)

def gather_inputs(dirname):
    """
    Gathers the listing of files and directories from the specified directory.
    
    Args:
        dirname (str): The directory whose contents are to be listed.
    
    Returns:
        list of str: A list containing the names of files and directories.
    """
    try:
        return os.listdir(dirname)
    except Exception as e:
        print(f"Error accessing directory: {e}")
        return []

def display_results(results):
    """
    Displays the results of the file listing.
    
    Args:
        results (list of str): A list containing the names of files and directories.
    """
    for entry in results:
        print(entry)

if __name__ == '__main__':
    main(args)
