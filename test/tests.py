# tests.py

import unittest
from src import project, parsing
import shlex

# used to test output to stdout
import contextlib
import io


# constants
my_connection = {
    'user': '',
    'password': '',
    'database': ''
}

# Tests were created with this folder in mind
# if the folder name changed, some test might have
# different results than expected
test_folder_name = 'test_data'


def _parse_arguments(s: str) -> list[str]:
    return shlex.split(s)


def _run_main(args: list[str]):
    project.main(args, my_connection)


def _reload_database():
    """Loads up the database to its default state. Assumes database exists"""
    # consume any output if necessary
    with contextlib.redirect_stdout(io.StringIO()):
        _run_main(['project.py', 'import', test_folder_name])


def _format_to_output(tables: list[tuple]) -> str:
    """
    Formats a table to meet printing requirements, should be used when the
    number of tables will be unknown
    :param tables: list of tuple formatted tables which are expected to print out
    :return:
    """
    output = ''
    for table in tables:
        output += f'{parsing.format_table(table)}\n'
    return output.strip()


def _format_email_list(emails: list[str]) -> str:
    """
    Formats a sequence of emails into its string format
    :param emails: list of emails
    :return: formatted emails for output
    """
    return ';'.join(sorted(emails))


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self._base_argv = ['project.py']
        _reload_database()

    @classmethod
    def tearDownClass(cls):
        # Sets the database to its original
        # state after tests are run
        _reload_database()

    def add_to_argv(self, args: str) -> list[str]:
        argv = self._base_argv.copy()
        for arg in _parse_arguments(args):
            argv.append(arg)
        return argv

    def test_import_form_existing_folder(self):
        args = self.add_to_argv('import test_data')
        expected_output = '20,6,5'

        # Redirects whatever is printed to console
        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        # Reads whatever was printed
        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_import_from_nonexistent_folder(self):
        args = self.add_to_argv('import nonexistent')
        expected_output = '0,0,0'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_inserting_students(self):
        args = self.add_to_argv('insertStudent testID lwong@uci.edi Lauren NULL Wong')
        expected_output = 'Success'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_student_twice(self):
        args = self.add_to_argv('insertStudent testID lwong@uci.edi Lauren NULL Wong')
        expected_output = 'Success\nFail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_student_failing_integrity_constraints(self):
        # A Students.UCINetID can not be null
        args = self.add_to_argv('insertStudent NULL lwong@uci.edi Lauren NULL Wong')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_delete_student(self):
        args = self.add_to_argv('deleteStudent mchang13')
        expected_output = 'Success'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_delete_nonexistent_student(self):
        args = self.add_to_argv('deleteStudent nonexistent')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_student_and_delete_after(self):
        args1 = self.add_to_argv('insertStudent testID lwong@uci.edi Lauren NULL Wong')
        args2 = self.add_to_argv('deleteStudent testID')
        expected_output = 'Success\nSuccess'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args1)
            _run_main(args2)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_delete_deleted_student(self):
        args = self.add_to_argv('deleteStudent mchang13')
        expected_output = 'Success\nFail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_machine(self):
        args = self.add_to_argv('insertMachine 102 test.com 192.168.10.5 Active "DBH 1011"')
        expected_output = 'Success'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_machine_twice(self):
        args = self.add_to_argv('insertMachine 102 test.com 192.168.10.5 Active "DBH 1011"')
        expected_output = 'Success\nFail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_machine_failing_integrity_constraints(self):
        # A Machines.MachineID can not be null
        args = self.add_to_argv('insertMachine NULL test.com 192.168.10.5 Active "DBH 1011"')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_use_record(self):
        args = self.add_to_argv('insertUse 1 mchang13 3 2023-01-09 2023-03-10')
        expected_output = 'Success'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_use_record_twice(self):
        args = self.add_to_argv('insertUse 1 mchang13 3 2023-01-09 2023-03-10')
        expected_output = 'Success\nFail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_use_record_failing_integrity_constraints1(self):
        # Null projectID
        args = self.add_to_argv('insertUse NULL mchang13 102 2023-01-09 2023-03-10')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_use_record_failing_integrity_constraints2(self):
        # Null UCINetID
        args = self.add_to_argv('insertUse 1 NULL 102 2023-01-09 2023-03-10')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_insert_use_record_failing_integrity_constraints3(self):
        # Null UCINetID
        args = self.add_to_argv('insertUse 1 mchang13 NULL 2023-01-09 2023-03-10')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_update_course_that_exists(self):
        args = self.add_to_argv('updateCourse 1 "My New Updated Course"')
        expected_output = 'Success'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_update_course_that_does_not_exist(self):
        args = self.add_to_argv('updateCourse 102 "My New Updated Course"')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_update_is_ok_when_not_giving_a_new_name(self):
        # The title of course 1 is already "computer graphics"
        args = self.add_to_argv('updateCourse 1 "Computer Graphics"')
        expected_output = 'Success'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_courses_attended_case_student_one(self):
        args = self.add_to_argv('listCourse mchang13')
        expected_output = _format_to_output(
            [(1, 'Computer Graphics', 'F23'),
             (4, 'Introduction to Data Management', 'S24'),
             (5, 'Project in Databases and Web Applications', 'S24')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_courses_attended_case_student_two(self):
        args = self.add_to_argv('listCourse jtrujillo2')
        expected_output = _format_to_output(
            [(4, 'Introduction to Data Management', 'S24')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_courses_attended_case_student_three(self):
        # Is in no projects and therefore no course
        args = self.add_to_argv('listCourse ageorge20')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_courses_attended_non_existent_student(self):
        # Is in no projects and therefore no course
        args = self.add_to_argv('listCourse nonexistent')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_popular_course_list_all(self):
        args = self.add_to_argv('popularCourse 5')
        expected_output = _format_to_output(
            [('4', 'Introduction to Data Management', '7'),
             ('5', 'Project in Databases and Web Applications', '5'),
             ('2', 'Computational Photography & Vision', '3'),
             ('3', 'Project in Computer Vision', '2'),
             ('1', 'Computer Graphics', '1')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_popular_course_list_top_course(self):
        args = self.add_to_argv('popularCourse 1')
        expected_output = _format_to_output(
            [('4', 'Introduction to Data Management', '7')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_popular_course_list_less_than_all(self):
        args = self.add_to_argv('popularCourse 3')
        expected_output = _format_to_output(
            [('4', 'Introduction to Data Management', '7'),
             ('5', 'Project in Databases and Web Applications', '5'),
             ('2', 'Computational Photography & Vision', '3')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_popular_course_cant_list_more_than_all(self):
        # Since there is only 5 courses, will list 5 instead of 10
        args = self.add_to_argv('popularCourse 10')
        expected_output = _format_to_output(
            [('4', 'Introduction to Data Management', '7'),
             ('5', 'Project in Databases and Web Applications', '5'),
             ('2', 'Computational Photography & Vision', '3'),
             ('3', 'Project in Computer Vision', '2'),
             ('1', 'Computer Graphics', '1')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_popular_course_cant_list_none(self):
        # Since there is only 5 courses, will list 5 instead of 10
        args = self.add_to_argv('popularCourse 0')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_popular_course_cant_list_negative(self):
        # Since there is only 5 courses, will list 5 instead of 10
        args = self.add_to_argv('popularCourse -1')
        expected_output = 'Fail'

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_admin_emails_expect_emails(self):
        args = self.add_to_argv('adminEmails 1')
        trujillo_emails = [
            'salazarmaria@yahoo.com',
            'jessicapadilla@gmail.com',
            'sallywalker@gmail.com',
            'udavis@hotmail.com',
            'jrodriguez@yahoo.com'
        ]

        murphy_emails = [
            'david17@yahoo.com',
            'turnerjessica@gmail.com'
        ]

        expected_output = _format_to_output(
            [('jtrujillo2', 'Jorge', 'NULL', 'Trujillo',
                _format_email_list(trujillo_emails)),
             ('rmurphy10', 'Richard', 'NULL', 'Murphy',
                _format_email_list(murphy_emails))]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_admin_emails_machine_with_no_admins(self):
        args = self.add_to_argv('adminEmails 5')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_admin_emails_invalid_machine_id(self):
        args = self.add_to_argv('adminEmails 102')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_active_students_can_find_students(self):
        args = self.add_to_argv('activeStudent 4 1 2020-01-01 2020-01-30')
        expected_output = _format_to_output(
            [('mchang13', 'Megan', 'NULL', 'Chang')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_active_students_nonexistent_machine(self):
        args = self.add_to_argv('activeStudent 102 1 2020-01-04 2020-01-05')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_active_students_from_too_far_date(self):
        args = self.add_to_argv('activeStudent 1 1 1970-01-01 1970-01-02')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_active_students_did_not_use_enough(self):
        args = self.add_to_argv('activeStudent 1 100 2020-01-04 2020-01-05')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_machine_usage_counts_usage(self):
        args = self.add_to_argv('machineUsage 1')
        expected_output = _format_to_output(
            [('6', 'compute3', '192.168.20.3', '0'),
             ('5', 'compute2', '192.168.20.2', '0'),
             ('4', 'compute1', '192.168.20.1', '0'),
             ('3', 'gpu3', '192.168.10.3', '0'),
             ('2', 'gpu2', '192.168.10.2', '0'),
             ('1', 'gpu1', '192.168.10.1', '1')]
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_machine_counts_nonexistent_machine(self):
        args = self.add_to_argv('machineUsage 102')
        expected_output = _format_to_output(
            []
        )

        with contextlib.redirect_stdout(io.StringIO()) as output:
            _run_main(args)

        self.assertEqual(output.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
