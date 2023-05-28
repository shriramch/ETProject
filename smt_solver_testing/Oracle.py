import re
import time
import signal
import shutil
import logging
import subprocess
import multiprocessing as mp

from enum import Enum
from smt_solver_testing.Logger import (
    log_crash_trigger, log_duplicate_trigger, log_ignore_list_mutant,
    log_segfault_trigger, log_solver_timeout, log_invalid_mutant,
    log_soundness_trigger
)

from multiprocessing import Process, Value, Array, Lock, Manager

mutex = Lock()

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

def plain(cli):
    plain_cli = ""
    for token in cli.split(" "):
        plain_cli += token.split("/")[-1]
    return escape(plain_cli)


def escape(s):
    s = s.replace(".", "")
    s = s.replace("=", "")
    return s


def report_diff(
    scratchfile,
    bugtype,
    ref_cli,
    ref_stdout,
    ref_stderr,
    sol_cli,
    sol_stdout,
    sol_stderr,
    args
):
    plain_cli = plain(sol_cli)
    # format: <solver><{crash,wrong,invalid_model}><seed>.<random-str>.smt2
    report = "%s/%s-%s-%s.smt2" % (
        args.bugfolder,
        bugtype,
        plain_cli,
        scratchfile.split("/")[-1].split(".")[-2]
    )
    try:
        shutil.copy(scratchfile, report)
    except Exception:
        print("error: couldn't copy scratchfile to bugfolder.")
        exit(1)

    logpath = "%s/%s-%s-%s.output" % (
        args.bugfolder,
        bugtype,
        plain_cli,
        scratchfile.split("/")[-1].split(".")[-2]
    )
    with open(logpath, "w") as log:
        log.write("*** REFERENCE \n")
        log.write("command: " + ref_cli + "\n")
        log.write("stderr:\n")
        log.write(ref_stderr)
        log.write("stdout:\n")
        log.write(ref_stdout)
        log.write("\n\n*** INCORRECT \n")
        log.write("command: " + sol_cli + "\n")
        log.write("stderr:\n")
        log.write(sol_stderr)
        log.write("stdout:\n")
        log.write(sol_stdout)
    return report


def report(scratchfile, bugtype, cli, stdout, stderr, args):
    plain_cli = plain(cli)
    # format: <solver><{crash,wrong,invalid_model}><seed>.smt2
    report = "%s/%s-%s-%s.smt2" % (
        args.bugfolder,
        bugtype,
        plain_cli,
        scratchfile.split("/")[-1].split(".")[-2]
    )
    try:
        shutil.copy(scratchfile, report)
    except Exception as e:
        # print("error: couldn't copy scratchfile to bugfolder.")
        logging.error("error: couldn't copy scratchfile to bugfolder.")
        exit(1)
    logpath = "%s/%s-%s-%s.output" % (
        args.bugfolder,
        bugtype,
        plain_cli,
        scratchfile.split("/")[-1].split(".")[-2]
    )
    with open(logpath, "w") as log:
        log.write("command: " + cli + "\n")
        log.write("stderr:\n")
        log.write(stderr)
        log.write("stdout:\n")
        log.write(stdout)
    return report


def grep_result(stdout):
    """
    Grep the result from the stdout of a solver.
    """
    result = SolverResult()
    for line in stdout.splitlines():
        if re.search("^unsat$", line, flags=re.MULTILINE):
            result.append(SolverQueryResult.UNSAT)
        elif re.search("^sat$", line, flags=re.MULTILINE):
            result.append(SolverQueryResult.SAT)
        elif re.search("^unknown$", line, flags=re.MULTILINE):
            result.append(SolverQueryResult.UNKNOWN)
    return result


def in_list(stdout, stderr, lst):
    stdstream = stdout + " " + stderr
    for err in lst:
        if err in stdstream:
            return True
    return False

def in_crash_list(stdout, stderr):
    return in_list(stdout, stderr, crash_list)


def in_duplicate_list(stdout, stderr):
    return in_list(stdout, stderr, duplicate_list)


def in_ignore_list(stdout, stderr):
    return in_list(stdout, stderr, ignore_list)

