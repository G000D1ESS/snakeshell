import os
import sys

from .utils import getcmd, change_dir


def main():
    sys.tracebacklimit = 0
    while True:
        cmd, args = getcmd() 
        if cmd == 'cd':
            change_dir(args[1])
            continue
        pid = os.fork()
        if pid == 0:
            os.fsync(0)
            os.execv(f'/bin/{args[0]}', args)
        else:
            _, status = os.waitpid(pid, os.P_WAIT)
            if status != 0:
                os.write(1, b'Exit: %d\n' % status)


if __name__ == '__main__':
    main()

