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
        os.fsync(0)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        os.execvp(self.path, self.args)


class RedirectCommand(Command):

    def __init__(
        self,
        path: str,
        args: list[str],
        stdout_to: str | None = None,
        stdin_from: str | None = None,
    ):
        self.path = path
        self.args = args
        self.stdout_to = stdout_to
        self.stdin_from = stdin_from

    def run(self) -> None:
        if self.stdin_from:
            os.close(0)
            fd = os.open(
                path=self.stdin_from,
                flags=os.O_RDONLY,
                mode=0o644,
            )
            os.set_inheritable(fd, True)
        if self.stdout_to:
            os.close(1)
            fd = os.open(
                path=self.stdout_to,
                flags=os.O_WRONLY|os.O_CREAT|os.O_TRUNC,
                mode=0o644,
            )
            os.set_inheritable(fd, True)
        super().run()


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
    args = cmd.split()

    if len(args) >= 2 and args[-2] in {'<', '>'}:
        stdout_to = None
        stdin_from = None
        if args[-2] == '>':
            stdout_to = args[-1]
        elif args[-2] == '<':
            stdin_from = args[-1]
        args = args[:-2]
        return RedirectCommand(
            path=args[0],
            args=args,
            stdin_from=stdin_from,
            stdout_to=stdout_to,
        )

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

