from sys import argv
from re import search

def file_to_str(filename):
    with open(filename) as file:
        lines = [line for line in file]
    return ''.join(lines)

target = file_to_str(argv[1])
regex = file_to_str(argv[2])

if search(regex, target) == None:
    print('False')
else:
    print('True')
