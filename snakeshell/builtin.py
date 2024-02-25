import os
import sys

from .command import Command


class ExitCommand(Command):
    def execute(self, *args, **kwargs) -> int:
        sys.exit(0)
        return 0


class ChangeDirCommand(Command):
    def execute(self, *args, **kwargs) -> int:
        path = self.args[0]
        path = os.path.normpath(path)
        path = os.path.expanduser(path)
        os.chdir(path)
        return 0


class InvertExitStatusCommand(Command):
    def execute(self, *args, **kwargs) -> int:
        factory = CommandFactory()
        subcommand = factory.get_command(
            path=self.args[0],
            args=self.args[1:],
        )
        exit_status = subcommand.execute(*args, **kwargs)
        return int(exit_status == 0)


class CommandFactory:

    def __init__(self):
        self.builtins = {
            'exit': ExitCommand,
            'cd': ChangeDirCommand,
            '!': InvertExitStatusCommand,
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

