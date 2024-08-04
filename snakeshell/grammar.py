GRAMMAR = r"""
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
    | atom '|' !inverted pipeline
    | atom '|' !inverted atom
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
    | redirected
    | inverted
    | subshell
    | command
    ;

redirected
    =
    | redirected redirection
    | command redirection
    ;

redirection
    =
    operator:redirection_start filename:filename
    ;

redirection_start
    =
    | fd:[/[0-9]/] !/\s+/ type:'>>'
    | fd:[/[0-9]/] !/\s+/ type:'<>'
    | fd:[/[0-9]/] !/\s+/ type:'<&'
    | fd:[/[0-9]/] !/\s+/ type:'>&'
    | fd:[/[0-9]/] !/\s+/ type:'>'
    | fd:[/[0-9]/] !/\s+/ type:'<'
    ;

command
    =
    path:filename args:{arg}*
    ;

arg
    =
    | !redirection_start string
    | !redirection_start command_substitution
    ;

command_substitution
    =
    '$(' @:global ')'
    ;

filename
    =
    string
    ;

string
    =
    | "'" ~ @:/[^']*/ "'"
    | '"' ~ @:/[^"]*/ '"'
    | /[^\s'";()<>|&$]+/
    ;
"""
