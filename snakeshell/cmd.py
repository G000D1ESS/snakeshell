import os
import signal

from dataclasses import dataclass


@dataclass
class Command:
    path: str
    args: list[str]

    def run(self):
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


@dataclass
class ShellCommand:
    command: Command
    input_file: str | None = None
    output_file: str | None = None

    def run(self):

        # Redirect standard input if `self.input_file` is specified.
        if self.input_file is not None:
            os.close(0)
            os.open(
                mode=0o644,
                path=self.input_file,
                flags=os.O_RDONLY,
            )
            os.set_inheritable(0, True)

        # Redirect standard output if `self.output_file` is specified.
        if self.output_file is not None:
            os.close(1)
            os.open(
                mode=0o644,
                path=self.output_file,
                flags=os.O_WRONLY|os.O_CREAT|os.O_TRUNC,
            )
            os.set_inheritable(1, True)

        # Execute the command with optional redirections applied.
        self.command.run()

