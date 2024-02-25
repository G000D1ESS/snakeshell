import os


def write(data: str) -> None:
    """
    Writes text to the console without a newline at the end.
    """
    os.write(1, data.encode('utf-8'))


def writeline(data: str) -> None:
    """
    Writes a line of text to the console, followed by an end character.
    """
    write(data+'\n')


def readline() -> str:
    """
    Read a line of text from the console.
    """
    return os.read(0, 1024).decode('utf-8')


def error(msg: str) -> None:
    """
    Writes an error message to the standard error output.
    """
    color_msg = '\033[101m' + msg + '\033[0m\n'
    os.write(2, color_msg.encode('utf-8'))


def prompt_msg() -> str:
    """
    Generate a prompt message indicating the current working directory.
    """
    dirname = os.getcwd()
    homedir = os.path.expanduser('~')
    if dirname.startswith(homedir):
        dirname = '~' + dirname[len(homedir):]
    return f'\033[34;1m{dirname}\033[0m $ '


def prompt_user_to_input() -> str:
    """
    Displays a prompt message to the user and requests
    their input, returning the user's input line.
    """
    write(prompt_msg())
    return readline()
