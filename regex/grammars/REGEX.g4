grammar REGEX;

/*
lower_char
    : 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'
    | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
    ;

upper_char
    : 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M'
    | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
    ;

number
    : '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    ;
*/

lower_char
    : 'a' 
    ;

upper_char
    : 'A' 
    ;

number
    : '1'
    ;

number_small
    : '1' | '2' | '3'
    ;

number_big
    : '3' | '4' | '5'
    ;

basic_regex
    : lower_char
    | upper_char
    | number
    | '(' regex ')' 
    | '[a-z]'
    | '[A-Z]'
    | '[0-9]' 
    | '[^a-z]'
    | '[^A-Z]'
    | '[^0-9]'
    ; 


modifying_appendants
    : '*'
    | '+'
    | '?' 
    | '*?'
    | '+?'
    | '??' 
    | '*+'
    | '++'
    | '?+'
    | '{' number_small '}'
    | '{' number_big '}'
    | '{' number_small ',' number_big '}'
    | '{' number_small ',' number_big '}' '?'
    | '{' number_small ',' number_big '}' '+'
    ; 

regex
    : basic_regex
    | basic_regex modifying_appendants
    | basic_regex regex 
    | basic_regex '|' regex 
    ;

complete_regex
    : regex
    | '^' regex
    | regex '$'
    | '^' regex '$'
    ;

start
    : complete_regex EOF
    ;
