#! /bin/bash
if [ ! "$#" -eq 2 ]; then
    echo "Usage: ./sat/run_tests.sh <TARGET_SIZE> <BOUND>"
    exit 2
fi

target_size=$1
bound=$2
grammar="./regex/grammars/REGEX.g4"
target="./regex/target/target.txt"

commands="python3 ./regex/testers/tester.py $target"
commands=$commands";./regex/testers/tester $target"

rm -f temp/*

echo "python3 ./regex/target/gen_target.py $target_size > $target"
python3 ./regex/target/gen_target.py $target_size > $target

echo ./bin/prepare_grammar $grammar 
./bin/prepare_grammar $grammar 

echo ./bin/enumerate -n 8 "$commands" $bound 
./bin/enumerate -n 8 --keep-files "$commands" $bound

