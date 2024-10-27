import os
import sys
import termios
import tty
from enum import Enum


OR_CONTINUE = '||\n'
AND_CONTINUE = '&&\n'
BACKSLASH_CONTINUE = '\\\n'

EOF = ''


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


def move_cursor(x: int) -> None:
    """
    TODO: Write.
    """
    delay()
    if x > 0:
        os.write(1, f'\x1b[{x}C'.encode())
    elif x < 0:
        os.write(1, f'\x1b[{-x}D'.encode())


def delay():
    import time
    time.sleep(0)


def command_line() -> str:
    """
    TODO: Write.
    """
    default_settings = termios.tcgetattr(0)

    try:
        tty.setraw(0)

        position = 0
        buffer = bytearray()

        while True:
            match ch := os.read(0, 1):
                # EOF
                case b'':
                    return EOF

                # Enter
                case b'\r':
                    os.write(1, b'\r\n')
                    buffer.append(ord(b'\n'))
                    return buffer.decode('utf-8')

                # Ctrl-D
                case b'\x04':
                    if not buffer:
                        return EOF

                # Ctrl-C
                case b'\x03':
                    os.write(0, b'\r\n')
                    return '\n'

                # Backspace
                case b'\x7f':
                    if position > 0:
                        position -= 1
                        move_cursor(-1)
                        del buffer[position]

                # Escape
                case b'\x1b':
                    seq = os.read(0, 2).decode()
                    # Left arrow
                    if seq == r'[D':
                        if position > 0:
                            position -= 1
                            move_cursor(-1)
                    # Right arrow
                    elif seq == r'[C':
                        if position < len(buffer):
                            position += 1
                            move_cursor(+1)

                # Symbols
                case _:
                    buffer.insert(position, ord(ch))
                    position += 1
                    os.write(1, ch)

            # Update command line
            move_cursor(-position)
            os.write(1, '\x1b[K'.encode())
            os.write(1, buffer)
            move_cursor(position-len(buffer))
    finally:
        termios.tcsetattr(0, termios.TCSADRAIN, default_settings)


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
        line = command_line()
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
