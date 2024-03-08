# student.py

# manages the insertion of students and their emails


import mysql.connector.errors
from mysql.connector.abstracts import MySQLCursorAbstract
from .parsing import format_list


def add_student(cursor: MySQLCursorAbstract, args: list[str]) -> bool:
    """
    Adds a student into the loaded database
    :param cursor: cursor object that is connected to the requested database
    :param args: sequence of information for the student.
        follows the format of: [UCINetID:str] [email:str] [First:str] [Middle:str] [Last:str]
    :return:
    """
    # Places the information into User table and then creates Student
    user_stmt = """
        INSERT INTO Users
        (UCINetID, FirstName, MiddleName, LastName)
        VALUES
        (%s, %s, %s, %s)
    """
    student_stmt = """
        INSERT INTO Students
        (UCINetID)
        VALUES
        (%s)
    """
    try:
        # all but arg[1] (email)
        cursor.execute(user_stmt, format_list([args[i] for i in range(len(args)) if i != 1]))
        # offloads to add_email
        add_email(cursor, args[:2])
        # should be passed as a list
        cursor.execute(student_stmt, format_list(args[:1]))
    except mysql.connector.errors.ProgrammingError:
        return False

    return True


def add_email(cursor: MySQLCursorAbstract, args: list[str]) -> bool:
    """
    Adds an email to the associated UCINetID
    :param cursor: cursor object that is connected to the requested database
    :param args: sequence of information for the student.
        follows the format of: [UCINetID:str] [email:str]
    :return:
    """
    user_email_stmt = """
            INSERT INTO UserEmails
            (UCINetID, Email)
            VALUES
            (%s, %s)    
        """
    cursor.execute(user_email_stmt, format_list(args))
    return True


def delete_student(cursor: MySQLCursorAbstract, args: list[str]) -> bool:
    indicator = False
    find_user = """
        SELECT *
        FROM Users
        WHERE UCINetID = (%s)
    """
    cursor.execute(find_user, format_list([args[0]]))
    results = cursor.fetchall()
    for result in results:
        if result[0] == args[0]:
            # print("found user")
            indicator = True
            break
    if not indicator:
        # print("delete unsuccessful")
        return indicator
    else:
        delete_user_stmt = """
            DELETE FROM Users U
            WHERE U.UCINetID = (%s)
            """
        delete_student_stmt = """
            DELETE FROM Students S
            WHERE S.UCINetID = (%s)
        """
        cursor.execute(delete_student_stmt, format_list(args))
        cursor.execute(delete_user_stmt, format_list(args))
        # print("delete user successfully !")
        return indicator
