import pytest

from snakeshell.parser import parse
from snakeshell.tree import CommandNode


class TestCommandParse:

    @staticmethod
    def is_command_node(obj):
        return type(obj) == CommandNode

    @staticmethod
    def node_to_dict(obj):
        return {
            'exec': obj.execute_path,
            'args': obj.arguments,
        }

    def test_without_arguments(self):
        command = '/bin/echo'

        node = parse(command)
        node_as_dict = self.node_to_dict(node)

        assert self.is_command_node(node)
        assert node_as_dict == {
            'exec': '/bin/echo',
            'args': ['/bin/echo'],
        }

    def test_with_arguments(self):
        command = '/bin/echo a b c'

        node = parse(command)
        node_as_dict = self.node_to_dict(node)

        assert self.is_command_node(node)
        assert node_as_dict == {
            'exec': '/bin/echo',
            'args': ['/bin/echo', 'a', 'b', 'c'],
        }

    def test_with_single_quoted_argument(self):
        command = "/bin/echo 'a b c'"

        node = parse(command)
        node_as_dict = self.node_to_dict(node)

        assert self.is_command_node(node)
        assert node_as_dict == {
            'exec': '/bin/echo',
            'args': ['/bin/echo', 'a b c'],
        }

    def test_with_double_quoted_argument(self):
        command = '/bin/echo "a b c"'

        node = parse(command)
        node_as_dict = self.node_to_dict(node)

        assert self.is_command_node(node)
        assert node_as_dict == {
            'exec': '/bin/echo',
            'args': ['/bin/echo', 'a b c'],
        }

    def test_with_double_and_single_quoted_arguments(self):
        command = '/bin/echo "first one" \'second one\''

        node = parse(command)
        node_as_dict = self.node_to_dict(node)

        assert self.is_command_node(node)
        assert node_as_dict == {
            'exec': '/bin/echo',
            'args': ['/bin/echo', 'first one', 'second one'],
        }

