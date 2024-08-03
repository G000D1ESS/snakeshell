from snakeshell.tree import CommandNode


def test_execution_without_stdout():
    command = CommandNode(
        execute_path='echo',
        arguments=['echo'],
    )
    exit_code = command.execute()
    assert exit_code == 0


def test_execution_with_showing_message_in_stdout(capfd):
    command = CommandNode(
        execute_path='echo',
        arguments=['echo', 'test', 'message'],
    )

    exit_code = command.execute()
    captured = capfd.readouterr()

    assert exit_code == 0
    assert captured.out == 'test message\n'


def test_execution_with_absolute_path_supported(capfd):
    command = CommandNode(
        execute_path='/bin/echo',
        arguments=['/bin/echo', 'absolute', 'path'],
    )

    exit_code = command.execute()
    captured = capfd.readouterr()

    assert exit_code == 0
    assert captured.out == 'absolute path\n'


def test_execution_unknown_command_should_return_non_zero_exit_code():
    command = CommandNode(
        execute_path='UnkN0wNC0mm4Nd',
        arguments=['UnkN0wNC0mm4Nd'],
    )
    exit_code = command.execute()
    assert exit_code != 0

