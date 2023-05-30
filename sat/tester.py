import sys

bugfile = sys.argv[1]

def test_input():
    file = sys.argv[3]
    with open(file, mode='r') as f:
        text = f.read()
    l = text.splitlines()
    l1 = l[0].split()
    n, c = int(l1[2]), int(l1[3])
    conds = [] 
    for i in range(c):
        line = l[i + 1].split()
        cnt = len(line)
        conds.append([int(x) for x in line[: len(line) - 1]])
    return n, conds
    
def test_output():
    file = sys.argv[2]
    with open(file, mode='r') as f:
        text = f.read()
    l = text.splitlines()
    l1 = l[0].split()
    if l1[1] == "UNSATISFIABLE" or l1[1] == "UNKNOWN":
        return None
    l2 = l[1].split()
    return [int(x) for x in l2[1: len(l2) - 1]]

vals = test_output()

if vals is not None:
    n, conds = test_input()
    
    assert len(vals) == n
    for cond in conds:
        truth = False
        for var in cond:
            if var in vals:
                truth = True
        if not truth:
            with open(bugfile, "a") as f:
                f.write("p cnf {} {}\n".format(n, len(conds)))
                f.write("\n".join([" ".join([str(each) for each in cond] + ['0']) for cond in conds]))
                f.write("\n-------------------------------\n")
            print("Bug found")
