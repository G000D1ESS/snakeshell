import os
import sys

from src.utils import getcmd, change_dir


def main():
    sys.tracebacklimit = 0
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
            os.execvp(cmd, args)
        else:
            _, status = os.wait()
            if status != 0:
                os.write(1, b'Exit: %d\n' % status)


if __name__ == '__main__':
    main()

