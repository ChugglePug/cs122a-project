# course.py

from mysql.connector.abstracts import MySQLCursorAbstract


def update_course(cursor: MySQLCursorAbstract, course_id: int, title: str) -> bool:
    """
    Updates the title of a course.
    :param cursor: cursor object that is connected to the requested database
    :param args: The ID of the course to update and title
        follows the format of: [CourseId:int] [title:str]
    """
    try:
        query = """
            UPDATE Courses 
            SET title = %s 
            WHERE courseID = %s"""
        cursor.execute(query, (title, course_id))

        # Check if the course was actually updated by examining affected rows
        # (because the course being updated can be empty)
        if cursor.rowcount == 0:
            # Edge Case: Changing the course to the same name
            # The database reports no change, this should not be a fail case
            no_change_query = """
                    SELECT Title
                    FROM Courses
                    WHERE CourseID = %s
                    """
            cursor.execute(no_change_query, (course_id,))
            old_title = cursor.fetchall()[0][0]
            if old_title == title:
                return True
            # No rows were affected, meaning the course does not exist
            return False
        else:
            # Rows were affected, meaning the update was successful
            return True
    except Exception as e:
        # print(e)
        return False


def list_course(cursor: MySQLCursorAbstract, UCINetID: str):
    """
    Lists all unique courses that student attended
    :param cursor: cursor object that is connected to the requested database
    :param args: UCINetID
        follows the format of: [UCINetID:str]
    """
    # check if the user is a student
    exist_query = """
    SELECT *
    FROM Students
    WHERE UCINetID = %s
    """
    cursor.execute(exist_query, (UCINetID,))
    if len(cursor.fetchall()) == 0:
        return False

    query = """
    SELECT DISTINCT c.courseID, c.title, c.quarter
    FROM Courses c
    JOIN Projects p ON c.courseID = p.courseID
    JOIN StudentUseMachinesInProject u ON p.projectID = u.projectID
    WHERE u.StudentUCINetID = %s
    ORDER BY c.courseID ASC
    """
    cursor.execute(query, (UCINetID,))
    courses = list()
    for row in cursor.fetchall():
        courses.append(row)
    # if len(courses) == 0:
    #     return False
    return courses


def list_popular_courses(cursor: MySQLCursorAbstract, n: int):
    """
    Lists top N course that most students attended. Ordered.
    :param cursor: cursor object that is connected to the requested database
    :param args: Number of Courses, n
        follows the format of: [N:int]
    """
    # Edge Case: return 0 courses
    if n == 0:
        return []
    query = """
    SELECT c.courseID, c.title, COUNT(DISTINCT u.StudentUCINetID) as studentCount
    FROM Courses c
    JOIN Projects p ON c.courseID = p.courseID
    JOIN StudentUseMachinesInProject u ON p.projectID = u.projectID
    GROUP BY c.courseID
    ORDER BY studentCount DESC, c.courseID DESC
    LIMIT %s
    """
    cursor.execute(query, (n,))
    courses = list()
    for row in cursor.fetchall():
        courses.append(row)
    if len(courses) == 0:
        return False
    return courses
