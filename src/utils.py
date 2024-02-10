import os
import sys


def promt() -> str:
    """
    Generete promt message.
    """
    dirname = os.getcwd()
    homedir = os.path.expanduser('~')
    if dirname.startswith(homedir):
        dirname = '~' + dirname[len(homedir):]
    return f'{dirname} $ '


def change_dir(path: str) -> None:
    """
    Move to directory.
    """
    path = os.path.normpath(path)
    path = os.path.expanduser(path)
    os.chdir(path)


def parse(cmd: str) -> tuple[str, list[str]]:
    """
    Parse command line.
    """
    args = cmd.strip().split(' ')
    return args[0], args


def getcmd() -> tuple[str, list[str]]:
    """
    Request user to write command, then parse it.
    """
    msg = promt()
    os.write(1, msg.encode())
    cmd = os.read(0, 1024).decode()
    if not cmd:
        return '', []
    return parse(cmd)

