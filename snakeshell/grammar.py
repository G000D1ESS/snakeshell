GRAMMAR = r'''
start
    =
    global $
    ;

global
    =
    | sequential
    | @:expr [';']
    ;

sequential
    =
    | left:expr ';' right:sequential
    | left:expr ';' right:expr
    ;

and_or
    =
    | and_or ('||'|'&&') atom
    | atom ('||'|'&&') atom
    ;

subshell
    =
    '(' ~ subshell:global ')'
    ;

expr
    =
    | and_or
    | atom
    ;

inverted
    =
    '! ' ~ inverted:command
    ;

atom
    =
    | subshell
    | inverted
    | command
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
