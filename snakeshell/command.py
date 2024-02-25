import os
import signal

from dataclasses import dataclass


@dataclass
class Command:
    path: str
    args: list[str]

    def execute(
        self,
        stdin_fd: int | None = None,
        stdout_fd: int | None = None,
    ) -> int:

        pid = os.fork()
        if pid == 0:
            # Child process

            # Redirect standard input if `stdin` is specified.
            if stdin_fd is not None:
                os.dup2(stdin_fd, 0)

            # Redirect standard output if `stdout` is specified.
            if stdout_fd is not None:
                os.dup2(stdout_fd, 1)

            # Set the signal handler for SIGINT (Ctrl+C) to the default handling.
            # This ensures that the subprocess will terminate on a SIGINT signal.
            signal.signal(
                signal.SIGINT,
                signal.SIG_DFL,
            )

            # Replace the current process with a new process running the command.
            os.execvp(
                file=self.path,
                args=[self.path] + self.args,
            )

        # Parent process

        # Close file descriptors
        if stdin_fd is not None:
            os.close(stdin_fd)
        if stdout_fd is not None:
            os.close(stdout_fd)

        # Wait child process
        _, wait_status = os.wait()
        exit_code = os.waitstatus_to_exitcode(wait_status)
        return exit_code


@dataclass
class ShellCommand:
    command: Command
    input_file: str | None = None
    output_file: str | None = None

    def execute(self) -> int:

        stdin_fd: int | None = None
        stdout_fd: int | None = None

        # If an input file is specified, open it as read-only
        if self.input_file is not None:
            stdin_fd = os.open(
                mode=0o644,
                path=self.input_file,
                flags=os.O_RDONLY,
            )

        # If an output file is specified, open/create
        # it for writing, truncating it first
        if self.output_file is not None:
            stdout_fd = os.open(
                mode=0o644,
                path=self.output_file,
                flags=os.O_WRONLY|os.O_CREAT|os.O_TRUNC,
            )

        # Execute the command with the provided file descriptors
        # for stdin and stdout
        return self.command.execute(
            stdin_fd=stdin_fd,
            stdout_fd=stdout_fd,
        )

