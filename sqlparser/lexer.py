from itertools import islice
from collections import deque

from .regex import REG
from .tokens import *

def consume(iterator, n):
    deque(islice(iterator, n), maxlen = 0)


class Lexer:
    tokens = []
    _last_kw_idx = 0
    _last_word_idx = 0

    @property
    def last_keyword(self):
        return self._safe_idx(self._last_kw_idx)
    
    @property
    def last_word(self):
        return self._safe_idx(self._last_word_idx)
    
    @property
    def last_token(self):
        size = len(self)
        if size > 0:
            return self.tokens[-1]
        
        return None
    
    def __len__(self):
        return len(self.tokens)
    
    def _safe_idx(self, idx: int):
        if idx >= len(self.tokens):
            return None
        
        return self.tokens[idx]
    
    def _push(self, token: Token):
        idx = len(self)

        self.tokens.append(token)

        # update memery idx
        if not isinstance(token, Space):
            self._last_word_idx = idx
        
        if isinstance(token, Keyword):
            self._last_kw_idx = idx


    def push(self, token: Token):
        if isinstance(token, CompositeKeyword):
            self._push_composite(token)
        else:
            self._push(token)
    

    def _push_composite(self, token: Keyword):
        if not isinstance(self.last_word, CompositeKeyword):
            # first composite keyword
            token.start_at = len(self)

        elif token.keyword not in self.last_word.follow_words:
            # composite keyword not match
            # TODO covert last_word to keyword or raise error
            token.start_at = len(self)
        
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
                raise Exception(char)
        
        return self.tokens


def parse(sql):
    return Lexer().tokenize(sql)