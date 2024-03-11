# queries.py

from mysql.connector.abstracts import MySQLCursorAbstract
from mysql.connector import DATETIME
try:
    from src.parsing import format_list
except ImportError:
    from parsing import format_list


def adminEmails(cursor: MySQLCursorAbstract, machineId: int):
    select_statement = """
            SELECT U.UCINETId, firstName, middleName, lastName
            FROM Users AS U
            INNER JOIN Administrators AS A
            ON A.UCINetID = U.UCINetID
            INNER JOIN AdministratorManageMachines AS AMM
            ON AMM.AdministratorUCINetID = A.UCINetID
            WHERE AMM.machineID = (%s)
    """
    cursor.execute(select_statement, [machineId])
    admins = cursor.fetchall()
    id_list = []
    table = []
    for obj in admins:
        if obj[0] not in id_list:
            id_list.append(obj[0])
            statement = """
                    SELECT email
                    FROM UserEmails
                    WHERE UserEmails.UCINetID = %s
            """
            cursor.execute(statement, [obj[0]])
            # emails = ""
            emails = cursor.fetchall()
            # while (email != None):
            #     emails += f"{email[0]};"
            #     email = cursor.fetchone()
            # obj += (emails,)
            obj += (';'.join([email[0] for email in emails]),)
            table.append(obj)
    return table


def activeStudent(cursor: MySQLCursorAbstract, args: list[str]):
    select_statement = """
            SELECT Users.UCINetID, firstName, middleName, lastName
            FROM Users
            WHERE Users.UCINetID IN(
            SELECT StudentUseMachinesInProject.StudentUCINetID
            FROM StudentUseMachinesInProject
            WHERE machineId = %s AND startDate >= %s AND endDate <= %s
            GROUP BY StudentUseMachinesInProject.StudentUCINetID
            HAVING Count(*) >= %s
            )
            ORDER BY Users.UCINetID ASC
    """
    organized_args = format_list(args)
    # Format to meet [machineID, startDate, endDate, N]
    organized_args.append(organized_args.pop(1))
    cursor.execute(select_statement, organized_args)
    results = cursor.fetchall()
    if len(results) == 0:
        return False
    return results


def machineUsage(cursor: MySQLCursorAbstract, courseID: int):
    statement = """
            SELECT M.machineID, hostname, IPAddress, IF(M.machineID = S.machineID AND Count(S.machineID) > 0, Count(S.machineID), 0)
            FROM Machines M, StudentUseMachinesInProject S
            INNER JOIN Projects AS P ON P.projectID = S.projectID
            WHERE P.courseID = %s
            GROUP BY M.machineID, S.machineID
            ORDER BY M.machineID DESC
    """
    cursor.execute(statement, [courseID])
    results = cursor.fetchall()
    if len(results) == 0:
        return False
    return results
            
