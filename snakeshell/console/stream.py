import os
import sys


STDIN = 0
STDOUT = 1
STDERR = 2


def write(data: str) -> None:
    """
    Writes text to the console without a newline at the end.
    """
    if sys.stdin.isatty():
        os.write(STDOUT, data.encode('utf-8'))


def writeline(data: str) -> None:
    """
    Writes a line of text to the console, followed by an end character.
    """
    write(data + '\n')


def read(n: int) -> str:
    """
    Read N bytes from the console.
    """
    return os.read(STDIN, n).decode('utf-8')


def readline() -> str:
    """
    Read a line of text from the console.
    """
    return read(1024)


def error(msg: str) -> None:
    """
    Writes an error message to the standard error output.
    """
    color_msg = '\033[31msnake: ' + msg + '\033[0m\n'
    os.write(STDERR, color_msg.encode('utf-8'))
