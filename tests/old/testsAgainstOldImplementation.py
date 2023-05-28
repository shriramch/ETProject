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


def get_z3():
    z3_link = (
        "https://github.com/Z3Prover/z3/releases/download/z3-4.8.10/"
        + "z3-4.8.10-x64-ubuntu-18.04.zip"
    )
    os.system("wget " + z3_link)
    os.system("unzip z3-4.8.10-x64-ubuntu-18.04.zip")
    return os.path.abspath("z3-4.8.10-x64-ubuntu-18.04/bin/z3")


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


def mk_old_cmd(smt_solvers, depth, n):
    cmd = python
    cmd += " enumerator.py "
    cmd += '"' + ';'.join(smt_solvers) + '" '
    cmd += str(depth)
    return cmd


print("Prepare grammar...", flush=True)
output = run(python + " bin/prepare_grammar Strings.g4")

print("Downloading solvers...", flush = True)
smt_solvers = [get_z3() + " model_validate=true", get_cvc4() + " -q --strings-exp"]
# smt_solvers = ["z3", "cvc4"]

print("Checking out old implementation", flush = True)
run("rm -rf old_impl; unzip old_impl.zip")

for depth in [2,3]:
    print("## depth = "+str(depth))
    print("$ cd old_impl && " + mk_old_cmd(smt_solvers, depth, 1), flush=True)
    output = run("cd old_impl && " + mk_old_cmd(smt_solvers, depth, 1))
    tests_old, eff_old, nodes_old, time_old, bugs_old = parse_output(output)
    print("----old----------------------\n"+output)

    print()

    print("$ " + mk_cmd(smt_solvers, depth, 1), flush=True)
    output = run(mk_cmd(smt_solvers, depth, 1))
    tests, eff, nodes, time, bugs = parse_output(output)
    print("----new----------------------\n"+output)

    assert tests_old == tests
    assert nodes_old == nodes
    assert bugs_old == bugs