class Solver:
    def __init__(self, cil):
        self.cil = cil

    def solve(self, file, timeout, debug=False):
        total_time = -1
        try:
            t1 = time.time()
            mem_limit = 1048576
            cmd = 'ulimit -Sv {};timeout -s 9 64 '.format(mem_limit) + self.cil + " "+ file
            # cmd = list(filter(None, self.cil.split(" "))) + [file]
            if debug:
                print(cmd)
            output = subprocess.run(
                cmd,
                timeout=timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            total_time = time.time() - t1

        except subprocess.TimeoutExpired as te:
            if te.stdout and te.stderr:
                stdout = te.stdout.decode()
                stderr = te.stderr.decode()
            else:
                stdout = ""
                stderr = ""
            return stdout, stderr, 137, -1

        except ValueError:
            stdout = ""
            stderr = ""
            return stdout, stderr, 0, -1

        except FileNotFoundError:
            print('error: solver "' + cmd[0] + '" not found', flush=True)
            exit(ERR_USAGE)

        stdout = output.stdout.decode()
        stderr = output.stderr.decode()
        returncode = output.returncode

        if debug:
            print("output: " + stdout + "\n" + stderr)

        return stdout, stderr, returncode, total_time 

# class Solver:
    # def __init__(self, cil):
        # self.cil = cil

    # def solve(self, file, timeout, debug=False):
        # total_time = -1
        # try:
            # t1 = time.time()
            # cmd = list(filter(None, self.cil.split(" "))) + [file]
            # if debug:
                # print("cmd: " + " ".join(cmd), flush = True)

            # output = subprocess.run(
                # cmd,
                # timeout=timeout,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                # shell=False,
            # )
            # total_time = time.time() - t1

        # except subprocess.TimeoutExpired as te:
            # if te.stdout and te.stderr:
                # stdout = te.stdout.decode()
                # stderr = te.stderr.decode()
            # else:
                # stdout = ""
                # stderr = ""
            # return stdout, stderr, 137, -1

        # except ValueError:
            # stdout = ""
            # stderr = ""
            # return stdout, stderr, 0, -1

        # except FileNotFoundError:
            # print('error: solver "' + cmd[0] + '" not found', flush=True)
            # exit(ERR_USAGE)

        # stdout = output.stdout.decode()
        # stderr = output.stderr.decode()
        # returncode = output.returncode

        # if debug:
            # print("output: " + stdout + "\n" + stderr)

        # return stdout, stderr, returncode, total_time 


def sr2str(sol_res):
    if sol_res == SolverQueryResult.SAT:
        return "sat"
    if sol_res == SolverQueryResult.UNSAT:
        return "unsat"
    if sol_res == SolverQueryResult.UNKNOWN:
        return "unknown"


class SolverResult:
    """
    Class to store the result of multiple solver check-sat queries.
    :lst a list of multiple "SolverQueryResult" items
    """

    def __init__(self, result=None):
        self.lst = []
        if result:
            self.lst.append(result)

    def append(self, result):
        self.lst.append(result)

    def equals(self, rhs):
        if type(rhs) == SolverQueryResult:
            return len(self.lst) == 1 and self.lst[0] == rhs
        elif type(rhs) == SolverResult:
            if len(self.lst) != len(rhs.lst):
                return False
            for index in range(0, len(self.lst)):
                if (
                    self.lst[index] != SolverQueryResult.UNKNOWN
                    and rhs.lst[index] != SolverQueryResult.UNKNOWN
                    and self.lst[index] != rhs.lst[index]
                ):
                    return False
            return True
        else:
            return False

    def __str__(self):
        s = sr2str(self.lst[0])
        for res in self.lst[1:]:
            s += "\n" + sr2str(res)
        return s


class SolverQueryResult(Enum):
    """
    Enum storing the result of a single solver check-sat query.
    """

    SAT = 0  # solver query returns "sat"
    UNSAT = 1  # solver query returns "unsat"
    UNKNOWN = 2  # solver query reports "unknown"



def test(i, fn, args, num_active_processes, solver_stats=None):
    """
    returns num_bugs, num_ineffective_tests
    """
    oracle = SolverResult(SolverQueryResult.UNKNOWN)
    reference = None
    num_ineffective_tests = 0
    num_bugs = 0
    if args.solver_summary_stats:
        num_decided_formulas = 0

    fn_tmp = open(fn.strip("smt2")+"time", 'a')

    for solver_cli in args.CLIS:
        solver = Solver(solver_cli)

        while num_active_processes[0] >= mp.cpu_count() - 4:    
            pass

        with mutex:
            num_active_processes[0] += 1 
        
        stdout, stderr, exitcode, total_time = solver.solve(
            fn, args.timeout
        )
        with mutex:
            num_active_processes[0] -= 1

        fn_tmp.write(solver.cil + ","+ str(total_time)+",")

        if args.oracle_debug:
            print(solver_cli + " " + fn, flush=True)
            print(stdout, stderr, flush = True)

        if args.solver_summary_stats:
            if stdout.strip() == "unknown":
                solver_stats[solver_cli+"-unknown"] += 1
                fn_tmp.write("unknown\n")
                continue

        # Match stdout and stderr against the crash list
        # (see yinyang/config/Config.py:27) which contains various
        # crash messages such as assertion errors, check failure,
        # invalid models, etc.
        if in_crash_list(stdout, stderr):

            # Match stdout and stderr against the duplicate list
            # (see yinyang/config/Config.py:51) to prevent catching
            # duplicate bug triggers.
            if not in_duplicate_list(stdout, stderr):
                path = report(
                    fn, "crash", solver_cli, stdout, stderr, args
                )
                log_crash_trigger(path)
                num_bugs += 1
            else:
                log_duplicate_trigger()
            
            fn_tmp.write("crash\n")
        else:

            # Check whether the solver call produced errors, e.g, related
            # to its parser, options, type-checker etc., by matching stdout
            # and stderr against the ignore list
            # (see yinyang/config/Config.py:54).
            if in_ignore_list(stdout, stderr):
                log_ignore_list_mutant(solver_cli, fn)
                num_ineffective_tests += 1
                solver_stats[solver_cli+"-error/rejected"] += 1
                fn_tmp.write("rejected\n")
                continue  # Continue to the next solver.

            if exitcode != 0:

                # Check whether the solver crashed with a segfault.
                if exitcode == -signal.SIGSEGV or exitcode == 245:
                    path = report(
                        fn, "segfault", solver_cli, stdout, stderr, args
                    )
                    log_segfault_trigger(args, fn)
                    num_bugs += 1
                    fn_tmp.write(",segfault\n")
                    # return num_bugs, num_ineffective_tests
                    continue

                # Check whether the solver timed out.
                elif exitcode == 137:
                    # log_solver_timeout(args, solver_cli, fn)
                    if args.solver_summary_stats:
                        solver_stats[solver_cli+"-timeout"] += 1
                        fn_tmp.write("timeout\n")
                    num_ineffective_tests += 1
                    continue  # Continue to the next solver.

                # Check whether a "command not found" error occurred.
                elif exitcode == 127:
                    if args.solver_summary_stats:
                        solver_stats[solver_cli+"-error/rejected"] += 1
                        fn_tmp.write("command not found\n")
                    num_ineffective_tests += 1
                    continue  # Continue to the next solver.

            # Check if the stdout contains a valid solver query result,
            # i.e., contains lines with 'sat', 'unsat' or 'unknown'.
            elif (
                not re.search("^unsat$", stdout, flags=re.MULTILINE)
                and not re.search("^sat$", stdout, flags=re.MULTILINE)
                and not re.search("^unknown$", stdout, flags=re.MULTILINE)
            ):
                log_invalid_mutant(fn, solver_cli)
                num_ineffective_tests += 1
                if args.solver_summary_stats:
                    solver_stats[solver_cli+"-error/rejected"] += 1
                    fn_tmp.write("rejected\n")
                    continue  # Continue to the next solver.

            else:

                # Grep for '^sat$', '^unsat$', and '^unknown$' to produce
                # the output (including '^unknown$' to also deal with
                # incremental benchmarks) for comparing with the oracle
                # (yinyang) or with other non-erroneous solver runs
                # (opfuzz) for soundness bugs.
                result = grep_result(stdout)
                
                if args.solver_summary_stats:
                    if result != SolverQueryResult.UNKNOWN:
                        num_decided_formulas += 1


                if oracle.equals(SolverQueryResult.UNKNOWN) and result != SolverQueryResult.UNKNOWN:

                    # For differential testing (opfuzz), the first solver
                    # is set as the reference, its result to be the oracle.
                    oracle = result
                    reference = (solver_cli, fn, stdout, stderr)

                # Comparing with the oracle (yinyang) or with other
                # non-erroneous solver runs (opfuzz) for soundness bugs.
                if not oracle.equals(result):

                    # Produce a bug report for soundness bugs
                    # containing a diff with the reference solver
                    # (opfuzz).
                    ref_cli = reference[0]
                    ref_stdout = reference[1]
                    ref_stderr = reference[2]
                    path = report_diff(
                        fn,
                        "incorrect",
                        ref_cli,
                        ref_stdout,
                        ref_stderr,
                        solver_cli,
                        stdout,
                        stderr,
                        args
                    )
                    log_soundness_trigger(fn)
                    num_bugs += 1
                    fn_tmp.write("unsoundness\n")
                    continue

            fn_tmp.write(stdout)

    if args.solver_summary_stats: 
        if num_decided_formulas <= 1:   
            solver_stats["all-unvalidated_results"] += 1
    return num_bugs, num_ineffective_tests
