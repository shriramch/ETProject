grammar Strings;

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
    : 'String'
    ;

integer
    : '0'
    | '1'
    ;

integer_term
    : integer 
    | ParOpen 'str.to_int' str_term ParClose
    | ParOpen 'str.indexof' str_term str_term integer_term ParClose
    ;

string 
    : '""'
    | '"a"'
    ;

str_term
    : string
    | var_name
    | ParOpen 'str.++' str_term str_term ParClose
    | ParOpen 'str.at' str_term integer_term ParClose
    | ParOpen 'str.substr' str_term integer_term integer_term ParClose
    | ParOpen 'str.replace' str_term str_term str_term ParClose
    | ParOpen 'str.replace_all' str_term str_term str_term ParClose
    | ParOpen 'str.from_int' integer_term ParClose
    ;

regex_const
    : 're.none'
    | 're.all' 
    | 're.allchar'
    ;

regex_term
    : regex_const
    | ParOpen 're.comp' regex_term ParClose
    | ParOpen 're.+' regex_term ParClose
    | ParOpen 're.opt' regex_term ParClose
    | ParOpen 're.union' regex_term regex_term ParClose
    | ParOpen 're.inter' regex_term regex_term ParClose
    | ParOpen 're.++' regex_term regex_term ParClose
    | ParOpen 're.diff' regex_term regex_term ParClose
    | ParOpen 're.*' regex_const ParClose
    | ParOpen 'str.to_re' str_term ParClose
    | ParOpen 're.range' str_term str_term ParClose
    ;

bool_term
    : ParOpen 'not' bool_term ParClose
    | ParOpen 'and' bool_term bool_term ParClose
    | ParOpen 'or' bool_term bool_term ParClose
    | ParOpen 'xor' bool_term bool_term ParClose
    | ParOpen '=' bool_term bool_term ParClose
    | ParOpen 'distinct' bool_term bool_term ParClose
    | ParOpen 'ite' bool_term bool_term bool_term ParClose
    | ParOpen '=' str_term str_term ParClose
    | ParOpen 'distinct' str_term str_term ParClose
    | ParOpen 'str.<=' str_term str_term ParClose
    | ParOpen 'str.prefixof' str_term str_term ParClose
    | ParOpen 'str.suffixof' str_term str_term ParClose
    | ParOpen 'str.contains' str_term str_term ParClose
    | ParOpen 'str.is_digit' str_term ParClose
    | ParOpen 'str.in_re' str_term regex_term ParClose
    ;

declareConsta
    : ParOpen 'declare-const' 'a' var_type ParClose
    ;

declareConstb
    : ParOpen 'declare-const' 'b' var_type ParClose
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
