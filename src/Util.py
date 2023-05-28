import os
import random
import subprocess


def pretty_print(state):
    s = state.atom_seq.replace("''", " ").replace("'", "")
    return s.replace("( ", "(").replace(" )", ")")


def dump_formula(s,formula, args):
    fn = args.tempfolder+"/formula"+s+".smt2"
   #  #Hack
    # logics = [
        # "(set-logic AUFLIA)",                                                                          
        # "(set-logic AUFLIRA)",                                                                         
        # "(set-logic AUFNIRA",                                                                         
        # "(set-logic LIA)",
        # "(set-logic LRA)",
        # "(set-logic QF_ABV)",
        # "(set-logic QF_AUFBV)",
        # "(set-logic QF_AUFLIA)",
        # "(set-logic QF_AX)",
        # "(set-logic QF_BV)",                                                                          
        # "(set-logic QF_IDL)",                                                                          
        # "(set-logic QF_LIA)",                                                                          
        # "(set-logic QF_LRA)",                                                                          
        # "(set-logic QF_NIA)",                                                                          
        # "(set-logic QF_NRA)",                                                                          
        # "(set-logic QF_RDL)",                                                                          
        # "(set-logic QF_UF)",                                                                           
        # "(set-logic QF_UFBV)",                                                                       
        # "(set-logic QF_UFIDL)",                                                                        
        # "(set-logic QF_UFLIA)",                                                                       
        # "(set-logic QF_UFLRA)",                                                                        
        # "(set-logic QF_UFNRA)",                                                                        
        # "(set-logic UFLRA)",                                                                           
        # "(set-logic UFNIA)"  
    # ] 

    # preamble = random.choice(logics) 
    with open(fn, "w") as f:
        f.write(formula)
    return fn


def debug(state, parser, label=None):
    human_readable_stack = [parser.ruleNames[s.ruleIndex]+":"+str(s.ruleIndex) for s in state.stack] 
    if not label:
        print("[State]", "atn_state_id="+str(state.atn_state), "depth="+str(state.depth()),
               "stack="+str(human_readable_stack), "atom_seq="+str(state.atom_seq),
               flush = True)
    else:
        print(label+" [State]", "atn_state_id="+str(state.atn_state), "depth="+str(state.depth()),
               "stack="+str(human_readable_stack), "atom_seq="+str(state.atom_seq),
               flush = True)


