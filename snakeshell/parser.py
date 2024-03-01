from enum import Enum

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


def parse(command: str) -> ShellNode:

    root = ListNode()
    command = command.strip()

    i = 0
    unclosed = 0
    subcommand = ''
    is_subshell = False

    while i < len(command):
        if Operators.SUB_START == command[i]:
            unclosed += 1
            is_subshell = True
        elif Operators.SUB_END == command[i]:
            unclosed -= 1
        elif not unclosed and Operators.LIST == command[i]:
            subcommand = subcommand.strip()
            if is_subshell:
                root.add(parse_subshell(subcommand))
            else:
                root.add(parse_or_list(subcommand))
            subcommand = ''
            is_subshell = False
        else:
            subcommand += command[i]
        i += 1

    if subcommand:
        subcommand = subcommand.strip()
        if is_subshell:
            root.add(parse_subshell(subcommand))
        else:
            root.add(parse_or_list(subcommand))
    return root


def parse_subshell(command_line: str) -> ShellNode:
    root = SubshellNode()
    root.add(parse(command_line))
    return root


def parse_or_list(command_block: str) -> ShellNode:
    root = OrListNode()
    for command_block in command_block.split(Operators.OR_LIST):
        command_block = command_block.strip()
        command_block = parse_and_list(command_block)
        root.add(command_block)
    return root


def parse_and_list(command_block: str) -> ShellNode:
    root = AndListNode()
    for command in command_block.split(Operators.AND_LIST):
        command = command.strip()
        command = parse_command(command)
        root.add(command)
    return root


def parse_command(command: str) -> ShellNode:
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

