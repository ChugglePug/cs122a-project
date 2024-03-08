# database.py

# Manages creation and loading of database

from pathlib import Path

from mysql.connector.abstracts import MySQLCursorAbstract
from .parsing import format_list, format_table


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


def _load_user(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'users.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Users (UCINetID, FirstName, MiddleName, LastName) 
            VALUES (%s, %s, %s, %s)""", values)
        count += 1
    return count


def _load_admin(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'admins.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Administrators (UCINetID) 
            VALUES (%s)""", values)
        count += 1
    return count


def _load_student(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'students.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Students (UCINetID) 
            VALUES (%s)""", values)
        count += 1
    return count


def _load_emails(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'emails.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO UserEmails (UCINetID, Email) 
            VALUES (%s, %s)""", values)
        count += 1
    return count


def _load_courses(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'courses.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Courses (CourseID, Title, Quarter) 
            VALUES (%s, %s, %s)""", values)
        count += 1
    return count


def _load_project(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'projects.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Projects (ProjectID, Name, Description, CourseID) 
            VALUES (%s, %s, %s, %s)""", values)
        count += 1
    return count


def _load_machine(cursor: MySQLCursorAbstract, folder_name) -> int:
    path = Path(__file__).parent.parent / folder_name / 'machines.csv'
    count = 0
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO Machines (MachineID, Hostname, IPAddress, OperationalStatus, Location) 
            VALUES (%s, %s, %s, %s, %s)""", values)
        count += 1
    return count


def _load_use(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'use.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO StudentUseMachinesInProject (ProjectID, StudentUCINetID, MachineID, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s)""", values)


def _load_manage(cursor: MySQLCursorAbstract, folder_name):
    path = Path(__file__).parent.parent / folder_name / 'manage.csv'
    for values in _load_values_from_file(path):
        cursor.execute("""
            INSERT INTO AdministratorManageMachines (AdministratorUCINetID, MachineID) 
            VALUES (%s, %s)""", values)


def load_database(cursor: MySQLCursorAbstract, folder_name: str) -> str:
    """
    Loads the data of the folder into the database for use
    :param cursor: cursor object
    :param folder_name: Folder to read from.
    :return:
    """
    # Default value for counts of nothing was added
    counts = [0, 0, 0]

    # do nothing if not a dir
    if not (Path(__file__).parent.parent / folder_name).is_dir():
        raise NotADirectoryError

    # Drops the tables currently existing in the database
    _drop_all_tables(cursor)
    _load_schema(cursor)

    # some values are not used, but are counted anyway
    user_count = _load_user(cursor, folder_name)
    student_count = _load_student(cursor, folder_name)
    email_count = _load_emails(cursor, folder_name)
    admin_count = _load_admin(cursor, folder_name)
    course_count = _load_courses(cursor, folder_name)
    project_count = _load_project(cursor, folder_name)
    machine_count = _load_machine(cursor, folder_name)
    _load_use(cursor, folder_name)
    _load_manage(cursor, folder_name)

    # Some error when reading

    counts = [user_count, machine_count, course_count]
    return format_table(counts)


def create_database(cursor: MySQLCursorAbstract, database_name):
    """Create a database if it does not exist yet"""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.execute(f"USE {database_name}")


def _load_values_from_file(path: Path) -> list[str]:
    with open(path, 'r') as f:
        for line in f.readlines():
            values = line.strip().split(',')
            yield format_list(values)
