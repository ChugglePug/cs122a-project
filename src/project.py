# project.py
# For development, this file should not be run directly
# and the main.py file should be used.
# This file is meant for the autograder

import sys
import mysql.connector
from . import database as db
from typing import Any


def main(args: list[str], connection_info: dict[str, str]) -> Any:
    """
    Main process
    :param args:    sequence of args. Starts with the name of file
    :param connection_info: Required information which mysql.connector needs to run
    :return: Varies
    """

    # User might not have database created yet, so one is created if so
    database_name = connection_info['database']

    with mysql.connector.connect(**{key: value for key, value in connection_info.items() if key != 'database'}) as cnx:
        try:
            cnx.start_transaction()
            cursor = cnx.cursor()

            db.create_database(cursor, database_name)

            # TODO - implement functions here in elif chain
            # Remember to check what is supposed to be returned
            if args[1] == 'import':
                # TODO - check what return should be
                return_value = db.load_database(cursor, args[2])
            if args[1] == 'insertStudent':
                # TODO - do something
                pass
            if args[1] == 'addEmail':
                # TODO - do something
                pass
            if args[1] == 'deleteStudent':
                # TODO - do something
                pass
            if args[1] == 'insertMachine':
                # TODO - do something
                pass
            if args[1] == 'updateCourse':
                # TODO - do something
                pass
            if args[1] == 'listCourse':
                # TODO - do something
                pass
            if args[1] == 'popularCourse':
                # TODO - do something
                pass
            if args[1] == 'adminEmails':
                # TODO - do something
                pass
            if args[1] == 'activeStudent':
                # TODO - do something
                pass
            if args[1] == 'machineUsage':
                # TODO - do something
                pass

            # save any changes to database
            cnx.commit()

        # something went wrong
        except BaseException:
            cnx.rollback()




if __name__ == '__main__':
    autograder_connection = {
        'user': 'test',
        'password': 'password',
        'database': 'cs122a'
    }
    # TODO - Delete prior to submission
    main(sys.argv, autograder_connection)
