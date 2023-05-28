from sys import argv

str_beg = '''grammar SAT;
'''

str_var = '''var{0}
    : ' '
    | '{0}' ' '
    | '-{0}' ' '
    ;
'''

str_sat = '''clause
    : {} '0' '\\n'
    ;
'''

str_cnf = '''clauses
    : {}
    ;
'''

str_head = '''declareHeader
    : 'p' 'cnf' '{}' '{}' '\\n'
    ;
'''

str_end = '''start
    : declareHeader clauses EOF
    ;
'''



n_vars, n_clauses = int(argv[1]), int(argv[2])

print(str_beg)
print('\n'.join([str_var.format(i) for i in range(1, n_vars + 1)]))
print(str_sat.format(' '.join(['var{}'.format(i) for i in range(1, n_vars + 1)])))
print(str_cnf.format('clause ' * n_clauses))
print(str_head.format(n_vars, n_clauses))
print(str_end)

