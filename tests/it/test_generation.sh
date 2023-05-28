#! /bin/bash
if [ ! "$#" -eq 3 ]; then
    echo "Usage: ./tests/it/test_generation <GRAMMAR> <BOUND> <NUM_EXPECTED_TESTS>"
    exit 2
fi
grammar=$1
bound=$2
expected=$3
rm -rf temp/*

echo ./bin/prepare_grammar $grammar 
./bin/prepare_grammar $grammar 

echo ./bin/enumerate --generate-only --keep-files "" $bound 
./bin/enumerate --generate-only --keep-files "" $bound  &> /dev/null

actual=`ls temp|wc -l`
if [ ! "$actual" -eq $expected ]; then 
    echo "[FAIL] expected:" $expected "actual:" $actual  
    exit 1
fi
unique=`md5sum temp/*|awk -F " " '{print $1}'|sort|uniq -c |wc -l`
if [ ! "$unique" -eq $expected ]; then 
    echo "[FAIL] expected:" $expected "unique:" $unique 
fi
