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

