from enum import Enum

from .builtin import CommandFactory
from .command import ShellCommand, CommandSequence


class Token(str, Enum):
    STDOUT_TO = '>'
    STDIN_FROM = '<'
    END_OPERATOR = ';'


def parse_command(command_line: str) -> ShellCommand:
    
    input_file = None
    output_file = None

    command_factory = CommandFactory()
    execute_path, *tokens = command_line.split()

    i = 0
    cmd_args = []
    while i < len(tokens):
        token = tokens[i]
        match token:
            case Token.STDOUT_TO:
                i += 1
                output_file = tokens[i]
            case Token.STDIN_FROM:
                i += 1
                input_file = tokens[i]
            case _:
                cmd_args.append(token)
        i += 1

    command = command_factory.get_command(
        path=execute_path,
        args=cmd_args,
    )

    return ShellCommand(
        command=command,
        input_file=input_file,
        output_file=output_file,
    )


def parse_commands(command_line: str) -> CommandSequence:
    commands = CommandSequence()
    for command in command_line.split(Token.END_OPERATOR):
        command = command.strip()
        command = parse_command(command)
        commands.add(command)
    return commands

