import os
import sys


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
