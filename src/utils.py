import os
import sys
import signal
from dataclasses import dataclass


class Command:

    def __init__(
        self,
        path: str,
        args: list[str],
    ):
        self.path = path
        self.args = args


    def run(self) -> None:
        """
        Run command.
        """
        os.fsync(0)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        os.execvp(self.path, self.args)


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


def parse(cmd: str) -> Command:
    """
    Parse command line.
    """
    args = cmd.strip().split()
    return Command(
        path=args[0],
        args=args,
    )


def getcmd() -> Command | None:
    """
    Request user to write command, then parse it.
    """
    msg = promt()
    os.write(1, msg.encode())
    cmd = os.read(0, 1024).decode().strip()
    if not cmd:
        return
    return parse(cmd)

