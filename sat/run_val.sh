#! /bin/bash
if [ ! "$#" -eq 4 ]; then
    echo "Usage: ./sat/run_tests.sh <NUM_VARS> <NUM_CLAUSES> <BOUND> <MAX_TESTS>"
    exit 2
fi

vars=$1
clauses=$2
bound=$3
maxtests=$4
grammar="./sat/grammars/SAT.g4"

tester="./sat/tester.py"
tempfile="temp"
ansfile="logs/ans.txt"
bugfile="bugs/verify_bug.txt"

rm -f "$tempfile"/*

echo "python3 ./sat/grammars/gen_grammar.py $vars $clauses > $grammar"
python3 ./sat/grammars/gen_grammar.py $vars $clauses > $grammar

echo ./bin/prepare_grammar $grammar 
./bin/prepare_grammar $grammar 

echo ./bin/enumerate -n 8 -m $maxtests --keep-files --generate-only "" $bound 
./bin/enumerate -n 8 -m $maxtests --keep-files --generate-only "" $bound

for file in "$tempfile"/* 
do
	cryptominisat5 --verb 0 $file > $ansfile
	python3 $tester $bugfile $ansfile $file 
	
	cadical -q $file > $ansfile 
	python3 $tester $bugfile $ansfile $file 
done

rm -f $ansfile
