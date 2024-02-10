import os
import sys
import signal

from src.utils import getcmd, change_dir


def main():

    # Setup 
    sys.tracebacklimit = 0
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Main loop
    while True:
        cmd, args = getcmd()
        if not cmd:
            continue
        if cmd == 'cd':
            change_dir(args[1])
            continue
        if cmd == 'exit':
            break
        pid = os.fork()
        if pid == 0:
            os.fsync(0)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            os.execvp(cmd, args)
        else:
            _, status = os.wait()
            if status != 0:
                os.write(1, b'Exit: %d\n' % status)


if __name__ == '__main__':
    main()

