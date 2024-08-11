import sys
import signal

from tatsu.exceptions import FailedParse

from snakeshell import console
from snakeshell.parser import parse


def setup():
    # Disable the traceback to simplify error messages.
    sys.tracebacklimit = 0

    # Ignore SIGINT (Ctrl+C), preventing the shell from exiting on Ctrl+C.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def loop():
    # Start an infinite loop to continuously accept commands.
    while True:
        line = console.prompt()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            command = parse(line)
        except FailedParse:
            console.error('parse error')
            continue
        exit_code = command.execute()
        if exit_code != 0:
            console.error(f'process failed (exit code: {exit_code})')


def run_shell():
    setup()
    loop()
