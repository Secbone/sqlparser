import re
from .tokens import *
from .keywords import COMMON, COMPOSITE, OPERATOR


def is_keyword(value):
    val = value.upper()
    t = (COMMON_KEYWORDS.get(val)
        or COMPOSITE_KEYWORDS.get(val)
        or OPERATOR_KEYWORDS.get(val))
    if t is None:
        t = Name
    return t(value)


SEPERATOR = r'[\r\n\s,\(\)]'


SQL_REGEX = [
    (r'(--|# ).*?(\r\n|\r|\n|$)', Comment),
    (r'/\*[\s\S]*?\*/', Comment),
    (r'[\s\r\n]+', Space),
    (r',', Comma),
    (r'[\(\)]', Paren),
    (r'[\+\-\*\/><=]+', Operator),
    (r'\d*(\.\d+)?E-?\d+', Value),
    (r'\d+', Value),
    (r"'(''|\\\\|\\'|[^'])*'", String),
    (r'"(""|\\\\|\\"|[^"])*"', String),
    (r':P_\w+', Variable),
    (r'[\w]+(?=\s)', is_keyword),
    (r'[\w\.]+', Name),
]

FLAGS = re.IGNORECASE | re.UNICODE
REG = [(re.compile(rx, FLAGS).match, tt) for rx, tt in SQL_REGEX]


COMMON_KEYWORDS = dict.fromkeys(COMMON.keys(), Keyword)
COMPOSITE_KEYWORDS = dict.fromkeys(COMPOSITE.keys(), CompositeKeyword)
OPERATOR_KEYWORDS = dict.fromkeys(OPERATOR.keys(), Operator)