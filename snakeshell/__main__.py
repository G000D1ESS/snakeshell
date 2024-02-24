import os
import sys
import signal

from .cmd import run_command
from .utils import getcmd, change_dir


def setup():
    # Disable the traceback to simplify error messages.
    sys.tracebacklimit = 0

    # Ignore SIGINT (Ctrl+C), preventing the shell from exiting on Ctrl+C.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def loop():
    # Start an infinite loop to continuously accept commands.
    while True:
        command, write_to, read_from = getcmd()
        if not command:
            continue
        match command.path:
            case 'cd':
                change_dir(command.args[0])
            case 'exit':
                break
            case _:
                pid = os.fork()
                if pid == 0:
                    run_command(
                        cmd=command,
                        write_to=write_to,
                        read_from=read_from,
                    )
                # Wait child process
                _, status = os.wait()
                if status != 0:
                    os.write(2, b'\033[101mExit: %d\033[0m\n' % status)


def run_shell():
    setup()
    loop()


if __name__ == '__main__':
    run_shell()

