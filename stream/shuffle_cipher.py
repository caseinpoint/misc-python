import random


def shuffle_text(text: str) -> str:
    """Return shuffled text.

    Given the same seed, this function will un-shuffle the text."""

    result = list(text)

    indices = list(range(len(result)))
    random.shuffle(indices)

    for i in range(0, len(indices) - 1, 2):
        a, b = indices[i], indices[i + 1]
        result[a], result[b] = result[b], result[a]

    return ''.join(result)


def main(filename: str, seed: str) -> None:
    random.seed(seed)

    with open(filename, 'r') as f:
        file_text = f.read()

    file_text = shuffle_text(file_text)

    with open(filename, 'w') as f:
        f.write(file_text)


if __name__ == '__main__':
    from sys import argv

    main(*argv[1:])
