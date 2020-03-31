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

class Buffer(Token):
    def check(self, token):
        return False
    
    def is_end(self, token):
        return True
    
    def combine(self, tokens):
        raise NotImplemented('combine method must be implemented')

class Negtive(Buffer):
    def check(self, token):
        return isinstance(token, Value)
    
    def is_end(self, token):
        return True
    
    def combine(self, tokens):
        return Value(''.join([t.value for t in tokens]))

class Keyword(Token):
    @property
    def keyword(self):
        return self.value.upper()

class CompositeKeyword(Keyword, Buffer):
    def __init__(self, v):
        super().__init__(v)
        self.follow_words = COMPOSITE.get(self.keyword)
    
    def check(self, token):
        if isinstance(token, Keyword) and token.keyword in self.follow_words:
            return True
        
        return False
    
    def is_end(self, token):
        if isinstance(token, CompositeKeyword) and token.follow_words is None:
            return True
        return False
    
    def combine(self, tokens):
        return Keyword(' '.join([t.value for t in tokens]))


class Value(Token):
    def repr(self):
        return repr(type(self.value)) + repr(self.value)

class Name(Value):
    pass

class Operator(Token):
    pass

class Sub(Token):
    def __init__(self, v):
        super().__init__(v)

        from .lexer import Lexer
        self._lexer = Lexer()

        self.is_close = False
    
    @property
    def tokens(self):
        return self._lexer.tokens

    def _push(self, token: Token):
        pass

    def push(self, token: Token):
        self._push(token)
        self._lexer.push(token)

class Function(Sub):
    @property
    def name(self):
        return self.value
    
    def repr(self):
        return repr(self.name)+ '(' +','.join([repr(t) for t in self.tokens]) + ')'


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