from random import choice
from string import ascii_letters, digits
from sys import argv

num_digits = int(argv[1])

rand_str = ''.join([choice(ascii_letters + digits) for _ in range(num_digits)])
print(rand_str)
