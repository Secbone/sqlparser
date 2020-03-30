
from .keywords import COMPOSITE

T_SPACE = 1
T_COMMA = 2
T_PAREN = 3
T_KEYWORD = 4
T_FIELD = 5


class Token:
    def __init__(self, v):
        self.value = v
    
    def repr(self):
        return repr(self.value)
    
    def __repr__(self):
        return self.__class__.__name__+ ' ' +self.repr()

class Spliter(Token):
    pass
    
class Space(Spliter):
    pass

class Comma(Spliter):
    pass

class Paren(Spliter):
    @property
    def is_open(self):
        return self.value == '('

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


class Value(Token):
    pass

class Name(Value):
    pass

class Operator(Token):
    pass

class Sub(Token):
    tokens = []
    is_close = False

    def _push(self, token: Token):
        pass

    def push(self, token: Token):
        self._push(token)
        self.tokens.append(token)

class Function(Sub):
    arguments = []

    @property
    def name(self):
        return self.value
    
    def _push(self, token: Token):
        if not isinstance(token, Value):
            return
        
        self.arguments.append(token)
    
    def repr(self):
        return repr(self.name)+ '(' +','.join([repr(t) for t in self.arguments]) + ')'


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