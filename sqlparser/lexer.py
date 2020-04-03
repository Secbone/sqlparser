from itertools import islice
from collections import deque

from .regex import REG
from .tokens import *
from .keywords import *



NAME_TOKEN_TYPE = {
    T_COLUMN: Column,
    T_TABLE: Table,
}



def consume(iterator, n):
    deque(islice(iterator, n), maxlen = 0)


class Lexer:
    def __init__(self):
        self.tokens = []
        self._buffer = []
        self._last_kw_idx = -1
        self._last_word_idx = -1

    @property
    def last_keyword(self):
        return self._safe_idx(self._last_kw_idx)
    
    @property
    def last_word(self):
        return self._safe_idx(self._last_word_idx)
    
    @property
    def last_token(self):
        if self.size > 0:
            return self.tokens[-1]
        
        return None
    
    @property
    def sub_opening(self):
        return isinstance(self.last_token, Sub) and self.last_token.opening
    
    @property
    def follow_type(self):
        if self.last_keyword is None:
            return T_COLUMN
        
        return COMMON.get(self.last_keyword.keyword, T_COLUMN)
    
    @property
    def size(self):
        return len(self.tokens)
    
    def __len__(self):
        return self.size
    
    def _safe_idx(self, idx: int):
        if idx < 0 or idx >= self.size:
            return None
        
        return self.tokens[idx]
    
    def _push(self, token: Token):
        idx = self.size

        self.tokens.append(token)

        # update memery idx
        if not isinstance(token, Space):
            self._last_word_idx = idx
        
        if isinstance(token, Keyword):
            self._last_kw_idx = idx


    def push(self, token: Token):
        if len(self._buffer) > 0 or isinstance(token, Buffer):
            self._push_buffer(token)
        else:
            self._dispatch_token(token)
        
    
    def _dispatch_token(self, token: Token):
        if self.sub_opening:
            self._push_sub(token)
        elif isinstance(token, Space):
            self._push_space(token)
        elif isinstance(token, Name):
            self._push_name(token)
        elif isinstance(token, Keyword):
            self._push_keyword(token)
        elif isinstance(token, Paren):
            self._push_paren(token)
        elif isinstance(token, Operator):
            self._push_operator(token)
        else:
            self._push(token)


    def _push_sub(self, token: Sub):
        self.last_token.push(token)
    

    def _push_space(self, token: Space):
        self._push(token)
    

    def _push_name(self, token: Name):
        if isinstance(self.last_word, Name):
            self.last_word.as_name = token.value
            return
        
        t = NAME_TOKEN_TYPE[self.follow_type]    
        self._push(t(token.value))


    def _push_operator(self, token: Operator):
        if not isinstance(self.last_word, Value):
            if token.value == '-':
                self._push_buffer(Negtive('-'))
                return
            
            token = Name(token.value)
        
        # TODO push operator
        self._push(token)

    
    def _push_paren(self, token: Paren):
        if token.is_open:
            if isinstance(self.last_token, Name):
                # is function
                self.tokens[-1] = Function(self.last_token.value)
            else:
                # sub sentence
                # TODO sub sentence recursive push
                self._push(Sub(''))
        else:
            # close paren
            self._push(token)
    
    def _push_buffer(self, token):
        if isinstance(token, Space):
            return
        
        if len(self._buffer) < 1:
            self._buffer.append(token)
            return
        
        l_token = self._buffer[-1]
        if not l_token.check(token):
            # error check
            # TODO convert token type when error
            self._dispatch_token(l_token.combine(self._buffer))
            self._buffer.clear()
            
            if isinstance(token, Buffer):
                self._buffer.append(token)
            else:
                self._dispatch_token(token)
            return
        
        # token matched
        self._buffer.append(token)

        if l_token.is_end(token):
            self._dispatch_token(l_token.combine(self._buffer))
            self._buffer.clear()
    

    def _push_keyword(self, token: Keyword):
        if token.keyword == 'AS':
            # ignore `as` keyword
            return
        
        self._push(token)


    
    def _push_composite(self, token: Keyword):
        if not isinstance(self.last_word, CompositeKeyword):
            # first composite keyword
            token.start_at = self.size

        elif token.keyword not in self.last_word.follow_words:
            # composite keyword not match
            # TODO covert last_word to keyword or raise error
            token.start_at = self.size
        
        elif token.follow_words is not None:
            # composite keyword not end
            token.start_at = self.last_word.start_at
        
        else:
            # end of keyword
            start = self.last_word.start_at
            key = [t.value for t in self.tokens[start:] if isinstance(t, CompositeKeyword)] + [token.value]
            self.tokens = self.tokens[:start]
            token = Keyword(' '.join(key))
        
        return self._push(token)


    def tokenize(self, sql: str):
        iterable = enumerate(sql)

        for pos, char in iterable:
            for match, action in REG:
                m = match(sql, pos)
                if not m:
                    continue
                else:
                    self.push(action(m.group()))
                
                consume(iterable, m.end() - pos - 1)
                break
            else:
                raise Exception('{0} at pos {1}'.format(sql[pos-10: pos], pos))
        
        return self.tokens


def parse(sql):
    return Lexer().tokenize(sql)


def parse_clear(sql):
    for item in Lexer().tokenize(sql):
        if isinstance(item, (Space, Comment)):
            continue
        
        yield item