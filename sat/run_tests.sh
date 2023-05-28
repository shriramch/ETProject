#! /bin/bash
if [ ! "$#" -eq 3 ]; then
    echo "Usage: ./sat/run_tests.sh <NUM_VARS> <NUM_CLAUSES> <BOUND>"
    exit 2
fi

vars=$1
clauses=$2
bound=$3
grammar="./sat/grammars/SAT.g4"

commands="cryptominisat5 --verb 0"
commands=$commands";cadical -q"
#commands=$commands";python3 ~/ethz/ast/project/misc/random_sat.py"

rm -f temp/*

echo "python3 ./sat/grammars/gen_grammar.py $vars $clauses > $grammar"
python3 ./sat/grammars/gen_grammar.py $vars $clauses > $grammar

echo ./bin/prepare_grammar $grammar 
./bin/prepare_grammar $grammar 

echo ./bin/enumerate -n 8 "$commands" $bound 
./bin/enumerate -n 8 "$commands" $bound

