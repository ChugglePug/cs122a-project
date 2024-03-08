# machine.py

from mysql.connector.abstracts import MySQLCursorAbstract
from .parsing import format_list


def insert_machine(cursor: MySQLCursorAbstract, args: list[str]):
    indicator = False
    find_machine_stmt = """
        SELECT M.MachineID
        FROM Machines M
    """
    cursor.execute(find_machine_stmt)
    results = cursor.fetchall()
    for result in results:
        if result[0] == int(args[0]):
            print("found machine")
            indicator = True
            break
    if indicator:
        print("machine record already exists!")
        return indicator
    else:
        insert_machine_stmt = """
            INSERT INTO Machines
            (MachineID, Hostname, IPAddress, OperationalStatus, Location)
            VALUES
            (%s,%s,%s,%s,%s);
        """
        cursor.execute(insert_machine_stmt, format_list(args))
        print("Add Machine Record Successfully !")
        return indicator


def insert_use_record(cursor: MySQLCursorAbstract, args: list[str]):
    indicator1 = False
    indicator2 = False
    indicator3 = False
    find_machine_stmt = """
        SELECT M.machineID
        FROM Machines M
    """
    cursor.execute(find_machine_stmt)
    results = cursor.fetchall()
    for result in results:
        if result[0] == int(args[2]):
            indicator1 = True
            break
    find_student_stmt = """
        SELECT S.UCINetID
        FROM Students S
    """
    cursor.execute(find_student_stmt)
    results = cursor.fetchall()
    for result in results:
        if result[0] == args[1]:
            indicator2 = True
            break
    find_project_stmt = """
        SELECT P.projectID
        FROM Projects P
    """
    cursor.execute(find_project_stmt)
    results = cursor.fetchall()
    for result in results:
        if result[0] == int(args[0]):
            indicator3 = True
            break
    if indicator1 and indicator2 and indicator3:
        insert_user_record_stmt = """
            INSERT INTO StudentUseMachinesInProject
            (ProjectID, StudentUCINetID, MachineID, StartDate, EndDate)
            VALUES
            (%s,%s, %s, %s, %s)
        """
        cursor.execute(insert_user_record_stmt, format_list(args))
        print("Insert Student Use Record Successfully !")
        return True

    else:
        return False
