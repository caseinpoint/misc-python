from unicodedata import name
from pprint import pprint

# ERRORS = {141, 157, 158, 159, 160, 4053, 4054}

def print_unicode(start, stop):
    for i in range(start, stop):
        # if i in ERRORS:
        #     continue

        c = chr(i)
        rc = repr(c)

        if len(rc) == 3 or len(rc) == 4:
            print(i, c, rc, name(c, ''), f'\t"a{c}b"')

        if i != start and i % 80 == 0:
            if input(f'{" " * len(str(i))}continue? [Y/n]: ') == 'n':
                break

    print('done')


def get_lookup():
    lookup = {0: '\t', 1: '\n'}
    # lookup = {0: '\t', '\t': 0, 1: '\n', '\n': 1}
    # idx = 2

    ranges = [(32,879), (8192,11193), (11197,11217), (11244,11247),
              (119040,119272)]
    for start, stop in ranges:
        for i in range(start, stop + 1):
            c = chr(i)
            rc = repr(c)

            if len(rc) == 3:
                lookup[i] = (c, name(c, None))
                # lookup[idx] = c
                # lookup[c] = idx
                # idx += 1

    return lookup
