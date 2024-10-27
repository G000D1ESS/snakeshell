
import termios
import tty

from snakeshell import console
from snakeshell.console.cursor import move_cursor


EOF = ''


def interactive_readline() -> str:
    """
    TODO: Write.
    """
    default_settings = termios.tcgetattr(0)

    try:
        tty.setraw(0)

        position = 0
        buffer = bytearray()

        while True:
            match ch := console.read(1).encode('utf-8'):
                # EOF
                case b'':
                    return EOF

                # Enter
                case b'\r':
                    console.write('\r\n')
                    buffer.append(ord(b'\n'))
                    return buffer.decode('utf-8')

                # Ctrl-D
                case b'\x04':
                    if not buffer:
                        return EOF

                # Ctrl-C
                case b'\x03':
                    console.write('\r\n')
                    return '\n'

                # Backspace
                case b'\x7f':
                    if position > 0:
                        position -= 1
                        move_cursor(-1)
                        del buffer[position]

                # Escape
                case b'\x1b':
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
                    buffer.insert(position, ord(ch))
                    console.write(ch.decode('utf-8'))
                    position += 1

            # Update command line
            move_cursor(-position)
            console.write('\x1b[K')
            console.write(buffer.decode('utf-8'))
            move_cursor(position-len(buffer))
    finally:
        termios.tcsetattr(0, termios.TCSADRAIN, default_settings)
