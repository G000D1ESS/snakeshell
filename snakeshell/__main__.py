import os
import sys
import signal

from .utils import getcmd


def setup():
    # Disable the traceback to simplify error messages.
    sys.tracebacklimit = 0

    # Ignore SIGINT (Ctrl+C), preventing the shell from exiting on Ctrl+C.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def loop():
    # Start an infinite loop to continuously accept commands.
    while True:
        command = getcmd()
        if not command:
            continue
        exit_code = command.run()
        if exit_code != 0:
            os.write(2, b'\033[101mExit: %d\033[0m\n' % exit_code)


def run_shell():
    setup()
    loop()


if __name__ == '__main__':
    run_shell()

