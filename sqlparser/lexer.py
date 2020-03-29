from itertools import islice
from collections import deque

from .regex import REG

def consume(iterator, n):
    deque(islice(iterator, n), maxlen = 0)

def tokenize(sql):
    iterable = enumerate(sql)

    for pos, char in iterable:
        for match, action in REG:
            m = match(sql, pos)
            if not m:
                continue
            else:
                yield action(m.group())
            
            consume(iterable, m.end() - pos - 1)
            break
        else:
            yield char


def parse(sql):
    return [t for t in tokenize(sql)]