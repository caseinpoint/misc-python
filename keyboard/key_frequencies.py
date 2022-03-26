# from annotations import timed
from glob import iglob
from pprint import PrettyPrinter
from re import compile, IGNORECASE
from string import printable

EXTENSIONS = {'py', 'js', 'json', 'jsx', 'html', 'css'}
SKIP_PATTERNS = compile(r'migrations|bootstrap|jquery|package-lock|node_modules', IGNORECASE)

SHIFT_KEYS = {'~': '`', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
			  '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\', ':': ';', '"': "'", '<': ',', '>': '.', '?': '/'}
ALL_KEYS = set(printable)
ALL_KEYS -= {'\r', '\x0b', '\x0c'}
KEY_NAMES = {' ': 'SPACE', '\t': 'TAB', "'": 'APOSTRPHE', '\n': 'ENTER', ',': 'COMMA'}

PP = PrettyPrinter(indent=2, sort_dicts=False)


def find_files(path):
	for filename in iglob(pathname=f'{path}/**', recursive=True):
		split_dot = filename.split('.')
		if split_dot[-1] in EXTENSIONS and SKIP_PATTERNS.search(filename) is None:
			yield filename


# @timed
def process_file(filename, frequencies, totals):
	# print(f'\n{filename}')

	with open(filename) as f:
		file_txt = f.read()

	if len(file_txt) == 0:
		return False

	for i in range(len(file_txt) - 1):
		char = file_txt[i]
		if char not in ALL_KEYS:
			continue

		shifted = False
		if char in SHIFT_KEYS:
			char = SHIFT_KEYS[char]
			shifted = True
		elif char.isupper():
			char = char.lower()
			shifted = True

		j = i + 1
		while file_txt[j] not in ALL_KEYS:
			j += 1
		next_char = file_txt[j]
		if next_char in SHIFT_KEYS:
			next_char = SHIFT_KEYS[next_char]
		elif next_char.isupper():
			next_char = next_char.lower()

		if char in KEY_NAMES:
			char = KEY_NAMES[char]
		if next_char in KEY_NAMES:
			next_char = KEY_NAMES[next_char]

		if char not in frequencies:
			frequencies[char] = {'keys': {}, 'totals': {'press_count': 0, 'shift_count': 0}}

		totals['press_count'] += 1
		frequencies[char]['totals']['press_count'] += 1
		if shifted:
			totals['shift_count'] += 1
			frequencies[char]['totals']['shift_count'] += 1
		frequencies[char]['keys'][next_char] = frequencies[char]['keys'].get(next_char, 0) + 1

	last_char = file_txt[-1]
	if last_char in ALL_KEYS:
		last_shift = False
		if last_char in SHIFT_KEYS:
			last_char = SHIFT_KEYS[last_char]
			last_shift = True
		elif last_char.isupper():
			last_char = last_char.lower()
			last_shift = True

		if last_char in KEY_NAMES:
			last_char = KEY_NAMES[last_char]

		if last_char not in frequencies:
			frequencies[last_char] = {'keys': {}, 'totals': {'press_count': 0, 'shift_count': 0}}

		frequencies[last_char]['totals']['press_count'] += 1
		if last_shift:
			totals['shift_count'] += 1
			frequencies[last_char]['totals']['shift_count'] += 1

	return True


# @timed
def print_csv(frequencies):
	keys_sorted = sorted(frequencies.keys(),
						 key=lambda k: frequencies[k]['totals']['press_count'],
						 reverse=True)
	for key in keys_sorted:
		next_sorted = sorted(frequencies[key]['keys'].items(),
							 key=lambda i: i[1],
							 reverse=True)

		print(f'key:,{key}', end=',')
		print(f'count:,{frequencies[key]["totals"]["press_count"]}', end=',')
		print(f'shifted:,{frequencies[key]["totals"]["shift_percent"]}%')
		# print('next:', end=',')
		for next in next_sorted:
			print(next[1], end=',')
		print()
		for next in next_sorted:
			print(next[0], end=',')
		print('\n')


def print_top(frequencies, num):
	print(f'Keys by frequency (desc) and top {num} subsequent keys:')
	keys_sorted = sorted(frequencies.keys(),
						 key=lambda k: frequencies[k]['totals']['press_count'],
						 reverse=True)
	for key in keys_sorted:
		next_sorted = sorted(frequencies[key]['keys'].items(),
							 key=lambda i: i[1],
							 reverse=True)
		print(f'{" "*(10-len(key))}{key}', end=' ')
		for i in range(num):
			next = next_sorted[i]
			percent = f'{int(next[1] / frequencies[key]["totals"]["press_count"] * 100)}%'
			print(f'{next[0]}:{percent}', end=', ')
		print()


# @timed
def main():
	print('processing...')

	paths = ['/home/drue/Projects', '/home/drue/Hackbright/hb-dev/src/tools', '/home/drue/Hackbright/hb-dev/src/demos']
	count_files = 0

	frequencies = {}
	totals = {'press_count': 0, 'shift_count': 0}

	for path in paths:
		for filename in find_files(path):
			processed = process_file(filename, frequencies, totals)
			if processed:
				count_files += 1
	totals['count_files'] = count_files
	# totals['avg_presses'] = totals['press_count'] / count_files
	# totals['avg_shifts'] = totals['shift_count'] / count_files

	for key, counts in frequencies.items():
		counts['totals']['shift_percent'] = int(counts['totals']['shift_count'] / counts['totals']['press_count'] * 100)
	totals['shift_percent'] = int(totals['shift_count'] / totals['press_count'] * 100)

	# print_csv(frequencies)
	print_top(frequencies, 5)
	PP.pprint(totals)


if __name__ == '__main__':
	main()
