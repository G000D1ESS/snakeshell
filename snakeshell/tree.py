import os
import signal

from enum import Enum


class Operators(str, Enum):
    LIST = ';'
    OR_LIST = '||'
    AND_LIST = '&&'


class ShellNode:

    def __init__(self):
        self.children: list[ShellNode] = []

    def add(self, node: 'ShellNode'):
        self.children.append(node)

    def execute(self) -> int:
        exit_code: int = 0
        for child in self.children:
            exit_code = child.execute()
        return exit_code


class ListNode(ShellNode):
    pass


class OrListNode(ShellNode):

    def execute(self) -> int:
        exit_code: int = 0
        for child in self.children:
            exit_code = child.execute()
            if exit_code == 0:
                return exit_code
        return exit_code


class AndListNode(ShellNode):

    def execute(self) -> int:
        exit_code: int = 0
        for child in self.children:
            exit_code = child.execute()
            if exit_code != 0:
                return exit_code
        return exit_code


class ExecNode(ShellNode):

    def __init__(
        self,
        execute_path: str,
        arguments: list[str],
    ):
        super().__init__()
        self.execute_path = execute_path
        self.arguments = arguments

    def execute(self):
        pid = os.fork()
        if pid == 0:
            # Child process.
            # Set the signal handler for SIGINT (Ctrl+C) to the default handling.
            # This ensures that the subprocess will terminate on a SIGINT signal.
            signal.signal(
                signal.SIGINT,
                signal.SIG_DFL,
            )

            # Replace the current process with a new process running the command.
            os.execvp(
                file=self.execute_path,
                args=self.arguments,
            )

        # Parent process.
        # Wait child process.
        _, wait_status = os.wait()
        exit_code = os.waitstatus_to_exitcode(wait_status)
        return exit_code


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
    return ExecNode(
        execute_path=path,
        arguments=[path]+args,
    )


