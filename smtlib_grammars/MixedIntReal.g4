grammar Mixed;

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

var_a
    : 'a';

var_b
    : 'b';

int_term
    : integer
    | var_b 
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
    | var_a 
    | ParOpen '-' real_term ParClose
    | ParOpen '-' real_term real_term ParClose
    | ParOpen '+' real_term real_term ParClose
    | ParOpen '*' real_term real_term ParClose
    | ParOpen '/' real_term real_term ParClose
    | ParOpen 'sin' real_term ParClose
    | ParOpen 'cos' real_term ParClose
    | ParOpen 'tan' real_term ParClose
    | ParOpen 'to_real' int_term ParClose
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

assertStatement
    : ParOpen 'assert' bool_term ParClose
    ;

declareConsta
    : ParOpen 'declare-const' 'a' 'Real' ParClose
    ;

declareConstb
    : ParOpen 'declare-const' 'b' 'Int' ParClose
    ;

start
    : declareConsta declareConstb assertStatement checkSat EOF
    ;
