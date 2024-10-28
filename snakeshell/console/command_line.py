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
    default_settings = termios.tcgetattr(0)

    try:
        tty.setraw(0)
        set_cursor(CursorType.THICK)

        buffer: list[str] = []
        cursor_position: int = 0

        while True:
            input_result, cursor_position = handle_input(buffer, cursor_position)
            if input_result is not None:
                return input_result
            redraw_input_line(buffer, cursor_position)

    finally:
        termios.tcsetattr(0, termios.TCSADRAIN, default_settings)
        set_cursor(CursorType.DEFAULT)


def redraw_input_line(buffer: list[str], cursor_position: int) -> None:
    """
    Clears the current line in the terminal and redraws the buffer contents,
    restores the previous cursor position.
    """
    move_cursor(-cursor_position)
    console.write('\x1b[K')
    console.write(''.join(buffer))
    move_cursor(cursor_position - len(buffer))


def handle_input(
        buffer: list[str],
        cursor_position: int,
) -> tuple[str | None, int]:
    """
    Processes a single character of user input and handles different commands.
    """
    match ch := console.read(1):
        case '\r':
            return handle_enter(buffer), cursor_position
        case '\x03':
            return handle_ctrl_c(), cursor_position
        case '\x04':
            return handle_ctrl_d(buffer), cursor_position
        case '\x7f':
            cursor_position = handle_backspace(buffer, cursor_position)
        case '\x1b':
            cursor_position = handle_escape_sequences(buffer, cursor_position)
        case _:
            cursor_position = handle_character_input(ch, buffer, cursor_position)
    return None, cursor_position


def handle_enter(buffer: list[str]) -> str:
    """
    Handles the Enter key press, finalizing the current input.
    """
    buffer.append('\n')
    console.write('\r\n')
    return ''.join(buffer)


def handle_ctrl_d(buffer: list[str]) -> str | None:
    """
    Handles Ctrl-D (EOF) key press. Returns EOF if buffer is empty, otherwise does nothing.
    """
    if not buffer:
        return EOF


def handle_ctrl_c() -> str:
    """
    Handles Ctrl-C key press, which cancels the current line input.
    """
    console.write('\r\n')
    return '\n'


def handle_backspace(buffer: list[str], cursor_position: int) -> int:
    """
    Handles the backspace key, deleting the character before the cursor.
    """
    if cursor_position > 0:
        cursor_position -= 1
        move_cursor(-1)
        del buffer[cursor_position]
    return cursor_position


def handle_escape_sequences(buffer: list[str], cursor_position: int) -> int:
    """
    Handles escape sequences for arrow keys to move the cursor within the buffer.
    """
    seq = console.read(2)

    # Left arrow
    if seq == r'[D' and cursor_position > 0:
        move_cursor(-1)
        return cursor_position - 1

    # Right arrow
    if seq == r'[C' and cursor_position < len(buffer):
        move_cursor(+1)
        return cursor_position + 1

    return cursor_position


def handle_character_input(ch: str, buffer: list[str], cursor_position: int) -> int:
    """
    Inserts a character into the buffer at the current cursor position.
    """
    buffer.insert(cursor_position, ch)
    console.write(ch)
    return cursor_position + 1
