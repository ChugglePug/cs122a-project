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
    project.main(sys.argv, my_connection)