
from .keywords import COMPOSITE

T_SPACE = 1
T_COMMA = 2
T_PAREN = 3
T_KEYWORD = 4
T_FIELD = 5


class Token:
    def __init__(self, v):
        self.value = v
    
    def __repr__(self):
        return self.__class__.__name__+ ' ' +repr(self.value)

class Spliter(Token):
    pass
    
class Space(Spliter):
    pass

class Comma(Spliter):
    pass

class Paren(Spliter):
    pass

class Keyword(Token):
    @property
    def keyword(self):
        return self.value.upper()

class CompositeKeyword(Keyword):
    start_at = 0
    follow_words = None
    
    def __init__(self, v):
        super().__init__(v)
        self.follow_words = COMPOSITE.get(self.keyword)
    

class Name(Token):
    pass

class Column(Name):
    pass

class Table(Name):
    pass

class Sub(Token):
    pass

class SubColumn(Sub, Column):
    pass

class SubTable(Sub, Table):
    pass