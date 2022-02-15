"""A very basic script for enciphering and deciphering text files using a stream method."""

import random
from string import printable
from sys import argv

_, flag, filename, state = argv
ENCODE = '-e'
DECODE = '-d'

random.seed(a=state)

actually_printable = printable[:-3]

lookup = {}
for idx, val in enumerate(actually_printable):
    lookup[idx] = val
    lookup[val] = idx

with open(file=filename, mode='r', errors='replace') as f:
    text = f.read()

results = []
for char in text:
    idx = lookup.get(char, None)

    if idx is None:
        results.append(char)

    else:

        offset = random.randrange(len(actually_printable))
        if flag == DECODE:
            offset *= -1

        idx = (idx + offset) % len(actually_printable)

        results.append(lookup[idx])

file_split = filename.split('.')

if ENCODE in file_split:
    file_split.remove(ENCODE)

elif DECODE in file_split:
    file_split.remove(DECODE)

file_split.insert(-1, flag)

new_name = '.'.join(file_split)

with open(file=new_name, mode='w', encoding='utf-16', errors='replace') as f:
    f.write(''.join(results))
