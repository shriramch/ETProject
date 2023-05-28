grammar FloatingPoints;

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
    : '(_ FloatingPoint 11  53)'
    ;

declareConsta
    : ParOpen 'declare-const' 'a' var_type ParClose
    ;

declareConstb
    : ParOpen 'declare-const' 'b' var_type ParClose
    ;

fp_consts
    : '(fp #b0 #b00000000000 #b0000000000000000000000000000000000000000000000000000)'
    | '(fp #b1 #b11111111111 #b1111111111111111111111111111111111111111111111111111)'
    ;


rounding_mode
    : 'RNE' 
    | 'RNA'
    | 'RTP'
    | 'RTN'
    | 'RTZ'
    ;

fp_term 
    : fp_consts
    | var_name
    | ParOpen 'fp.abs' fp_term ParClose
    | ParOpen 'fp.neg' fp_term ParClose
    | ParOpen 'fp.add' rounding_mode fp_term fp_term ParClose
    | ParOpen 'fp.sub' rounding_mode fp_term fp_term ParClose
    | ParOpen 'fp.mul' rounding_mode fp_term fp_term ParClose
    | ParOpen 'fp.div' rounding_mode fp_term fp_term ParClose
    | ParOpen 'fp.fma' rounding_mode fp_term fp_term fp_term ParClose
    | ParOpen 'fp.sqrt' rounding_mode fp_term ParClose
    | ParOpen 'fp.roundToIntegral' rounding_mode fp_term ParClose
    | ParOpen 'fp.rem' fp_term fp_term ParClose
    | ParOpen 'fp.min' fp_term fp_term ParClose
    | ParOpen 'fp.max' fp_term fp_term ParClose
    ;

bool_term
    : ParOpen '=' fp_term fp_term ParClose
    | ParOpen 'distinct' fp_term fp_term ParClose
    | ParOpen 'fp.leq' fp_term fp_term ParClose
    | ParOpen 'fp.lt' fp_term fp_term ParClose
    | ParOpen 'fp.geq' fp_term fp_term ParClose
    | ParOpen 'fp.gt' fp_term fp_term ParClose
    | ParOpen 'fp.eq' fp_term fp_term ParClose
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
