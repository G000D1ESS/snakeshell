import pytest

from snakeshell.parser import parse
from snakeshell.tree import CommandNode, ListNode


def is_command(node):
    return isinstance(node, CommandNode)


def is_sequence(node):
    return isinstance(node, ListNode)


def serialize(node):
    if is_sequence(node):
        left = serialize(node.left)
        right = serialize(node.right)
        if isinstance(right, list):
            return [left, *right]
        return [left, right]
    if is_command(node):
        return {
            'exec': node.execute_path,
            'args': node.arguments,
        }
    raise ValueError(f'Unknown node type: {type(node)}')


def test_sequence_with_spaces():
    command = 'a; b; c'

    node = parse(command)
    node_as_list = serialize(node)

    assert is_sequence(node)
    assert node_as_list == [
        {'exec': 'a', 'args': ['a']},
        {'exec': 'b', 'args': ['b']},
        {'exec': 'c', 'args': ['c']},
    ]


def test_sequence_without_spaces():
    command = 'a;b;c'

    node = parse(command)
    node_as_list = serialize(node)

    assert is_sequence(node)
    assert node_as_list == [
        {'exec': 'a', 'args': ['a']},
        {'exec': 'b', 'args': ['b']},
        {'exec': 'c', 'args': ['c']},
    ]


def test_sequence_with_trailing_semicolon():
    command = 'a; b; c;'

    node = parse(command)
    node_as_list = serialize(node)

    assert is_sequence(node)
    assert node_as_list == [
        {'exec': 'a', 'args': ['a']},
        {'exec': 'b', 'args': ['b']},
        {'exec': 'c', 'args': ['c']},
    ]


@pytest.mark.xfail
def test_sequence_multiple_trailing_semicolons():
    command = 'a; b; c;;;'
    parse(command)
