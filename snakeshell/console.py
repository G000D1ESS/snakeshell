import os
import sys
from enum import Enum


OR_CONTINUE = '||\n'
AND_CONTINUE = '&&\n'
BACKSLASH_CONTINUE = '\\\n'


class CursorType(Enum):
    THICK = '\x1b[5 q'
    THIN = '\x1b[3 q'
    DEFAULT = '\x1b[0 q'


def write(data: str) -> None:
    """
    Writes text to the console without a newline at the end.
    """
    if sys.stdin.isatty():
        os.write(1, data.encode('utf-8'))


def writeline(data: str) -> None:
    """
    Writes a line of text to the console, followed by an end character.
    """
    write(data + '\n')


def readline() -> str:
    """
    Read a line of text from the console.
    """
    return os.read(0, 1024).decode('utf-8')


def error(msg: str) -> None:
    """
    Writes an error message to the standard error output.
    """
    color_msg = '\033[31msnake: ' + msg + '\033[0m\n'
    os.write(2, color_msg.encode('utf-8'))


def set_cursor(cursor_type: CursorType) -> None:
    """
    Sets the cursor style in the console to the specified type.
    """
    change_cursor_escape_sequence = str(cursor_type.value)
    write(change_cursor_escape_sequence)


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
        line = readline()
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
