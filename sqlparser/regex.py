import re
from .tokens import *


def is_keyword(value):
    t = KEYWORDS.get(value.upper(), Field)
    return t(value)


SEPERATOR = r'[\r\n\s,\(\)]'


SQL_REGEX = [
    (r'[\s\r\n]+', Space),
    (r',', Comma),
    (r'[\(\)]', Paren),
    (r'[\w]+(?='+ SEPERATOR +')', is_keyword),
    (r'[\w\*\-\+\/_\.\>\<\=]+(?='+ SEPERATOR +')', Field),
]

FLAGS = re.IGNORECASE | re.UNICODE
REG = [(re.compile(rx, FLAGS).match, tt) for rx, tt in SQL_REGEX]


COMMON_KEYWORDS = [
    'SELECT',
    'UPDATE',
    'INSERT',
    'DELETE',
    'FROM',
    'WHERE',
    'ON',
    'IN',
    'AS',
    'DISTINCT',
]


KEYWORDS = dict.fromkeys(COMMON_KEYWORDS, Keyword)