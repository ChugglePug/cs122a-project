# project.py
# For development, this file should not be run directly
# and the main.py file should be used.
# This file is meant for the autograder

import sys
import mysql.connector


def main(args: list[str], connection_info: dict) -> None:
    connection = mysql.connector.connect(**connection_info)

    with connection as cnx:
        cursor = connection.cursor()
        pass


if __name__ == '__main__':
    autograder_connection = {
        'user': 'test',
        'password': 'password',
        'database': 'cs122a'
    }
    # TODO - Delete prior to submission
    raise RuntimeError('This was probably not meant to be run. Remove exception if so')
    main(sys.argv, autograder_connection)
