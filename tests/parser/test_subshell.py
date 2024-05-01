from snakeshell.parser import parse
from snakeshell.tree import SubshellNode


def is_subshell(node):
    return type(node) == SubshellNode


def test_single_command():
    command = '(echo a b c)'
    node = parse(command)
    assert is_subshell(node)


def test_command_sequence():
    command = '(echo a; echo b; echo c)'
    node = parse(command)
    assert is_subshell(node)


def test_pipeline():
    command = '(echo a b c | tr a-z A-Z | cat)'
    node = parse(command)
    assert is_subshell(node)


def test_or_list():
    command = '(echo a || echo b || echo c)'
    node = parse(command)
    assert is_subshell(node)


def test_and_list():
    command = '(echo a && echo b && echo c)'
    node = parse(command)
    assert is_subshell(node)


def test_and_or_list():
    command = '(echo a && echo b || echo c)'
    node = parse(command)
    assert is_subshell(node)

