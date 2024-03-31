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
    '(' @:global ')'
    ;

sequential
    =
    | expr ';' sequential
    | expr ';' expr
    ;

and_or
    =
    | and_or ('||'|'&&') (pipeline|atom)
    | (pipeline|atom) ('||'|'&&') (pipeline|atom)
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
    '! ' ~ @:command
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
