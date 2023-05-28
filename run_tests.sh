#! /bin/bash
EXIT_STATUS=0

# Test generation
./tests/it/test_generation.sh smtlib_grammars/Core.g4 "3" "4" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/Core.g4 "4" "152" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/Ints.g4 "4" "80" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/RealIntsIntVars.g4 "4" "102" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/RealIntsRealVars.g4 "4" "104" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/MixedIntReal.g4 "4" "93" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/Bitvectors.g4 "4" "48" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/BitvectorArrays.g4 "4" "2" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/BitvectorArrays.g4 "5" "200" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/FloatingPoints.g4 "4" "112" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/Strings.g4 "4" "124" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/Optimization.g4 "4" "104" || EXIT_STATUS=$?
./tests/it/test_generation.sh smtlib_grammars/Bags.g4 "4" "14" || EXIT_STATUS=$?

exit $EXIT_STATUS 

