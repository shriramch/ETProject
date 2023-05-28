import os
import sys
import subprocess

python = sys.executable


def run(cmd):
    return subprocess.getoutput(cmd)
    # os.system(cmd)


def parse_counts(output):
    d = dict()
    for line in output.split("\n"):
        bound = int(line.split(" ")[0].split("=")[-1])
        try:
            number = int(line.split(" ")[-1])
        except:
            number = float(line.split(" ")[-1])
        d[bound] = number
    return d


def parse_enumerate(output):
    return int(output.split("\n")[-4].split(" ")[2])


def run_test(grammar):
    print(grammar)
    run("bin/prepare_grammar " + grammar)
    output = run("bin/count " + grammar)
    counted = parse_counts(output)

    for i in range(3, 4): # only testing depth=3 for scalability 
        computed = parse_enumerate(run('bin/enumerate "z3" ' + str(i)))
        print(counted[i] == computed), print("depth:",str(i),"counted:"+str(counted[i]), "computed:",str(computed))


grammars = ["smtlib_grammars/"+f for f in os.listdir("smtlib_grammars") if f.endswith("g4")]
for grammar in grammars:
    run_test(grammar)
