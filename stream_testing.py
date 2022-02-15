"""something weird is happening with stream_cipher.py, trying to find out what"""

# import random

# SEED = 'test'
# NUM_TESTS = 100000
# RANGE = 100

# random.seed(SEED)

# rand_nums1 = []
# for _ in range(NUM_TESTS):
# 	rand_nums1.append(random.randrange(RANGE))

# random.seed(SEED)

# rand_nums2 = []
# for _ in range(NUM_TESTS):
# 	rand_nums2.append(random.randrange(RANGE))

# count = 0
# for i in range(NUM_TESTS):
# 	if rand_nums1[i] != rand_nums2[i]:
# 		count += 1
# 		print(f'rand_nums1[{i}]: {rand_nums1[i]}, rand_nums2[{i}]: {rand_nums2[i]}')

# print(f'\ntotal mismatches: {count}')

from string import ascii_lowercase

out_file = open('test.txt', 'w')

for i in range(1000):
    out_file.write(f'{ascii_lowercase}\n')

out_file.close()
