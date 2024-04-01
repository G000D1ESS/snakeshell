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


class PipelineNode(Node):

    def execute(self) -> int:

        # Open pipe
        r, w = os.pipe()
        os.set_inheritable(r, True)
        os.set_inheritable(w, True)

        if fork() == 0:
            # Child process.
            # Write stdout into pipe.
            os.close(r)
            os.dup2(w, 1)
            code = self.left.execute()
            sys.exit(code)

        if fork() == 0:
            # Child process.
            # Read stdin from pipe.
            os.close(w)
            os.dup2(r, 0)
            code = self.right.execute()
            sys.exit(code)

        # Parent process.

        # Close pipe.
        os.close(r)
        os.close(w)

        # Wait children.
        statuses = [
            os.wait(),
            os.wait(),
        ]

        # Check process exit codes
        for _, status in statuses:
            exit_code = os.waitstatus_to_exitcode(status)
            if exit_code != 0:
                return exit_code
        return 0


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


class RedirectNode(Node):

    MODES = {
        '<': {'fd': 0, 'mode': os.O_RDONLY},
        '>': {'fd': 1, 'mode': os.O_CREAT | os.O_TRUNC | os.O_WRONLY},
        '>>': {'fd': 1, 'mode': os.O_CREAT | os.O_APPEND | os.O_WRONLY},
        '<>': {'fd': 0, 'mode': os.O_CREAT | os.O_RDWR},
        '<&': {'fd': 0, 'mode': None},
        '>&': {'fd': 1, 'mode': None},
    }

    def __init__(
        self,
        fd: str | None,
        filename: str,
        operator: str,
        executable: Node,
    ):
        super().__init__(
            left=executable,
            right=None,
        )
        self.fd = fd
        if fd is None:
            self.fd = self.MODES[operator]['fd']
        self.fd = int(self.fd)
        self.mode = self.MODES[operator]['mode']
        self.filename = filename

    def execute(self) -> int:

        if fork() == 0:
            # Child process.
                if self.mode is None:
                    if self.filename == '-':
                        os.close(self.fd)
                    else:
                        new = os.dup(int(self.filename))
                        os.dup2(new, self.fd)
                else:
                    try:
                        new = os.open(
                            path=self.filename,
                            flags=self.mode,
                            mode=0o644,
                        )
                        os.dup2(new, self.fd)
                    except FileNotFoundError:
                        sys.exit(1)
                exit_code = self.left.execute()
                sys.exit(exit_code)

        # Parent process.
        _, wait_status = os.wait()
        exit_code = os.waitstatus_to_exitcode(wait_status)
        return exit_code


class ListNode(Node):

    def execute(self) -> int:
        self.left.execute()
        return self.right.execute()


class OrNode(Node):

    def execute(self) -> int:
        exit_code = self.left.execute()
        if exit_code == 0:
            return exit_code
        return self.right.execute()


class AndNode(Node):

    def execute(self) -> int:
        exit_code = self.left.execute()
        if exit_code != 0:
            return exit_code
        return self.right.execute()

