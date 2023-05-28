"""
Script to test bug detection logic of yinyang (src/core/Fuzzer.py).
"""
import os
import sys
import random
import subprocess

python = sys.executable
script_dir = os.path.dirname(os.path.realpath(__file__))
ERRORS = False


def newest_log(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def is_sound(res1, res2):
    for i in range(len(res1)):
        if not (res1[i] == res2[i] or res1[i] == "unknown" 
                or res2[i] == "unknown"):
            return False
    return True


def call_fuzzer(first_config, second_config):
    cmd = (
        python
        + " enumerator.py "
        + '"'
        + first_config
        + ";"
        + second_config
        + '" '
        + "3 "
        + "-m 1"
    )
    output = subprocess.getoutput(cmd)
    print(output)
    issues = 0
    if len(os.listdir("./bugs")) != 0:
        issues = 1
    if "Error" in output:
        exit(1)
    return issues, cmd


def create_mocksmt2(fn):
    open(fn, "w").write(
        "(declare-fun x () Int)\n(declare-fun y () Int)\n(assert (= x y))"
    )


def create_mocksolver_msg(msg, script_fn):
    code = "#! /usr/bin/env python3\n"
    code += 'msg="""' + msg + '"""\n'
    code += "print(msg)"
    open(script_fn, "w").write(code)
    os.system("chmod +x " + script_fn)


def create_mocksolver_segfault(script_fn):
    code = "#! /usr/bin/env python3\n"
    code += "import sys;sys.setrecursionlimit(1<<30);f=lambda f:f(f);f(f)"
    open(script_fn, "w").write(code)
    os.system("chmod +x " + script_fn)


def create_mocksolver_timeout(script_fn):
    code = "#! /usr/bin/env python3\n"
    code += "import time; time.sleep(30)"
    open(script_fn, "w").write(code)
    os.system("chmod +x " + script_fn)


def test_crash_list():
    print("*** (1) Test crash list")
    #
    os.system("rm -rf ./bugs/*")
    #
    solver = "crash.py"
    msg = """
    Fatal failure within void CVC4::SmtEngine::checkUnsatCore() at src/smt/smt_engine.cpp:1464
    Internal error detectedSmtEngine::checkUnsatCore(): produced core was satisfiable.
    Aborted
    """  # noqa: E501
    create_mocksolver_msg(msg, solver)
    first_config = os.path.abspath(solver)
    second_config = os.path.abspath(solver)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 1:
        print("[ERROR] Crash cannot be captured.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + solver)


def test_ignore_list():
    print("*** (2) Test ignore list")
    #
    os.system("rm -rf ./bugs/*")
    #
    solver = "ignore_list.py"
    msg = """
    formula3.smt2:2.12: No set-logic command was given before this point.
    formula3.smt2:2.12: CVC4 will make all theories available.
    formula3.smt2:2.12: Consider setting a stricter logic for (likely) better performance.
    formula3.smt2:2.12: To suppress this warning in the future use (set-logic ALL).
    (error "Parse Error: formula3.smt2:2.23: Symbol 'Bdool' not declared as a type

      (declare-fun v () Bdool )
    ")
    """  # noqa: E501

    create_mocksolver_msg(msg, solver)
    first_config = os.path.abspath(solver)
    second_config = os.path.abspath(solver)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 0:
        print("[ERROR] test should be ignored.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + solver)



def test_segfault():
    print("*** (3) Test segfault")
    #
    os.system("rm -rf ./bugs/*")
    #
    solver = "segfault.py"
    create_mocksolver_segfault(solver)
    first_config = os.path.abspath(solver)
    second_config = os.path.abspath(solver)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 1:
        print("[ERROR] Segfault undetected.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + solver)


def test_timeout():
    print("*** (4) Test timeout")
    #
    os.system("rm -rf ./bugs/*")
    #
    timeout_solver = "timeout.py"
    sat_solver = "sat_solver.py"
    create_mocksolver_timeout(timeout_solver)
    msg = "sat"
    create_mocksolver_msg(msg, sat_solver)
    first_config = os.path.abspath(timeout_solver)
    second_config = os.path.abspath(sat_solver)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 0:
        print("[ERROR] test should be ignored.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + sat_solver)



def test_empty_output():
    print("*** (5) Test empty output")
    #
    os.system("rm -rf ./bugs/*")
    #
    empty_solver = "empty_solver.py"
    sat_solver = "sat_solver.py"
    msg = ""
    create_mocksolver_msg(msg, empty_solver)
    msg = "sat"
    create_mocksolver_msg(msg, sat_solver)
    first_config = os.path.abspath(empty_solver)
    second_config = os.path.abspath(sat_solver)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 0:
        print("[ERROR] test should be ignored.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + sat_solver)
        os.system("rm -rf " + empty_solver)


def test_unsoundness():
    print("*** (6) Unsoundness")
    #
    os.system("rm -rf ./bugs/*")
    #
    values = ["sat", "unsat", "unknown"]
    k = random.randint(1, 20)
    res1 = random.choices(values, k=k)
    j = random.randint(0, k - 1)
    res1[j] = random.choice(["sat", "unsat"])
    res2 = random.choices(values, k=k)
    while is_sound(res1, res2):
        res2 = random.choices(values, k=k)
    solver1 = "solver1.py"
    create_mocksolver_msg("\n".join(res1), solver1)
    solver2 = "solver2.py"
    first_config = os.path.abspath(solver1)
    second_config = os.path.abspath(solver2)
    create_mocksolver_msg("\n".join(res2), solver2)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 1:
        print("[ERROR] Unsoundness undetected.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + solver1)
        os.system("rm -rf " + solver2)


def test_soundness():
    print("*** (7) Soundness")
    #
    os.system("rm -rf ./bugs/*")
    #
    values = ["sat", "unsat", "unknown"]
    k = random.randint(1, 20)
    res1 = random.choices(values, k=k)
    res2 = res1
    j = random.randint(0, k - 1)
    res1[j] = random.choice(["sat", "unsat"])

    for i in range(len(res1)):
        if (res1[i] == "sat" or res1[i] == "unsat")\
           and random.choice([True, False]):
            res2[i] = "unknown"
    solver1 = "solver1.py"
    create_mocksolver_msg("\n".join(res1), solver1)
    solver2 = "solver2.py"
    first_config = os.path.abspath(solver1)
    second_config = os.path.abspath(solver2)
    create_mocksolver_msg("\n".join(res2), solver2)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )

    if issues != 0:
        print("[ERROR] False positive.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + solver1)
        os.system("rm -rf " + solver2)


def test_duplicate_list():
    print("*** (8) Test duplicate list")
    #
    os.system("rm -rf ./bugs/*")
    #
    solver = "crash.py"
    msg = """
Fatal failure within void CVC4::SmtEngine::checkUnsatCore() at src/smt/smt_mock.cpp:1489
Internal error detectedSmtEngine::checkMock(): produced core was satisfiable.
Aborted
"""  # noqa: E501
    config_py = """
solvers = []
crash_list = [
    "Exception",
    "lang.AssertionError",
    "lang.Error",
    "runtime error",
    "LEAKED",
    "Leaked",
    "Segmentation fault",
    "segmentation fault",
    "segfault",
    "ASSERTION",
    "Assertion",
    "Fatal failure",
    "Internal error detected",
    "an invalid model was generated",
    "Failed to verify",
    "failed to verify",
    "ERROR: AddressSanitizer:",
    "invalid expression",
    "Aborted"
]

duplicate_list = [
    "src/smt/smt_mock.cpp:1489"
]

ignore_list = [
    "(error ",
    "unsupported",
    "unexpected char",
    "failed to open file",
    "Expected result sat but got unsat",
    "Expected result unsat but got sat",
    "Parse Error",
    "Cannot get model",
    "Symbol 'str.to-re' not declared as a variable",
    "Symbol 'str.to.re' not declared as a variable",
    "Unimplemented code encountered",
]

"""
    os.system("mv yinyang/config/config.py yinyang/config/config.py.orig")
    with open("yinyang/config/Config.py", "w") as f:
        f.write(config_py)
    create_mocksolver_msg(msg, solver)
    first_config = os.path.abspath(solver)
    second_config = os.path.abspath(solver)
    issues, cmd = call_fuzzer(
        first_config, second_config
    )
    if issues != 0:
        print("[ERROR] False positive.")
        print(cmd)
        exit(1)



if __name__ == "__main__":
    # Create empty mock.smt2, set fuzzer opts
    FN = "mock.smt2"
    create_mocksmt2(FN)
    OPTS = "-i 1 -m 1 "
    test_crash_list()
    print()
    test_ignore_list()
    print()
    test_segfault()
    print()
    test_timeout()
    print()
    test_empty_output()
    print()
    test_unsoundness()
    print()
    test_soundness()
    print()
    # test_duplicate_list()
