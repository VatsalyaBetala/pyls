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
