# main.py
# This file should not be committed with personal information
# make sure to delete any personal information if needed

import sys
from src import project


# personal information should go here
my_connection = {
    'user': '',
    'password': '',
    'database': ''
}

if __name__ == '__main__':
    input_args = ['project.py']
    # Error checking is done somewhere else
    for arg in input('python3 project.py ').split():
        input_args.append(arg)
    project.main(input_args, my_connection)