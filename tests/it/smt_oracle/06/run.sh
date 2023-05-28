#! /bin/bash
BIN_DIR=`realpath ../../../bin`
GRAMMAR_DIR=`realpath ../../../smtlib_grammars`
export PATH=$PATH:$BIN_DIR
patch -u ${GRAMMAR_DIR}/BitvectorArrays.g4 -i grammar.patch -o grammar.g4
Z3_CFG="${BIN_DIR}/cvc5-c16b7a2 -q"
CVC5_CFG="${BIN_DIR}/cvc5-c16b7a2 -q --arrays-eager-lemmas --check-unsat-cores --check-models"
Grammar=`realpath grammar.g4`

echo prepare_grammar $Grammar
prepare_grammar $Grammar 
timeout -s 9 360 enumerate "$Z3_CFG;$CVC5_CFG" 5 -n 20||true

bug_count=`ls bugs/*.smt2|wc -l`

rm -rf logs bugs grammar temp $Grammar 

if [[ $bug_count -gt 0 ]]; then
   exit 0 
fi
exit 1
