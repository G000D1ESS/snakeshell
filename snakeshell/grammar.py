GRAMMAR = r'''
start
    =
    global $
    ;

global
    =
    | @:sequential [';']
    | @:expr [';']
    ;

subshell
    =
    '(' ~ subshell:global ')'
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

pipeline
    =
    | atom '|' pipeline
    | atom '|' atom
    ;

expr
    =
    | and_or
    | pipeline
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
