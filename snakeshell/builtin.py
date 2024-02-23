

def change_dir(path: str) -> None:
    """
    Move to directory.
    """
    path = os.path.normpath(path)
    path = os.path.expanduser(path)
    os.chdir(path)
