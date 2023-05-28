import os
import argparse
import subprocess

def check_executable(path):
    if not os.path.exists(path):
        cmd = "which "+ path.strip('"').split(" ")[0]
        out = subprocess.getoutput(cmd)
        if "" == out.strip():
            return False
    return True


def check_clis(args):
    for cil in args.CLIS:
        if not check_executable(cil):
            print("Error: cil", cil ,"is invalid", flush = True)
            exit(1)

def check_bugfolder(args): 
    if not os.path.exists(args.bugfolder):
        os.mkdir(args.bugfolder)


def check_logfolder(args): 
    if not os.path.exists(args.logfolder):
        os.mkdir(args.logfolder)

def check_tempfolder(args):
    if not os.path.exists(args.tempfolder):
        os.mkdir(args.tempfolder)

def do_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "CLIS",
        metavar="CLIS",
    )
    parser.add_argument("depth", type=int, help="depth bound")
    parser.add_argument("--to-csv-file", type=str, help="copy statistics to said csv file", default=None)
    parser.add_argument("--solver-summary-stats", type=str, help="gather summary stats on solvers")
    parser.add_argument("--interval_size_in_secs", type=float, help="interval in which to print out/write statistics", default=2)
    parser.add_argument("--generate-only", action='store_true', help="only generate, do not test", default=None)
    parser.add_argument("--oracle-debug", action='store_true', help="let the oracle print the stdout and stderr to the console")
    parser.add_argument("--keep-files", action='store_true', help="do not delete generated files")
    parser.add_argument("--bugfolder", type=str, default="./bugs", help="bug folder")
    parser.add_argument("--logfolder", type=str, default="./logs", help="log folder")
    parser.add_argument("--tempfolder", type=str, default="./temp", help="temp folder")
    parser.add_argument("-t", "--timeout", type=float, help="timeout in secs", default=64)
    parser.add_argument("-m", "--max-tests", type=int,
                        help="limit number of tests", default=-1)
    parser.add_argument("-n", "--num-workers", type=int,
                        help="number of workers", default=1)

    return parser.parse_args()


def do_checks(args):
    if not args.generate_only:
        check_clis(args)
        check_bugfolder(args)
    check_logfolder(args)
    check_tempfolder(args)
