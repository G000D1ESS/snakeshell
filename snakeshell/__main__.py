import sys
import signal

from .console import error as show_error 
from .console import prompt_user_to_input
from .tree import parse


def setup():
    # Disable the traceback to simplify error messages.
    sys.tracebacklimit = 0

    # Ignore SIGINT (Ctrl+C), preventing the shell from exiting on Ctrl+C.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def loop():
    # Start an infinite loop to continuously accept commands.
    while True:
        line = prompt_user_to_input()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        command = parse(line)
        exit_code = command.execute()
        if exit_code != 0:
            show_error(f'Exit: {exit_code}')


def run_shell():
    setup()
    loop()


if __name__ == '__main__':
    run_shell()

