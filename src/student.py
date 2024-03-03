# student.py

# manages the insertion of students and their emails

from pathlib import Path
from mysql.connector.abstracts import MySQLCursorAbstract
from .parsing import format_list


def add_student(cursor: MySQLCursorAbstract, args: list[str]):
    """
    Adds a student into the loaded database
    :param cursor: cursor object that is connected to the requested database
    :param args: sequence of information for the student.
        follows the format of: [UCINetID:str] [email:str] [First:str] [Middle:str] [Last:str]
    :return:
    """
    # Places the information into User table and then creates Student
    user_stmt = """
        INSERT INTO User
        (UCINetID, firstName, middleName, lastName)
        VALUES
        (%s, %s, %s, %s)
    """
    user_email_stmt = """
        INSERT INTO UserEmails
        (UCINetID, email)
        VALUES
        (%s, %s)    
    """
    student_stmt = """
        INSERT INTO Student
        (UCINetID)
        VALUES
        (%s)
    """
    # all but arg[1] (email)
    cursor.execute(user_stmt, format_list([args[i] for i in range(len(args)) if i != 1]))
    # offloads to add_email
    add_email(cursor, args[:2])
    # should be passed as a list
    cursor.execute(student_stmt, format_list(args[:1]))


def add_email(cursor: MySQLCursorAbstract, args: list[str]):
    """
    Adds an email to the associated UCINetID
    :param cursor: cursor object that is connected to the requested database
    :param args: sequence of information for the student.
        follows the format of: [UCINetID:str] [email:str]
    :return:
    """
    user_email_stmt = """
            INSERT INTO UserEmails
            (UCINetID, email)
            VALUES
            (%s, %s)    
        """
    cursor.execute(user_email_stmt, format_list(args))



