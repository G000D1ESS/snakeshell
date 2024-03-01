from enum import Enum
from typing import Callable
from functools import wraps

from .tree import (
    ShellNode,
    ListNode,
    OrListNode,
    AndListNode,
    CommandNode,
    SubshellNode,
    BuiltinCommandNode,
)


BUILTIN_COMMANDS = {
    'cd',
    'exec',
    'exit',
}


class Operators(str, Enum):
    LIST = ';'
    OR_LIST = '||'
    AND_LIST = '&&'
    SUB_START = '('
    SUB_END = ')'


def handle_subshell(func):
    @wraps(func)
    def wrapped(command: str) -> ShellNode:
        command = command.strip()
        is_subshell = command.startswith(Operators.SUB_START)
        is_subshell &= command.endswith(Operators.SUB_END)
        if is_subshell:
            command = command[1:-1]
            command = command.strip()
            root = SubshellNode()
            root.add(parse(command))
            return root
        return func(command)
    return wrapped


@handle_subshell
def parse(command: str) -> ShellNode:

    root = ListNode()
    command = command.strip()

    i = 0
    unclosed = 0
    subcommand = ''

    while i < len(command):

        subcommand += command[i]

        if Operators.SUB_START == command[i]:
            unclosed += 1
        elif Operators.SUB_END == command[i]:
            unclosed -= 1

        if unclosed:
            i += 1
            continue

        if Operators.LIST == command[i]:
            subcommand = subcommand[:-1]
            root.add(parse_or_list(subcommand))
            subcommand = ''
        i += 1

    if subcommand.strip():
        root.add(parse_or_list(subcommand))
    return root


@handle_subshell
def parse_or_list(command: str) -> ShellNode:

    root = OrListNode()
    command = command.strip()

    i = 0
    unclosed = 0
    subcommand = ''

    while i < len(command):

        subcommand += command[i]

        if Operators.SUB_START == command[i]:
            unclosed += 1
        elif Operators.SUB_END == command[i]:
            unclosed -= 1

        if unclosed:
            i += 1
            continue

        if i > 0 and Operators.OR_LIST == command[i-1]+command[i]:
            subcommand = subcommand[:-2]
            root.add(parse_and_list(subcommand))
            subcommand = ''
        i += 1

    if subcommand.strip():
        root.add(parse_and_list(subcommand))
    return root


@handle_subshell
def parse_and_list(command: str) -> ShellNode:

    root = AndListNode()
    command = command.strip()

    i = 0
    unclosed = 0
    subcommand = ''

    while i < len(command):

        subcommand += command[i]

        if Operators.SUB_START == command[i]:
            unclosed += 1
        elif Operators.SUB_END == command[i]:
            unclosed -= 1

        if unclosed:
            i += 1
            continue

        if i > 0 and Operators.AND_LIST == command[i-1]+command[i]:
            subcommand = subcommand[:-2]
            root.add(parse_command(subcommand))
            subcommand = ''
        i += 1

    if subcommand.strip():
        root.add(parse_command(subcommand))
    return root


@handle_subshell
def parse_command(command: str) -> ShellNode:
    command = command.strip()
    path, *args = command.split()
    if path in BUILTIN_COMMANDS:
        return BuiltinCommandNode(
            execute_path=path,
            arguments=[path]+args,
        )
    return CommandNode(
        execute_path=path,
        arguments=[path]+args,
    )

