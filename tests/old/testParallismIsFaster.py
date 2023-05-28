import os
import sys
import subprocess

python = sys.executable

print("#CORES", os.cpu_count(), flush = True)

def get_cvc4():
    cvc4_link = (
        "https://github.com/CVC4/CVC4/releases/download/1.7/"
        + "cvc4-1.7-x86_64-linux-opt"
    )
    os.system("wget " + cvc4_link)
    os.system("chmod +x cvc4-1.7-x86_64-linux-opt")
    return os.path.abspath("cvc4-1.7-x86_64-linux-opt")


def get_z3():
    z3_link = (
        "https://github.com/Z3Prover/z3/releases/download/z3-4.8.10/"
        + "z3-4.8.10-x64-ubuntu-18.04.zip"
    )
    os.system("wget " + z3_link)
    os.system("unzip z3-4.8.10-x64-ubuntu-18.04.zip")
    return os.path.abspath("z3-4.8.10-x64-ubuntu-18.04/bin/z3")


def mk_cmd(smt_solvers, depth, n):
    cmd = python
    cmd += " bin/enumerate "
    cmd += '"' + ';'.join(smt_solvers) + '" '
    cmd += str(depth) + " "
    cmd += "-n " + str(n)
    return cmd


def run(cmd):
    return subprocess.getoutput(cmd)


def parse_output(output):
    """
    Finished search. 118 tests executed, eff: 96.61%
    1945 nodes generated, 21.78s elapsed
    Proved up to depth 3
    0 bug triggers found
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
smt_solvers = [get_z3() + " model_validate=true", get_cvc4() + " -q --strings-exp"]

print("$ " + mk_cmd(smt_solvers, 3, 1), flush=True)
output = run(mk_cmd(smt_solvers, 3, 1))
# os.system(mk_cmd(smt_solvers, 3, 1))
print("output1", output)
tests1, eff1, nodes1, time1, bugs1 = parse_output(output)
print()

print("$ " + mk_cmd(smt_solvers, 3, 2), flush=True)
output = run(mk_cmd(smt_solvers, 3, 2))
print("output2", output)
tests2, eff2, nodes2, time2, bugs2 = parse_output(output)
print()

assert tests1 == tests2
assert eff1 == eff2
assert nodes1 == nodes2
assert bugs1 == bugs2
assert time2 < time1

# print("$ " + mk_cmd(smt_solvers, 3, 3), flush=True)
# output = run(mk_cmd(smt_solvers, 3, 3))
# print("output3", output)
# tests3, eff3, nodes3, time3, bugs3 = parse_output(output)
# print()

# print("$ " + mk_cmd(smt_solvers, 3, 4), flush=True)
# output = run(mk_cmd(smt_solvers, 3, 4))
# print("output4", output)
# tests4, eff4, nodes4, time4, bugs4 = parse_output(output)
# print()

# assert tests1 == tests2 == tests3 == tests4
# assert eff1 == eff2 == eff3 == eff4
# assert nodes1 == nodes2 == nodes3 == nodes4
# assert bugs1 == bugs2 == bugs3 == bugs4
# assert time4 < time3 < time2 < time1
