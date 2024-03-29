import tatsu

from snakeshell.grammar import GRAMMAR
from snakeshell.tree import (
    Node,
    ListNode,
    OrNode,
    AndNode,
    CommandNode,
    PipelineNode,
    SubshellNode,
    InvertExitCodeNode,
    BuiltinCommandNode,
)


BUILTIN_COMMANDS = {
    'cd',
    'exec',
    'exit',
}


# Setup PEG parser
_parser = tatsu.compile(GRAMMAR)


class ShellSemantics:

    def sequential(self, ast):
        left, _, right = ast
        return ListNode(
            left=left,
            right=right,
        )

    def pipeline(self, ast):
        left, _, right = ast
        return PipelineNode(
            left=left,
            right=right,
        )

    def and_or(self, ast):
        left, op, right = ast
        if op == '&&':
            return AndNode(
                left=left,
                right=right,
            )
        if op == '||':
            return OrNode(
                left=left,
                right=right,
            )

    def subshell(self, ast):
        return SubshellNode(
            left=ast,
            right=None,
        )

    def inverted(self, ast):
        return InvertExitCodeNode(
            left=ast,
            right=None,
        )

    def command(self, ast):
        path = ast.path
        args = ast.args
        if path in BUILTIN_COMMANDS:
            return BuiltinCommandNode(
                execute_path=path,
                arguments=[path]+args,
            )
        return CommandNode(
            execute_path=path,
            arguments=[path]+args,
        )

    def string(self, ast):
        return str(ast)


def parse(command: str) -> Node:
    node = _parser.parse(
        command,
        semantics=ShellSemantics(),
    )
    return node

