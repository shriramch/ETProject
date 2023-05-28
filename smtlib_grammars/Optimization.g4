grammar Optimization;

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

integer
    : '0'
    | '1'
    ;

int_term
    : integer
    | ParOpen '-' int_term ParClose
    | ParOpen '-' int_term int_term ParClose
    | ParOpen '+' int_term int_term ParClose
    | ParOpen '*' int_term int_term ParClose
    | ParOpen 'div' int_term int_term ParClose
    | ParOpen 'mod' int_term int_term ParClose
    | ParOpen 'abs' int_term ParClose
    | ParOpen 'to_int' real_term ParClose
    ;

real_term
    : real
    | var_name
    | ParOpen '-' real_term ParClose
    | ParOpen '-' real_term real_term ParClose
    | ParOpen '+' real_term real_term ParClose
    | ParOpen '*' real_term real_term ParClose
    | ParOpen '/' real_term real_term ParClose
    | ParOpen 'to_real' int_term ParClose
    ; 

bool_term
    : ParOpen '=' real_term real_term ParClose
    | ParOpen '<=' real_term real_term ParClose
    | ParOpen '<' real_term real_term ParClose
    | ParOpen '>=' real_term real_term ParClose
    | ParOpen '>' real_term real_term ParClose
    | ParOpen '=' int_term int_term ParClose
    | ParOpen '<=' int_term int_term ParClose
    | ParOpen '<' int_term int_term ParClose
    | ParOpen '>=' int_term int_term ParClose
    | ParOpen '>' int_term int_term ParClose
    | ParOpen 'is_int' real_term ParClose
    ;


checkSat
    : ParOpen 'check-sat' ParClose
    ;

maximizeA
    : ParOpen 'maximize a' ParClose
    ;

maximizeB
    : ParOpen 'maximize b' ParClose
    ;

getObj
    : ParOpen 'get-objectives' ParClose
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
    : declareConsta declareConstb assertStatement maximizeA maximizeB checkSat EOF;
