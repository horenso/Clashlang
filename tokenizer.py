from enum import Enum
from re import match
from typing import Mapping
from sys import stderr
from textwrap import shorten
from typing import Type


class TokenType(Enum):
    WHITESPACE = 0
    NUMBER = 1
    OPERATOR = 2
    PARENTHESIS = 3
    IDENTIFIER = 4


regex_map: Mapping[str, TokenType] = {
    '[\s\n\t\r]': TokenType.WHITESPACE,
    '\d+(\.\d+)?': TokenType.NUMBER,
    '[\+\-\*/]': TokenType.OPERATOR,
    '[()\[\]]': TokenType.PARENTHESIS,
    '[a-zA-Z]([a-zA-Z]|\d)*': TokenType.IDENTIFIER
}


class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"<{self.token_type.name} '{self.value}'>"


class Tokenizer:
    def __init__(self, string: str):
        self.string = string

    def _match_next_token(self):
        for pattern, token_type in regex_map.items():
            potential_match = match(pattern, self.string)
            if potential_match:
                s = potential_match.group(0)
                self.string = self.string[len(s):]
                return Token(token_type, s)
        return None

    def parse(self):
        while len(self.string) > 0:
            token = self._match_next_token()
            if token == None:
                print(shorten(self.string, width=10,
                      placeholder='...'), file=stderr)
                print('^ Invalid token', file=stderr)
                return
            if token.token_type == TokenType.WHITESPACE:
                continue
            yield token
