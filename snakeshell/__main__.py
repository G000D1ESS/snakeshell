import os
import sys
import signal

from .utils import getcmd, change_dir


def setup():
    sys.tracebacklimit = 0
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def loop():
    while True:
        command = getcmd()
        if not command:
            continue
        match command.path:
            case 'cd':
                change_dir(command.args[1])
            case 'exit':
                break
            case _:
                pid = os.fork()
                if pid == 0:
                    command.run()
                # Wait child process
                _, status = os.wait()
                if status != 0:
                    os.write(2, b'\033[101mExit: %d\033[0m\n' % status)


def run_shell():
    setup()
    loop()


if __name__ == '__main__':
    run_shell()

