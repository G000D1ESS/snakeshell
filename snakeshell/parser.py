import tatsu

from snakeshell.grammar import GRAMMAR
from snakeshell.tree import (
    Node,
    ListNode,
    OrNode,
    AndNode,
    CommandNode,
    RedirectNode,
    PipelineNode,
    SubshellNode,
    InvertExitCodeNode,
    BuiltinCommandNode,
    CommandSubstitutionNode,
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

    def redirected(self, ast):
        node, options = ast
        return RedirectNode(
            executable=node,
            filename=options['filename'],
            fd=options['operator']['fd'],
            operator=options['operator']['type'],
        )

    def command(self, ast):
        path = ast.path
        args = ast.args
        if path in BUILTIN_COMMANDS:
            return BuiltinCommandNode(
                execute_path=path,
                arguments=[path] + args,
            )
        return CommandNode(
            execute_path=path,
            arguments=[path] + args,
        )

    def command_substitution(self, ast):
        return CommandSubstitutionNode(
            executable=ast,
        )

    def string(self, ast):
        return str(ast)


def parse(command: str) -> Node:
    node = _parser.parse(
        command,
        semantics=ShellSemantics(),
    )
    return node
