grammar Reals;

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
    : 'Real'
    ;

real
    : '0.0' 
    | '1.0'
    ;

real_term
    : real
    | var_name
    | ParOpen '-' real_term ParClose
    | ParOpen '-' real_term real_term ParClose
    | ParOpen '+' real_term real_term ParClose
    | ParOpen '*' real_term real_term ParClose
    | ParOpen '/' real_term real_term ParClose
    | ParOpen 'sin' real_term ParClose
    | ParOpen 'cos' real_term ParClose
    | ParOpen 'tan' real_term ParClose
    ; 

bool_term
    : ParOpen 'not' bool_term ParClose
    | ParOpen 'and' bool_term bool_term ParClose
    | ParOpen 'or' bool_term bool_term ParClose
    | ParOpen 'xor' bool_term bool_term ParClose
    | ParOpen '=' bool_term bool_term ParClose
    | ParOpen 'distinct' bool_term bool_term ParClose
    | ParOpen 'ite' bool_term bool_term bool_term ParClose
    | ParOpen '=' real_term real_term ParClose
    | ParOpen '<=' real_term real_term ParClose
    | ParOpen '<' real_term real_term ParClose
    | ParOpen '>=' real_term real_term ParClose
    | ParOpen '>' real_term real_term ParClose
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
