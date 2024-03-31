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
    | redirected
    | command
    ;

redirected
    =
    command:command redirection:{redirection}+
    ;

redirection
    =
    operation:redirection_start filename:filename
    ;

redirection_start
    =
    | fd:[/[0-9]/] type:'>>'
    | fd:[/[0-9]/] type:'<>'
    | fd:[/[0-9]/] type:'<&'
    | fd:[/[0-9]/] type:'&>'
    | fd:[/[0-9]/] type:'>'
    | fd:[/[0-9]/] type:'<'
    ;

command
    =
    path:filename args:{arg}*
    ;

arg
    =
    !redirection_start string
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
'''
