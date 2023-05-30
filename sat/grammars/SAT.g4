grammar SAT;

var1
    : ' '
    | '1' ' '
    | '-1' ' '
    ;

clause
    : var1 '0' '\n'
    ;

clauses
    : clause clause 
    ;

declareHeader
    : 'p' 'cnf' '1' '2' '\n'
    ;

start
    : declareHeader clauses EOF
    ;

