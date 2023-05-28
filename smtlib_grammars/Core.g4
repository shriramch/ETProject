grammar Core;

ParOpen
    : '('
    ;

ParClose
    : ')'
    ;

var_name
    : 'a'
    | 'b'
    ;

var_type
    : 'Bool'
    ;

declareConsta
    : ParOpen 'declare-const' 'a' var_type ParClose
    ;

declareConstb
    : ParOpen 'declare-const' 'b' var_type ParClose
    ;

boolean 
    : 'true'
    | 'false'
    ;

bool_term
    : boolean
    | var_name
    | ParOpen 'not' bool_term ParClose
    | ParOpen 'and' bool_term bool_term ParClose
    | ParOpen 'or' bool_term bool_term ParClose
    | ParOpen 'xor' bool_term bool_term ParClose
    | ParOpen '=' bool_term bool_term ParClose
    | ParOpen 'distinct' bool_term bool_term ParClose
    | ParOpen 'ite' bool_term bool_term bool_term ParClose
    ;

checkSat
    : ParOpen 'check-sat' ParClose
    ;

assertStatement
    : ParOpen 'assert' bool_term ParClose
    ;

start
    : declareConsta declareConstb assertStatement checkSat EOF
    ;
