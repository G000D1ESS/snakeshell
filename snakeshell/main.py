import os
import sys
import signal

from .utils import getcmd, change_dir


def main():

    # Setup 
    sys.tracebacklimit = 0
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Main loop
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
                    os.write(2, b'Exit: %d\n' % status)

