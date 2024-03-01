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
    GROUP_START = '('
    GROUP_END = ')'


def parse(command_line: str) -> ShellNode:

    root = ListNode()

    command_block = ''
    unclosed_groups = 0
    parser = parse_or_list

    for ch in command_line:
        match ch:
            case Operators.GROUP_START:
                unclosed_groups += 1
                parser = parse_subshell
            case Operators.GROUP_END:
                unclosed_groups -= 1
            case Operators.LIST:
                if unclosed_groups:
                    command_block += ch
                if not unclosed_groups:
                    command_block = command_block.strip()
                    command_block = parser(command_block)
                    root.add(command_block)
                    parser = parse_or_list
                    command_block = ''
            case _:
                command_block += ch

    if command_block:
        command_block = command_block.strip()
        command_block = parser(command_block)
        root.add(command_block)
    return root


def parse_subshell(command_block):
    root = SubshellNode()
    root.add(parse(command_block))
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

