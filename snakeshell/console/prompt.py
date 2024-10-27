import os

from snakeshell.console.stream import write
from snakeshell.console.cursor import set_cursor, CursorType
from snakeshell.console.command_line import interactive_readline


OR_CONTINUE = '||\n'
AND_CONTINUE = '&&\n'
BACKSLASH_CONTINUE = '\\\n'


def prompt_msg() -> str:
    """
    Generate a prompt message indicating the current working directory.
    """
    dirname = os.getcwd()
    homedir = os.path.expanduser('~')
    if dirname.startswith(homedir):
        dirname = '~' + dirname[len(homedir) :]
    return f'\033[34;1m{dirname}\033[0m $ '


def prompt() -> str:
    """
    Displays a prompt message to the user and requests
    their input, returning the user's input line.
    """
    write(prompt_msg())
    set_cursor(CursorType.THICK)

    command = ''
    completed = False

    while not completed:
        line = interactive_readline()
        command += line
        if command.endswith(BACKSLASH_CONTINUE):
            write('> ')
            command = command[:-2]
            continue
        if command.endswith(AND_CONTINUE) or command.endswith(OR_CONTINUE):
            write('> ')
            command = command[:-1]
            command += ' '
            continue
        completed = True

    set_cursor(CursorType.DEFAULT)
    return command
