import random
from secrets import randbits
random.seed(randbits(256))


def main(lists, num, low, high, add, repeat, unsort):
	"""Print list(s) of num random numbers from low to high."""

	ints = [i for i in range(low, high + 1)]

	for _ in range(lists):
		if not repeat:
			picks = random.sample(population=ints, k=num)
		else:
			picks = random.choices(population=ints, k=num)

		if not unsort:
			picks.sort()

		if add > 1:
			picks.append([random.randint(1, add)])

		print(picks)


if __name__ == '__main__':
	from argparse import ArgumentParser
	parser = ArgumentParser(description='generate lists of random numbers')

	parser.add_argument('-l', '--lists', help='number of lists, default=1', type=int, default=1)
	parser.add_argument('-n', '--num', help='size of list, default=5', type=int, default=5)
	parser.add_argument('-L', '--low', help='min number in list, default=1', type=int, default=1)
	parser.add_argument('-H', '--high', help='max number in list, default=32', type=int, default=32)
	parser.add_argument('-a', '--add', help='additional random number from 1 to a, default=none', type=int, default=0)
	parser.add_argument('-r', '--repeat', help='allow repeats, default=false', action='store_true')
	parser.add_argument('-u', '--unsort', help='unsorted list, default=false', action='store_true')

	args = parser.parse_args()
	main(**vars(args))
