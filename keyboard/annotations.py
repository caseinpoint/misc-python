"""Annotations example from Henry Chen's guest lecture."""

from datetime import datetime


def timed(func):
    def new_func(*args):
        start = datetime.now()

        result = func(*args)

        time = datetime.now() - start
        print(f'function call took {time}')

        return result

    return new_func
