import os
from enum import Enum


class CursorType(Enum):
    THICK = '\x1b[5 q'
    THIN = '\x1b[3 q'
    DEFAULT = '\x1b[0 q'


def set_cursor(cursor_type: CursorType) -> None:
    """
    Sets the cursor style in the console to the specified type.
    """
    change_cursor_escape_sequence = str(cursor_type.value).encode()
    os.write(1, change_cursor_escape_sequence)


def move_cursor(x: int) -> None:
    """
    TODO: Write.
    """
    if x > 0:
        os.write(1, f'\x1b[{x}C'.encode())
    elif x < 0:
        os.write(1, f'\x1b[{-x}D'.encode())
