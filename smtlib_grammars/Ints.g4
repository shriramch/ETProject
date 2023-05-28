grammar Ints;

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
    : 'Int'
    ;

integer
    : '0'
    | '1'
    ;

int_term
    : integer
    | var_name
    | ParOpen '-' int_term ParClose
    | ParOpen '-' int_term int_term ParClose
    | ParOpen '+' int_term int_term ParClose
    | ParOpen '*' int_term int_term ParClose
    | ParOpen 'div' int_term int_term ParClose
    | ParOpen 'mod' int_term int_term ParClose
    | ParOpen 'abs' int_term ParClose
    ; 

bool_term
    : ParOpen 'not' bool_term ParClose
    | ParOpen 'and' bool_term bool_term ParClose
    | ParOpen 'or' bool_term bool_term ParClose
    | ParOpen 'xor' bool_term bool_term ParClose
    | ParOpen '=' bool_term bool_term ParClose
    | ParOpen 'distinct' bool_term bool_term ParClose
    | ParOpen 'ite' bool_term bool_term bool_term ParClose
    | ParOpen '=' int_term int_term ParClose
    | ParOpen '<=' int_term int_term ParClose
    | ParOpen '<' int_term int_term ParClose
    | ParOpen '>=' int_term int_term ParClose
    | ParOpen '>' int_term int_term ParClose
    ;

checkSat
    : ParOpen 'check-sat' ParClose
    ;

assertStatement
    : ParOpen 'assert' bool_term ParClose
    ;

declareConsta
    : ParOpen 'declare-const' 'a' var_type ParClose
    ;

declareConstb
    : ParOpen 'declare-const' 'b' var_type ParClose
    ;

start
    : declareConsta declareConstb assertStatement checkSat EOF
    ;
