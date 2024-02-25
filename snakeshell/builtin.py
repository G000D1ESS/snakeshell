import os
import sys

from .command import Command


class ExitCommand(Command):
    def run(self, *args, **kwargs) -> int:
        sys.exit(0)
        return 0


class ChangeDirCommand(Command):
    def run(self, *args, **kwargs):
        path = self.args[0]
        path = os.path.normpath(path)
        path = os.path.expanduser(path)
        os.chdir(path)
        return 0


BUILTIN_COMMANDS = {
    'exit': ExitCommand,
    'cd': ChangeDirCommand,
}

