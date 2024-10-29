import sys
import signal
import os

from tatsu.exceptions import FailedParse

from snakeshell import console
from snakeshell.parser import parse


def setup():
    # Disable the traceback to simplify error messages.
    sys.tracebacklimit = 0

    # Ignore SIGINT (Ctrl+C), preventing the shell from exiting on Ctrl+C.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Set the 'CLICOLOR' environment variable to '1' to enable
    # colored output for commands like 'ls'.
    os.environ['CLICOLOR'] = '1'


def loop():
    # Start an infinite loop to continuously accept commands.
    while True:
        try:
            line = console.prompt()
        except EOFError:
            break

        line = line.strip()
        if not line:
            continue

        try:
            command = parse(line)
        except FailedParse as error:
            error_msg = 'parse error\n'
            error_msg += f'{line}\n'
            error_msg += '^'.rjust(error.pos+1)
            console.error(error_msg)
            continue

        try:
            exit_code = command.execute()
            if exit_code != 0:
                console.error(f'process failed (exit code: {exit_code})')
        except Exception as error:  # noqa
            console.error(f'execution error: {error}')


def run_shell():
    setup()
    loop()
