from glob import iglob
from pprint import PrettyPrinter
from re import compile, IGNORECASE
from string import printable

EXTENSIONS = {'py', 'js', 'json', 'jsx', 'html', 'css'}
SKIP_PATTERNS = compile('migrations|bootstrap|jquery', IGNORECASE)

SHIFT_KEYS = {'~': '`', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
			  '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\', ':': ';', '"': "'", '<': ',', '>': '.', '?': '/'}
ALL_KEYS = set(printable)
ALL_KEYS -= {'\r', '\x0b', '\x0c'}


def find_files(path):
	for filename in iglob(pathname=f'{path}/**', recursive=True):
		split_dot = filename.split('.')
		if split_dot[-1] in EXTENSIONS and SKIP_PATTERNS.search(filename) is None:
			yield filename

def process_file(filename, frequencies):
	processed = False

	with open(filename) as f:
		file_txt = f.read()

	if len(file_txt) == 0:
		return processed

	frequencies['totals']['press_count'] += len(file_txt)

	for i in range(len(file_txt) - 1):
		char = file_txt[i]
		shifted = False
		if char not in ALL_KEYS:
			continue
		elif char in SHIFT_KEYS:
			char = SHIFT_KEYS[char]
			shifted = True
		elif char.isupper():
			char = char.lower()
			shifted = True

		next_char = file_txt[i + 1]
		if next_char in SHIFT_KEYS:
			next_char = SHIFT_KEYS[next_char]
		elif next_char.isupper():
			next_char = next_char.lower()

		if char not in frequencies:
			frequencies[char] = {'press_count': 0, 'shift_count': 0}

		frequencies[char]['press_count'] += 1
		if shifted:
			frequencies['totals']['shift_count'] += 1
			frequencies[char]['shift_count'] += 1
		frequencies[char][next_char] = frequencies[char].get(next_char, 0) + 1

	last_char = file_txt[-1]
	if last_char in ALL_KEYS:
		last_shift = False
		if last_char in SHIFT_KEYS:
			last_char = SHIFT_KEYS[last_char]
			last_shift = True
		elif last_char.isupper():
			last_char = last_char.lower()
			last_shift = True

		if last_char not in frequencies:
			frequencies[last_char] = {'press_count': 0, 'shift_count': 0}

		frequencies[last_char]['press_count'] += 1
		if last_shift:
			frequencies['totals']['shift_count'] += 1
			frequencies[last_char]['shift_count'] += 1

	processed = True
	return processed


def print_sorted(frequencies):
	pass


def main():
	print('processing...')

	paths = ['/home/drue/Projects', '/home/drue/Hackbright/hb-dev/src/tools', '/home/drue/Hackbright/hb-dev/src/demos']
	count_files = 0

	frequencies = {'totals': {'press_count': 0, 'shift_count': 0}}

	for path in paths:
		for filename in find_files(path):
			processed = process_file(filename, frequencies)
			if processed:
				count_files += 1

	for counts in frequencies.values():
		counts['shift_ratio'] = counts['shift_count'] / counts['press_count']

	print(f'Files processed: {count_files}')
	pp = PrettyPrinter(indent=2, sort_dicts=False)
	pp.pprint(frequencies)
