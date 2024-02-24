from enum import Enum
from typing import NamedTuple

from .cmd import Command, ShellCommand


class Token(str, Enum):
    STDOUT_TO = '>'
    STDIN_FROM = '<'


def parse_command(command_line: str) -> ShellCommand:
    
    input_file = None
    output_file = None

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

    command = Command(
        path=execute_path,
        args=cmd_args,
    )

    return ShellCommand(
        command=command,
        input_file=input_file,
        output_file=output_file,
    )

