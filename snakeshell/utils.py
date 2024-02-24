import os

from .cmd import ShellCommand
from .parser import parse_command


def promt() -> str:
    """
    Generete promt message.
    """
    dirname = os.getcwd()
    homedir = os.path.expanduser('~')
    if dirname.startswith(homedir):
        dirname = '~' + dirname[len(homedir):]
    return f'\033[34;1m{dirname}\033[0m $ '


def getcmd() -> ShellCommand | None:
    """
    Request user to write command, then parse it.
    """
    msg = promt()
    os.write(1, msg.encode())
    cmd = os.read(0, 1024).decode().strip()
    if not cmd:
        return
    return parse_command(cmd)

