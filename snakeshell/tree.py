import os
import sys
import signal


def fork() -> int:
    pid = os.fork()
    if pid == 0:
        # Set the signal handler for SIGINT (Ctrl+C) to the default handling.
        # This ensures that the subprocess will terminate on a SIGINT signal.
        signal.signal(
            signal.SIGINT,
            signal.SIG_DFL,
        )
    return pid


class ShellNode:

    def __init__(self):
        self.children: list[ShellNode] = []

    def add(self, node: 'ShellNode'):
        self.children.append(node)

    def execute(self) -> int:
        exit_code: int = 0
        for child in self.children:
            exit_code = child.execute()
        return exit_code


class SubshellNode(ShellNode):

    def execute(self) -> int:
        pid = fork()
        if pid == 0:
            # Child process.
            exit_status: int = 0
            for child in self.children:
                exit_status = child.execute()
            sys.exit(exit_status)

        # Parent process.
        _, wait_status = os.wait()
        exit_code = os.waitstatus_to_exitcode(wait_status)
        return exit_code


class CommandNode(ShellNode):

    def __init__(
        self,
        execute_path: str,
        arguments: list[str],
    ):
        super().__init__()
        self.execute_path = execute_path
        self.arguments = arguments

    def execute(self) -> int:
        pid = fork()
        if pid == 0:
            # Child process.
            # Replace the current process with a new
            # process running the command.
            os.execvp(
                file=self.execute_path,
                args=self.arguments,
            )

        # Parent process.
        # Wait child process.
        _, wait_status = os.wait()
        exit_code = os.waitstatus_to_exitcode(wait_status)
        return exit_code


class BuiltinCommandNode(CommandNode):

    def execute(self) -> int:
        match self.execute_path:
            case 'cd':
                path = self.arguments[1]
                path = os.path.normpath(path)
                path = os.path.expanduser(path)
                os.chdir(path)
            case 'exec':
                # Set the signal handler for SIGINT (Ctrl+C) to
                # the default handling. This ensures that the process
                # will terminate on a SIGINT signal.
                signal.signal(
                    signal.SIGINT,
                    signal.SIG_DFL,
                )
                # Replace the current process with a new
                # process running the command.
                path, *args = self.arguments[1:]
                os.execvp(
                    file=path,
                    args=[path]+args,
                )
            case 'exit':
                exit_code = 0
                if len(self.arguments) >= 2:
                    exit_code = int(self.arguments[1])
                sys.exit(exit_code)
        return 0


class ListNode(ShellNode):
    pass


class OrListNode(ListNode):

    def execute(self) -> int:
        exit_code: int = 0
        for child in self.children:
            exit_code = child.execute()
            if exit_code == 0:
                return exit_code
        return exit_code


class AndListNode(ListNode):

    def execute(self) -> int:
        exit_code: int = 0
        for child in self.children:
            exit_code = child.execute()
            if exit_code != 0:
                return exit_code
        return exit_code

