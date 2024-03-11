# tests.py

import unittest
from src import project
import shlex

# used to test output to stdout
import contextlib
import io


# constants
my_connection = {
    'user': 'root',
    'password': 'J5m31t14G19',
    'database': 'cs122a_project'
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

    # TODO - check what real excepted output should be
    def test_import_from_nonexistent_folder(self):
        args = self.add_to_argv('import nonexistent')
        expected_output = 'Fail'

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


if __name__ == '__main__':
    unittest.main()
