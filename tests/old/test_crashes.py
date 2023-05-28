import os
import sys
import subprocess

python = sys.executable


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
    crash_issues = 0
    if len(os.listdir("./bugs")) != 0:
        crash_issues = 1
    return crash_issues, cmd


def create_mocksolver_msg(msg, script_fn):
    code = "#! /usr/bin/env python3\n"
    code += 'msg="""' + msg + '"""\n'
    code += "print(msg)"
    open(script_fn, "w").write(code)
    os.system("chmod +x " + script_fn)


def test_crash_list(msg, fn):
    print("Test", fn)
    solver = "crash.py"
    create_mocksolver_msg(msg, solver)
    first_config = os.path.abspath(solver)
    second_config = os.path.abspath(solver)
    crash, cmd = call_fuzzer(first_config, second_config)

    if crash != 1:
        print("[ERROR] Crash", fn, "cannot be captured.")
        print(cmd)
        exit(1)
    else:
        os.system("rm -rf " + solver)

if __name__ == "__main__":
    root_folder = os.path.dirname(os.path.realpath(__file__))
    crash_folder = root_folder + "/crashes"
    for fn in os.listdir(crash_folder):
        fn = crash_folder + "/" + fn
        msg = open(fn).read()
        test_crash_list(msg, fn)
        os.system("rm -rf ./bugs/*")
