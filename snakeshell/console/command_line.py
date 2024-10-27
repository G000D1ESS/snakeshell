import os
import termios
import tty

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
