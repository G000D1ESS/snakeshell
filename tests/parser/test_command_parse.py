from snakeshell.parser import parse
from snakeshell.tree import CommandNode


def is_command(node):
    return type(node) == CommandNode


def node_to_dict(node):
    return {
        'exec': node.execute_path,
        'args': node.arguments,
    }


def test_without_arguments():
    command = '/bin/echo'

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_command(node)
    assert node_as_dict == {
        'exec': '/bin/echo',
        'args': ['/bin/echo'],
    }


def test_with_arguments():
    command = '/bin/echo a b c'

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_command(node)
    assert node_as_dict == {
        'exec': '/bin/echo',
        'args': ['/bin/echo', 'a', 'b', 'c'],
    }


def test_with_single_quoted_argument():
    command = "/bin/echo 'a b c'"

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_command(node)
    assert node_as_dict == {
        'exec': '/bin/echo',
        'args': ['/bin/echo', 'a b c'],
    }


def test_with_double_quoted_argument():
    command = '/bin/echo "a b c"'

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_command(node)
    assert node_as_dict == {
        'exec': '/bin/echo',
        'args': ['/bin/echo', 'a b c'],
    }


def test_with_double_and_single_quoted_arguments():
    command = '/bin/echo "first one" \'second one\''

    node = parse(command)
    node_as_dict = node_to_dict(node)

    assert is_command(node)
    assert node_as_dict == {
        'exec': '/bin/echo',
        'args': ['/bin/echo', 'first one', 'second one'],
    }

