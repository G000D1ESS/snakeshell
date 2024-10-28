import sys
import termios
import tty

from snakeshell import console
from snakeshell.console.cursor import move_cursor, set_cursor, CursorType

EOF = ''


def command_line() -> str:
    """
    Reads a line of input, detecting if it is a TTY (interactive) input or not.
    """
    if not sys.stdin.isatty():
        return console.readline()
    return interactive_readline()


def interactive_readline() -> str:
    """
    Handles interactive line reading with cursor movement, backspace,
    and basic command-line editing capabilities.
    """
    set_cursor(CursorType.THICK)
    default_settings = termios.tcgetattr(0)

    try:
        tty.setraw(0)

        buffer = []
        position = 0

        while True:
            match ch := console.read(1):
                # EOF
                case '':
                    return EOF

                # Enter
                case '\r':
                    buffer.append('\n')
                    console.write('\r\n')
                    return ''.join(buffer)

                # Ctrl-D
                case '\x04':
                    if not buffer:
                        return EOF

                # Ctrl-C
                case '\x03':
                    console.write('\r\n')
                    return '\n'

                # Backspace
                case '\x7f':
                    if position > 0:
                        position -= 1
                        move_cursor(-1)
                        del buffer[position]

                # Escape
                case '\x1b':
                    seq = console.read(2)
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
                    buffer.insert(position, ch)
                    console.write(ch)
                    position += 1

            # Update command line
            redraw_input_line(buffer, position)

    finally:
        termios.tcsetattr(0, termios.TCSADRAIN, default_settings)
        set_cursor(CursorType.DEFAULT)


def redraw_input_line(
        buffer: list[chr],
        cursor_position: int,
) -> None:
    move_cursor(-cursor_position)
    console.write('\x1b[K')
    console.write(''.join(buffer))
    move_cursor(cursor_position - len(buffer))
