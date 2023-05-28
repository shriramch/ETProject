grammar SAT;

var1
    : ' '
    | '1' ' '
    | '-1' ' '
    ;

var2
    : ' '
    | '2' ' '
    | '-2' ' '
    ;

var3
    : ' '
    | '3' ' '
    | '-3' ' '
    ;

var4
    : ' '
    | '4' ' '
    | '-4' ' '
    ;

var5
    : ' '
    | '5' ' '
    | '-5' ' '
    ;

clause
    : var1 var2 var3 var4 var5 '0' '\n'
    ;

clauses
    : clause clause clause clause clause clause clause clause clause clause 
    ;

declareHeader
    : 'p' 'cnf' '5' '10' '\n'
    ;

start
    : declareHeader clauses EOF
    ;

