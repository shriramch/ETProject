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

var6
    : ' '
    | '6' ' '
    | '-6' ' '
    ;

var7
    : ' '
    | '7' ' '
    | '-7' ' '
    ;

var8
    : ' '
    | '8' ' '
    | '-8' ' '
    ;

var9
    : ' '
    | '9' ' '
    | '-9' ' '
    ;

var10
    : ' '
    | '10' ' '
    | '-10' ' '
    ;

clause
    : var1 var2 var3 var4 var5 var6 var7 var8 var9 var10 '0' '\n'
    ;

clauses
    : clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause clause 
    ;

declareHeader
    : 'p' 'cnf' '10' '25' '\n'
    ;

start
    : declareHeader clauses EOF
    ;

