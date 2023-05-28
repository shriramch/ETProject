import os
import sys
import subprocess


python = sys.executable

def get_cvc4():
    cvc4_link = (
        "https://github.com/CVC4/CVC4/releases/download/1.7/"
        + "cvc4-1.7-x86_64-linux-opt"
    )
    os.system("wget " + cvc4_link)
    os.system("chmod +x cvc4-1.7-x86_64-linux-opt")
    return os.path.abspath("cvc4-1.7-x86_64-linux-opt")


def get_z3_4_8_6():
    z3_link = (
        "https://github.com/Z3Prover/z3/releases/download/z3-4.8.6/"
        + "z3-4.8.6-x64-ubuntu-16.04.zip"
    )
    subprocess.getoutput("wget " + z3_link)
    subprocess.getoutput("unzip z3-4.8.6-x64-ubuntu-16.04.zip")
    return os.path.abspath("z3-4.8.6-x64-ubuntu-16.04/bin/z3")


def run(cmd):
    # os.system(cmd)
    return subprocess.getoutput(cmd)


def mk_cmd(smt_solvers, depth, n):
    cmd = python
    cmd += " bin/enumerate "
    cmd += '"' + ';'.join(smt_solvers) + '" '
    cmd += str(depth) + " "
    cmd += "-n " + str(n)
    return cmd


def parse_output(output):
    """
    Finished search. 118 tests executed, eff: 96.61%
    1945 nodes generated, 21.78s elapsed
    Proved up to depth 3
    0 bugs found
    """

    output = output.split("\n")
    fourth_last_line = [line for line in output if "Finished search" in line]
    tests = fourth_last_line[0].split(" ")[2].strip()
    eff = fourth_last_line[0].split(" ")[6].strip()

    third_last_line = [line for line in output if "nodes generated" in line]
    nodes = third_last_line[0].split(" ")[0].strip()
    time = float(third_last_line[0].split(" ")[3].strip()[:-1])

    last_line = [line for line in output if "bug triggers" in line]
    bugs = last_line[0].split(" ")[0]
    return tests, eff, nodes, time, bugs

print("Prepare grammar...", flush=True)
output = run(python + " bin/prepare_grammar Strings.g4")
print(output)

print("Downloading solvers...", flush=True)
smt_solvers = [get_z3_4_8_6() + " model_validate=true", get_cvc4() + " -q --strings-exp"]

print("$ " + mk_cmd(smt_solvers, 3, 1), flush=True)
output = run(mk_cmd(smt_solvers, 3, 1))
tests, eff, nodes, time, bugs = parse_output(output)
assert int(bugs) == 15


