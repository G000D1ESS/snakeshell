import pytest

from snakeshell.parser import parse
from snakeshell.tree import CommandNode


@pytest.mark.parametrize(
    "command, excpected_path, excpected_args",
    [
        [
            '/bin/echo',
            '/bin/echo', ['/bin/echo'],
        ],
        [
            '/bin/echo foo bar',
            '/bin/echo', ['/bin/echo', 'foo', 'bar'],
        ],
        [
            "/bin/echo 'foo bar'",
            '/bin/echo', ['/bin/echo', 'foo bar'],
        ],
        [
            '/bin/echo "foo bar"',
            '/bin/echo', ['/bin/echo', 'foo bar'],
        ],
        [
            '/bin/echo \'a b\' "c d"',
            '/bin/echo', ['/bin/echo', 'a b', 'c d'],
        ],
    ],
)
def test_command_parsing(
    command,
    excpected_path,
    excpected_args,
):
    result = parse(command)
    assert isinstance(result, CommandNode)
    assert result.arguments == excpected_args
    assert result.execute_path == excpected_path

