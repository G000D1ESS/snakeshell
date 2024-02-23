from enum import Enum
from typing import NamedTuple

from .cmd import Command


class Token(str, Enum):
    STDOUT_TO = '>'
    STDIN_FROM = '<'


class ParsedCommand(NamedTuple):
    command: Command
    write_to: str | None = None
    read_from: str | None = None


def parse_command(command_line: str) -> ParsedCommand:
    
    write_to = None
    read_from = None
    execute_path, *tokens = command_line.split()

    i = 0
    cmd_args = []
    while i < len(tokens):
        token = tokens[i]
        match token:
            case Token.STDOUT_TO:
                i += 1
                write_to = tokens[i]
            case Token.STDIN_FROM:
                i += 1
                read_from = tokens[i]
            case _:
                cmd_args.append(token)
        i += 1

    command = Command(
        path=execute_path,
        args=cmd_args,
    )

    return ParsedCommand(
        command=command,
        write_to=write_to,
        read_from=read_from,
    )

