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


def run_command(
    cmd: Command,
    write_to: str | None = None,
    read_from: str | None = None,
) -> None:

    # Redirect standard output if `write_to` is specified.
    if write_to:
        os.close(1)
        os.open(
            mode=0o644,
            path=write_to,
            flags=os.O_WRONLY|os.O_CREAT|os.O_TRUNC,
        )
        os.set_inheritable(1, True)

    # Redirect standard input if `read_from` is specified.
    if read_from:
        os.close(0)
        os.open(
            mode=0o644,
            path=read_from,
            flags=os.O_RDONLY,
        )
        os.set_inheritable(0, True)

    # Execute the command with optional redirections applied.
    cmd.run()

