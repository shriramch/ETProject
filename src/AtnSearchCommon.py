import copy
import zlib

from antlr4.atn.ATNState import (
        RuleStartState, RuleStopState, BasicBlockStartState, BasicState
)
from antlr4.atn.Transition import AtomTransition, RuleTransition, SetTransition

BOUND_ASSERTION_FAILMSG = "Fatal failure: unroll inadmissible depth (too high)."


class State(object):
    def __init__(self, atn_state, atom_seq):
        self.atn_state = atn_state
        self.atom_seq = atom_seq
        self.stack = []

    def __hash__(self):
        return hash(self.atn_state) ^ zlib.adler32(bytes(self.atom_seq, encoding='utf8'))\
                ^ hash(frozenset(self.stack))

    def depth(self):
        return len(self.stack)


def handle_atom_transition(parser, transition, atn_state, atom_seqs):
    idx = atn_state.transitions[0].label[0]
    if len(atom_seqs) == 0:
        atom_seqs.append(parser.literalNames[idx])
    else:
        new_atom_seqs = []
        for a in atom_seqs:
            new_atom_seqs.append(a + parser.literalNames[idx])
        atom_seqs = new_atom_seqs
    return atom_seqs


def handle_set_transition(parser, transition, atom_seqs):
    new_atom_seqs = []
    for labl in transition.label:
        labl_s = parser.literalNames[labl]
        for a in atom_seqs:
            new_atom_seqs.append(a + labl_s)
    return new_atom_seqs


def check_path_for_rule_transition(s1):
    """
    Checks transition sequence s1 -t1-> s2 -t2-> ... -tn-> sn
    for nonterminals on the path.

    s1: first state

    @returns
        True:  if there are nonterminals on the path.
        False: otherwise
    """
    atn_state = s1
    while not isinstance(atn_state, RuleStopState):
        assert(len(atn_state.transitions) == 1)
        t = atn_state.transitions[0]
        if isinstance(t, RuleTransition):
            return True
        atn_state = t.target
    return False


def production_is_non_const(start_state):
    """
    start_state: start state for production rule p

    A production rule p -> alpha_1 | ... | alpha_n is non-constant iff every alpha_i
    contains a nonterminal.

    returns:    True iff production p is non-constant
                False otherwise
    """
    assert(isinstance(start_state, RuleStartState) and len(start_state.transitions) == 1)
    atn_state = start_state.transitions[0].target
    if isinstance(atn_state, BasicState):
        return check_path_for_rule_transition(atn_state)
    elif isinstance(atn_state, BasicBlockStartState):
        for t in atn_state.transitions:
            path_start_state = t.target
            if not check_path_for_rule_transition(path_start_state):
                return False
        return True
    assert False


def precompute_non_const_productions(parser):
    m = dict()
    atn = parser.atn
    for i in range(0, len(parser.ruleNames) - 1):
        start_state = atn.ruleToStartState[i]
        m[i] = production_is_non_const(start_state)
    return m


# def prune(state, max_depth, non_const_prod_map):
    # """
    # Prune if |state.stack| = max_depth and state[-1] is start state of
    # non_const rule, i.e. the corresponding path is not realizable.
    # """
    # return len(state.stack) == max_depth and non_const_prod_map[state.stack[-1]]


def unroll(parser, state, max_depth):
    """
    Linearly walk through ATN. Continue as long as there are no decision
    points.
    """

    assert len(state.stack) <= max_depth, BOUND_ASSERTION_FAILMSG

    atn_state = copy.deepcopy(state.atn_state)
    stack = copy.deepcopy(state.stack)
    atom_seqs = [copy.deepcopy(state.atom_seq)]
    while len(atn_state.transitions) == 1:
        # print(atn_state, flush=True)
        transition = atn_state.transitions[0]

        if isinstance(transition, AtomTransition):
            # print("AtomTransition",  flush=True)
            # atom transitions, e.g., s1 -label-> s2
            idx = atn_state.transitions[0].label[0]
            if idx != -1:
                atom_seqs = handle_atom_transition(parser, transition, atn_state,
                                                   atom_seqs)

        if isinstance(transition, SetTransition):
            # print("SetTransition", flush=True)
            # set transitions, e.g., s1  -{label1,...,labeln}-> s2
            atom_seqs = handle_set_transition(parser, transition, atom_seqs)

        if isinstance(transition, RuleTransition):
            # add follow state to stack
            # print("RuleTransition " + parser.ruleNames[transition.ruleIndex], flush=True)
            stack.append(transition.followState)

        # Assign new atn_state after the transition
        atn_state = atn_state.transitions[0].target
        if isinstance(atn_state, RuleStopState):
            # print("StopStateTransition", flush=True)

            # When running into a rule stop state, return to the last automaton
            # from which the jump was initiated.
            if len(stack) != 0 and len(stack) <= max_depth:
                atn_state = stack[-1]
                stack.pop()

    unrolled_states = []
    for seq in atom_seqs:
        new_state = State(atn_state, seq)
        new_state.stack = stack
        if new_state != state:
            unrolled_states.append(new_state)
    return unrolled_states


def get_sucessors(parser, curr, max_depth):
    unrolled_states = unroll(parser, curr, max_depth)
    successors = []
    for ustate in unrolled_states:
        if len(ustate.atn_state.transitions) != 0:
            for t in ustate.atn_state.transitions:
                succ_state = State(t.target, ustate.atom_seq)
                succ_state.stack = ustate.stack
                successors.append(succ_state)
        else:
            successors.append(ustate)
    return successors



