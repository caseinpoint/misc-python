"""A very basic script for enciphering and deciphering text files using a stream method."""

import random


def generate_lookup() -> dict:
    """Create character lookup dictionary."""

    lookup = {0: '\t', '\t': 0, 1: '\n', '\n': 1}
    idx = 2

    ranges = [(32,879), (8192,11193), (11197,11217), (11244,11247),
              (119040,119272)]
    for start, stop in ranges:
        for i in range(start, stop + 1):
            c = chr(i)
            rc = repr(c)

            if len(rc) == 3:
                lookup[idx] = c
                lookup[c] = idx
                idx += 1

    return lookup


def replace_text(text: str, lookup: dict, decode: bool = False) -> str:
    """Translate text using lookup dict."""

    stop = len(lookup) // 2
    results = []

    for char in text:
        idx = lookup.get(char, None)

        if idx is None:
            results.append(char)

        else:
            offset = random.randrange(stop)
            if decode:
                offset *= -1

            idx = (idx + offset) % stop

            results.append(lookup[idx])

    return ''.join(results)


def main(flag: str, filename: str, seed: str) -> str:
    random.seed(seed)

    decode = True if flag == '-d' else False
    lookup = generate_lookup()

    with open(filename, 'r') as f:
        file_text = f.read()

    file_text = replace_text(file_text, lookup, decode)

    with open(filename, 'w') as f:
        f.write(file_text)


if __name__ == '__main__':
    from sys import argv

    main(*argv[1:])
