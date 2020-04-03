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

class Comment(Spliter):
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

class String(Value):
    pass

class Variable(Value):
    pass

class Name(Value):
    def __init__(self, v):
        super().__init__(v)
        self._from = None
        self._name = None
        self._as = None

        name = v.split('.')
        if len(name) > 1:
            self._from = name[0]
            self._name = name[1]
        else:
            self._name = name[0]

    @property
    def from_name(self):
        return self._from
    
    @from_name.setter
    def from_name(self, name):
        self._from = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def as_name(self):
        return self._as
    
    @as_name.setter
    def as_name(self, name):
        self._as = name
    
    def repr(self):
        return f'FROM: {self.from_name} | NAME: {self.name} | AS: {self.as_name}'


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
    
    @property
    def opening(self):
        return self._lexer.sub_opening or not self.is_close

    def _push(self, token: Token):
        pass

    def push(self, token: Token):
        self._push(token)
        if isinstance(token, Paren) and not token.is_open and not self._lexer.sub_opening:
            self.is_close = True
            return
        
        self._lexer.push(token)
    
    def repr(self):
        return '(' +''.join([repr(t) for t in self.tokens]) + ')'


class Function(Sub):
    def __init__(self, v):
        super().__init__(v)
        self.arguments = []
    
    @property
    def name(self):
        return self.value
    
    def _push(self, token: Token):
        if not isinstance(token, Spliter):
            self.arguments.append(token)

    
    def repr(self):
        return repr(self.name)+ '(' +','.join([repr(t) for t in self.arguments]) + ')'


class Column(Name):
    pass

class Table(Name):
    pass

class SubColumn(Sub, Column):
    pass

class SubTable(Sub, Table):
    pass