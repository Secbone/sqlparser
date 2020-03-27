import re
from .tokens import *


def is_keyword(value):
    if value in KEYWORDS:
        return Keyword(value)
    return Field(value)


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