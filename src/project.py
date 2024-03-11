# project.py
# For development, this file should not be run directly
# and the main.py file should be used.
# This file is meant for the autograder

import sys
import mysql.connector
try:
    from src import (course, database, machine, parsing, queries, student)
except ModuleNotFoundError:
    import course
    import database
    import machine
    import parsing
    import queries
    import student
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

            database.create_database(cursor, database_name)

            # Remember to check what is supposed to be returned
            if args[1] == 'import':
                return_value = database.load_database(cursor, args[2])
            elif args[1] == 'insertStudent':
                return_value = student.add_student(cursor, args[2:])
            elif args[1] == 'addEmail':
                return_value = student.add_email(cursor, args[2:])
            elif args[1] == 'deleteStudent':
                return_value = student.delete_student(cursor, args[2:])
            elif args[1] == 'insertMachine':
                return_value = machine.insert_machine(cursor, args[2:])
            elif args[1] == 'insertUse':
                return_value = machine.insert_use_record(cursor, args[2:])
            elif args[1] == 'updateCourse':
                course_id, title = int(args[2]), args[3]
                return_value = course.update_course(cursor, course_id, title)
            elif args[1] == 'listCourse':
                UCINetID = args[2]
                return_value = course.list_course(cursor, UCINetID)
            elif args[1] == 'popularCourse':
                n = int(args[2])
                return_value = course.list_popular_courses(cursor, n)
            elif args[1] == 'adminEmails':
                machine_id = int(args[2])
                return_value = queries.adminEmails(cursor, machine_id)
            elif args[1] == 'activeStudent':
                return_value = queries.activeStudent(cursor, args[2:])
            elif args[1] == 'machineUsage':
                course_id = int(args[2])
                return_value = queries.machineUsage(cursor, course_id)

            cnx.commit()

        # something went wrong
        except (NotADirectoryError, mysql.connector.errors.ProgrammingError,
                mysql.connector.errors.IntegrityError) as e:
            return_value = False
            # tb = e.__traceback__
            # while tb is not None:
            #     print("File:", tb.tb_frame.f_code.co_filename, end=', ')
            #     print("Line:", tb.tb_lineno, end=', ')
            #     print("Function:", tb.tb_frame.f_code.co_name)
            #     tb = tb.tb_next
            cnx.rollback()

        # convert boolean value True to 'Success' and 'Fail otherwise'
        if isinstance(return_value, bool):
            print('Success' if return_value else 'Fail')
        # print comma separated tuple
        elif isinstance(return_value, tuple):
            print(parsing.format_table(return_value))
        # print all tuples
        else:
            for table in return_value:
                print(parsing.format_table(table))


if __name__ == '__main__':
    autograder_connection = {
        'user': 'test',
        'password': 'password',
        'database': 'cs122a'
    }
    print(sys.argv)
    main(sys.argv, autograder_connection)
