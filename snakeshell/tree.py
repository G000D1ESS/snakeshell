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


class Node:

    def __init__(
        self,
        left,
        right,
    ):
        self.left: Node | None = left
        self.right: Node | None = right

    def execute(self) -> int:
        raise NotImplementedError


class SubshellNode(Node):

    def execute(self) -> int:
        pid = fork()
        if pid == 0:
            # Child process.
            exit_status = self.left.execute()
            sys.exit(exit_status)

        # Parent process.
        _, wait_status = os.wait()
        exit_code = os.waitstatus_to_exitcode(wait_status)
        return exit_code


class InvertExitCodeNode(Node):

    def execute(self) -> int:
        exit_code = self.left.execute()
        exit_code = int(exit_code == 0)
        return exit_code


class CommandNode(Node):

    def __init__(
        self,
        execute_path: str,
        arguments: list[str],
    ):
        super().__init__(left=None, right=None)
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


class ListNode(Node):

    def execute(self) -> int:
        self.left.execute()
        return self.right.execute()


class OrNode(ListNode):

    def execute(self) -> int:
        exit_code = self.left.execute()
        if exit_code == 0:
            return exit_code
        return self.right.execute()


class AndNode(ListNode):

    def execute(self) -> int:
        exit_code = self.left.execute()
        if exit_code != 0:
            return exit_code
        return self.right.execute()

