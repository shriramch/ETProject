# MIT License
#
# Copyright (c) [2020 - 2021] The yinyang authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import datetime

from logging.handlers import RotatingFileHandler

RED = "\033[91m"
BOLD = "\033[1m"
WARNING = "\033[91m"
ENDC = "\033[0m"


def init_logging(strategy, quiet_mode, name, args):
    fn = (
        datetime.datetime.now().strftime(strategy + "-%Y-%m-%d-%M:%S-%p")
        + ".log"
    )
    log_fn = args.logfolder + "/" + fn
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(filename=log_fn,
                                maxBytes=1024 * 1024, backupCount=5)
        ],
        format="%(asctime)s %(message)s",
        datefmt="[%Y/%m/%d %I:%M:%S %p]",
        level=logging.DEBUG,
    )

    if not quiet_mode:
        console = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(message)s", datefmt="[%Y/%m/%d %I:%M:%S %p]"
        )
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)


def log_strategy_solvers(strategy, targets):
    num_targets = len(targets)
    logging.info(
        "Strategy: "
        + strategy
        + ", "
        + str(num_targets)
        + " testing targets "
    )


def log_status(line):
    logging.info(line)


def log_generation_attempt(args):
    logging.debug(
        "Attempting to generate " + str(args.iterations) + " mutants"
    )


def log_finished_generations(successful, unsuccessful):
    logging.debug(
        "Finished generations: "
        + str(successful)
        + " successful, "
        + str(unsuccessful)
        + " unsuccessful"
    )


def log_crash_trigger(path):
    logging.debug("Crash! Stop testing on this seed.")
    logging.info(BOLD + WARNING + "Detected crash bug: " + path + ENDC)


def log_ignore_list_mutant(solver_cli, path):
    logging.debug("Invalid mutant:ignore_list." + " fn=" + path + " sol=" + str(solver_cli))


def log_duplicate_trigger():
    logging.debug("Duplicate. Stop testing on this seed.")


def log_segfault_trigger(args, path):
    logging.info(BOLD + WARNING + "Detected segfault: " + path + ENDC)


def log_solver_timeout(args, solver_cli, path):
    logging.debug(
        " Solver timeout occurred. sol="
        + str(solver_cli)
        + path
    )


def log_soundness_trigger(path):
    logging.debug(
        " Soundness bug! Stop testing on this seed."
    )
    logging.info(BOLD + WARNING + "Detected soundness bug! " + path + ENDC)


def log_invalid_mutant(path, solver_cli):
    logging.debug(
        " Invalid mutant:no '^sat$' or '^unsat$' in output."
          + " fn=" + path + " sol=" + str(solver_cli)
    )


def log_skip_seed_mutator(args, i):
    logging.debug(
        str(i)
        + "/"
        + str(args.iterations)
        + " Mutator indicated to skip the seed."
    )


def log_skip_seed_test(args, i):
    logging.debug(
        str(i)
        + "/"
        + str(args.iterations)
        + " Fuzzer::test indicated to skip the seed."
    )
