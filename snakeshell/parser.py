import tatsu

from .tree import (
    ShellNode,
    ListNode,
    OrListNode,
    AndListNode,
    CommandNode,
    SubshellNode,
    InvertExitCodeNode,
    BuiltinCommandNode,
)


BUILTIN_COMMANDS = {
    'cd',
    'exec',
    'exit',
}


GRAMMAR = r'''
start
    =
    sequential_list
    ;


sequential_list
    =
    sequence:or_list {';' sequence+:or_list}* [';']
    ;


or_list
    =
    sequence:and_list {'||' sequence+:and_list}*
    ;


and_list
    =
    sequence:expression {'&&' sequence+:expression}*
    ;


subshell
    =
    '(' subshell:start ')'
    ;


expression
    =
    | subshell
    | inverted
    | command
    ; 


inverted
    =
    '! ' ~ inverted:command
    ;


command
    =
    path:string args:{ string }*
    ;


string
    =
    | "'" @:/[^']*/ "'"
    | /[^\s'";()|&]+/
    ;
'''


# Setup PEG parser
parser = tatsu.compile(GRAMMAR)


class ShellSemantics:

    def sequential_list(self, ast):
        if isinstance(ast.sequence, list):
            lst = ListNode()
            for child in ast.sequence:
                lst.add(child)
            return lst
        return ast.sequence

    def and_list(self, ast):
        if isinstance(ast.sequence, list):
            lst = AndListNode()
            for child in ast.sequence:
                lst.add(child)
            return lst
        return ast.sequence

    def or_list(self, ast):
        if isinstance(ast.sequence, list):
            lst = OrListNode()
            for child in ast.sequence:
                lst.add(child)
            return lst
        return ast.sequence

    def subshell(self, ast):
        root = SubshellNode()
        root.add(ast.subshell)
        return root

    def inverted(self, ast):
        root = InvertExitCodeNode()
        root.add(ast.inverted)
        return root

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


def parse(command: str) -> ShellNode:
    node = parser.parse(
        command,
        semantics=ShellSemantics(),
    )
    return node

