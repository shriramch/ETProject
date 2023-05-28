grammar Bitvectors;

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
    : '(_ BitVec 64)'
    ;

declareConsta
    : ParOpen 'declare-const' 'a' var_type ParClose
    ;

declareConstb
    : ParOpen 'declare-const' 'b' var_type ParClose
    ;

bv_const
   : '#x0000000000000000'
   | '#x1111111111111111'
   ;

bitvec_term 
    : bv_const
    | var_name 
    | ParOpen 'bvnot' bitvec_term ParClose
    | ParOpen 'bvneg' bitvec_term ParClose
    | ParOpen 'bvand' bitvec_term bitvec_term ParClose
    | ParOpen 'bvor' bitvec_term bitvec_term ParClose
    | ParOpen 'bvadd' bitvec_term bitvec_term ParClose
    | ParOpen 'bvmul' bitvec_term bitvec_term ParClose
    | ParOpen 'bvudiv' bitvec_term bitvec_term ParClose
    | ParOpen 'bvurem' bitvec_term bitvec_term ParClose
    | ParOpen 'bvshl' bitvec_term bitvec_term ParClose
    | ParOpen 'bvlshr' bitvec_term bitvec_term ParClose
    ;

bool_term
    : ParOpen 'not' bool_term ParClose
    | ParOpen 'and' bool_term bool_term ParClose
    | ParOpen 'or' bool_term bool_term ParClose
    | ParOpen 'xor' bool_term bool_term ParClose
    | ParOpen '=' bool_term bool_term ParClose
    | ParOpen 'distinct' bool_term bool_term ParClose
    | ParOpen 'ite' bool_term bool_term bool_term ParClose
    | ParOpen 'bvult' bitvec_term bitvec_term ParClose
    | ParOpen '=' bitvec_term bitvec_term ParClose
    | ParOpen 'distinct' bitvec_term bitvec_term ParClose
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
