from enum import Enum

from snakeshell import console


class CursorType(Enum):
    THICK = '\x1b[5 q'
    THIN = '\x1b[3 q'
    DEFAULT = '\x1b[0 q'


def set_cursor(cursor_type: CursorType) -> None:
    """
    Sets the cursor style in the console to the specified type.
    """
    change_cursor_escape_sequence = str(cursor_type.value)
    console.write(change_cursor_escape_sequence)


def move_cursor(x: int) -> None:
    """
    Moves the cursor left or right in the console
    by a specified number of positions.
    """
    if x > 0:
        console.write(f'\x1b[{x}C')
    elif x < 0:
        console.write(f'\x1b[{-x}D')
