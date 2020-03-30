import re
from .tokens import *
from .keywords import COMMON, COMPOSITE


def is_keyword(value):
    val = value.upper()
    t = (COMMON_KEYWORDS.get(val)
        or COMPOSITE_KEYWORDS.get(val, Name))
    return t(value)


SEPERATOR = r'[\r\n\s,\(\)]'


SQL_REGEX = [
    (r'[\s\r\n]+', Space),
    (r',', Comma),
    (r'[\(\)]', Paren),
    (r'[\w]+(?='+ SEPERATOR +')', is_keyword),
    (r'[\w\*\-\+\/_\.\>\<\=]+(?='+ SEPERATOR +')', Name),
]

FLAGS = re.IGNORECASE | re.UNICODE
REG = [(re.compile(rx, FLAGS).match, tt) for rx, tt in SQL_REGEX]


COMMON_KEYWORDS = dict.fromkeys(COMMON, Keyword)
COMPOSITE_KEYWORDS = dict.fromkeys(COMPOSITE.keys(), CompositeKeyword)