# database.py

# Manages creation and loading of database
# TODO - ask where the test folders will be located

from pathlib import Path
from mysql.connector.abstracts import MySQLCursorAbstract
from .parsing import format_list


def _drop_all_tables(cursor):
    """Drops all tables from database"""
    try:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("SHOW TABLES")
        for table in cursor.fetchall():
            table_name = table[0]
            cursor.execute(f"DROP TABLE {table_name}")
    finally:
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def _load_schema(cursor):
    """Loads Schema"""
    path = Path(__file__).parent / 'schema.sql'
    with open(path, 'r') as f:
        for query in f.read().split(';')[:-1]:
            cursor.execute(query)


def _load_user(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'users.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO User (UCINetID, firstName, middleName, lastName) 
            VALUES (%s, %s, %s, %s)""", values)


def _load_admin(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'admins.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Administrator (UCINetID) 
            VALUES (%s)""", values)


def _load_student(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'students.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Student (UCINetID) 
            VALUES (%s)""", values)


def _load_emails(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'emails.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO UserEmails (UCINetID, email) 
            VALUES (%s, %s)""", values)


def _load_courses(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'courses.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Course (courseID, title, quarter) 
            VALUES (%s, %s, %s)""", values)


def _load_project(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'projects.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Project (projectID, name, description, courseID) 
            VALUES (%s, %s, %s, %s)""", values)


def _load_machine(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'machines.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Machine (machineID, hostname, IPAddress, operationalStatus, location) 
            VALUES (%s, %s, %s, %s, %s)""", values)


def _load_use(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'use.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO studentUse (projectID, UCINetID, machineID, startDate, endDate)
            VALUES (%s, %s, %s, %s, %s)""", values)


def _load_manage(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'manage.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO manages (UCINetID, machineID) 
            VALUES (%s, %s)""", values)


def load_database(cursor: MySQLCursorAbstract, folder_name: str):
    """
    Loads the data of the folder into the database for use
    :param cursor: cursor object
    :param folder_name: Folder to read from. Assumes all files in folder are existent and readable
    :return:
    """
    # Drops the tables currently existing in the database
    _drop_all_tables(cursor)
    _load_schema(cursor)

    _load_user(cursor, folder_name)
    _load_student(cursor, folder_name)
    _load_emails(cursor, folder_name)
    _load_admin(cursor, folder_name)
    _load_courses(cursor, folder_name)
    _load_project(cursor, folder_name)
    _load_machine(cursor, folder_name)
    _load_use(cursor, folder_name)
    _load_manage(cursor, folder_name)


def create_database(cursor: MySQLCursorAbstract, database_name):
    """Create a database if it does not exist yet"""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.execute(f"USE {database_name}")


def _load_values_from_file(path: Path) -> list[str]:
    with open(path, 'r') as f:
        for line in f.readlines():
            values = line.strip().split(',')
            # Replace 'NULL' strings with None for NULL values in a case-insensitive manner
            yield format_list(values)
