grammar Bags;

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
    : '(Bag String)'
    ;

declareConsta
    : ParOpen 'declare-fun' 'a ()' var_type ParClose
    ;

declareConstb
    : ParOpen 'declare-fun' 'b ()' var_type ParClose
    ;

string 
    : '""'
    | '"a"'
    ;

str_term
    : string
    | ParOpen 'bag.choose' bag_term ParClose
    ;

bag_term
    : var_name
    | ParOpen 'bag.union_disjoint' bag_term bag_term ParClose
    | ParOpen 'bag.union_max' bag_term bag_term ParClose
    | ParOpen 'bag.intersection' bag_term bag_term ParClose
    | ParOpen 'bag.difference_remove' bag_term bag_term ParClose
    | ParOpen 'bag.difference_subtract' bag_term bag_term ParClose
    | ParOpen 'bag.subbag' bag_term bag_term ParClose
    | ParOpen 'as bag.empty' var_type ParClose
    ;

bool_term
    : ParOpen '=' str_term str_term ParClose
    | ParOpen 'distinct' str_term str_term ParClose
    | ParOpen 'bag.member' str_term bag_term ParClose
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
