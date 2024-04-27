from snakeshell.parser import parse
from snakeshell.tree import CommandNode


class TestCommandParsing:

    def test_without_args(self):
        result = parse(command='/bin/cat')
        assert isinstance(result, CommandNode)
        assert result.execute_path == '/bin/cat'
        assert result.arguments == ['/bin/cat']

    def test_with_args(self):
        result = parse(command='/bin/echo foo bar')
        assert isinstance(result, CommandNode)
        assert result.execute_path == '/bin/echo'
        assert result.arguments == ['/bin/echo', 'foo', 'bar']

    def test_with_single_quoted_args(self):
        result = parse(command='/bin/echo \'foo bar\'')
        assert isinstance(result, CommandNode)
        assert result.execute_path == '/bin/echo'
        assert result.arguments == ['/bin/echo', 'foo bar']

    def test_with_double_quoted_args(self):
        result = parse(command='/bin/echo "foo bar"')
        assert isinstance(result, CommandNode)
        assert result.execute_path == '/bin/echo'
        assert result.arguments == ['/bin/echo', 'foo bar']

    def test_with_mixed_quoted_args(self):
        result = parse(command='/bin/echo \'first one\' "second one"')
        assert isinstance(result, CommandNode)
        assert result.execute_path == '/bin/echo'
        assert result.arguments == ['/bin/echo', 'first one', 'second one']

