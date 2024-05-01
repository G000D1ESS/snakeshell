from snakeshell.parser import parse
from snakeshell.tree import BuiltinCommandNode


def is_builtin(node):
    return type(node) == BuiltinCommandNode


def node_to_dict(node):
    return {
        'exec': node.execute_path,
        'args': node.arguments,
    }


def test_change_directory_builtin():
    command = 'cd ./some/path'

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_builtin(node)
    assert node_as_dict == {
        'exec': 'cd',
        'args': ['cd', './some/path'],
    }


def test_exec_builtin():
    command = 'exec echo a b c'

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_builtin(node)
    assert node_as_dict == {
        'exec': 'exec',
        'args': ['exec', 'echo', 'a', 'b', 'c'],
    }


def test_exit_builtin():
    command = 'exit 1'

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_builtin(node)
    assert node_as_dict == {
        'exec': 'exit',
        'args': ['exit', '1'],
    }
