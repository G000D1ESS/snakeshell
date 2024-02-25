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


class CommandFactory:

    def __init__(self):
        self.builtins = {
            'exit': ExitCommand,
            'cd': ChangeDirCommand,
        }

    def get_command(
        self,
        path: str,
        args: list[str],
    ):
        if builtin_cls := self.builtins.get(path):
            return builtin_cls(
                path=path,
                args=args,
            )
        return Command(
            path=path,
            args=args,
        )


command_factory = CommandFactory()

