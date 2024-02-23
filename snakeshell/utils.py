import os
import sys
import signal
from dataclasses import dataclass

from .cmd import Command


def promt() -> str:
    """
    Generete promt message.
    """
    dirname = os.getcwd()
    homedir = os.path.expanduser('~')
    if dirname.startswith(homedir):
        dirname = '~' + dirname[len(homedir):]
    return f'\033[34;1m{dirname}\033[0m $ '


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
    path, *args = cmd.split()

    if len(args) >= 2 and args[-2] in {'<', '>'}:
        stdout_to = None
        stdin_from = None
        if args[-2] == '>':
            stdout_to = args[-1]
        elif args[-2] == '<':
            stdin_from = args[-1]
        args = args[:-2]
        return RedirectCommand(
            path=path,
            args=args,
            stdin_from=stdin_from,
            stdout_to=stdout_to,
        )

    return Command(
        path=path,
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

