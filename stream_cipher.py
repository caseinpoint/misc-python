"""A very basic script for enciphering and deciphering text files using a stream method."""

from string import printable
import random
from sys import argv
from datetime import datetime

_, flag, filename, state = argv

file_split = filename.split('.')
if len(file_split) > 2:
	file_split[:-1] = ['.'.join(file_split[:-1])]

random.seed(a=state)

# 'a': 10
ltr_idx = {}
# 10: 'a'
idx_ltr = {}
for i, l in enumerate(printable[:-2]):
	ltr_idx[l] = i
	idx_ltr[i] = l

infile = open(filename, 'r')

new_chars = []
for line in infile:
	for char in line:
		idx = ltr_idx.get(char, 71)
		offset = random.randrange(len(ltr_idx))

		if flag == '-e':
			idx += offset
		elif flag == '-d':
			idx -= offset

		idx %= len(ltr_idx)

		new_chars.append(idx_ltr[idx])

infile.close()

new_file = ''.join(reversed(file_split[0]))
# test for pallindrome
if new_file == file_split[0]:
	new_file += flag
new_file += '.' + file_split[1]

outfile = open(new_file, 'w')

# time_start = datetime.now()
# for char in new_chars:
#	outfile.write(char)
# time_end = datetime.now()

# more efficient than for loop above
# time_start = datetime.now()
outfile.write(''.join(new_chars))
# time_end = datetime.now()

outfile.close()

# print(f'finished writing in {time_end - time_start}')

