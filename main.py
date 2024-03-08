# main.py
# This file should not be committed with personal information
# make sure to delete any personal information if needed

from src import project


def _parse_arguments(input_string: str) -> list[str]:
    """
    Parses arguments similar to a command line
    :param input_string: unformatted string
    :return:
    """

    args = input_string.split()
    parsed_args = []
    current_arg = ""
    in_quotes = False

    for arg in args:
        if '"' in arg:
            if in_quotes:
                current_arg += " " + arg.strip('"')
                parsed_args.append(current_arg)
                current_arg = ""
                in_quotes = False
            else:
                current_arg += arg.strip('"')
                in_quotes = True
        elif in_quotes:
            current_arg += " " + arg
        else:
            parsed_args.append(arg)

    return parsed_args


# personal information should go here
my_connection = {
    'user': '',
    'password': '',
    'database': ''
}

if __name__ == '__main__':
    input_args = ['project.py']
    # Error checking is done somewhere else
    for arg in _parse_arguments(input('python3 project.py ')):
        input_args.append(arg)
    project.main(input_args, my_connection)
