grammar BitvectorArrays;

ParOpen
    : '('
    ;

ParClose
    : ')'
    ;


var_type_arr
    : '(Array (_ BitVec 64) (_ BitVec 64))'
    ;

declareConsta
    : ParOpen 'declare-const ' 'a' var_type_arr ParClose
    ;

var_type_bv
    : '(_ BitVec 64)'
    ;

declareConstb
    : ParOpen 'declare-const ' 'b' var_type_bv ParClose
    ;

bv_const
   : '#x0000000000000000'
   | '#x1111111111111111'
   ;

var_name_b
    : 'b'
    ;

bitvec_term 
    : bv_const
    | var_name_b
    | ParOpen 'bvneg' bitvec_term ParClose
    | ParOpen 'bvor' bitvec_term ParClose
    | ParOpen 'bvadd' bitvec_term bitvec_term ParClose
    | ParOpen 'select' arr_term bitvec_term ParClose
    ;

var_name_a
    : 'a'
    ;

arr_term 
    : var_name_a
    | ParOpen 'store' var_name_a bitvec_term bitvec_term ParClose
    ;

bool_term
    : ParOpen '=' arr_term arr_term ParClose
    | ParOpen 'distinct' arr_term arr_term ParClose
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
