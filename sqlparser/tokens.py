class Token:
    def __init__(self, m):
        self.value = m
    
    def __repr__(self):
        return self.__class__.__name__ + repr(self.value)

class Spliter(Token):
    pass
    
class Space(Spliter):
    pass

class Comma(Spliter):
    pass

class Paren(Spliter):
    pass

class Keyword(Token):
    pass

class Field(Token):
    pass