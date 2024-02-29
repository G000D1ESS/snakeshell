from enum import Enum

from .tree import (
    ShellNode,
    ListNode,
    OrListNode,
    AndListNode,
    CommandNode,
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


def parse(user_input: str) -> ShellNode:
    root = ListNode()
    for command_block in user_input.split(Operators.LIST):
        command_block = command_block.strip()
        command_block = parse_or_list(command_block)
        root.add(command_block)
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

