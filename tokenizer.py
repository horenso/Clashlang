from enum import Enum, auto, unique
from re import match
from typing import Mapping
from sys import stderr
from copy import deepcopy
from textwrap import shorten
from typing import Type


class Position:
    def __init__(self):
        self.col = 1
        self.row = 1

    def __repr__(self):
        return f'{self.row}:{self.col}'


@unique
class TokenType(Enum):
    WHITESPACE = 0
    VAR = auto()
    LITERAL_NUM = auto()
    LITERAL_STR = auto()
    OP_PLUS = auto()
    OP_MINUS = auto()
    OP_MULT = auto()
    OP_POWER = auto()
    OP_DIV = auto()
    PAR_L = auto()
    PAR_R = auto()
    ASSIGN = auto()
    IDENTIFIER = auto()


regex_map: Mapping[str, TokenType] = {
    '[\s\n\t\r]': TokenType.WHITESPACE,
    'var': TokenType.VAR,
    '\d+(\.\d+)?': TokenType.LITERAL_NUM,
    '"(.*)"': TokenType.LITERAL_STR,
    '\+': TokenType.OP_PLUS,
    '\-': TokenType.OP_MINUS,
    '\*': TokenType.OP_MULT,
    '\*\*': TokenType.OP_POWER,
    '/': TokenType.OP_DIV,
    '\(': TokenType.PAR_L,
    '\)': TokenType.PAR_R,
    '=': TokenType.ASSIGN,
    '[a-zA-Z]([a-zA-Z0-9])*': TokenType.IDENTIFIER,
}


class Token:
    def __init__(self, token_type: TokenType, value: str, position: Position):
        self.token_type = token_type
        self.value = value
        self.position = position

    def __repr__(self) -> str:
        return f"<{self.token_type.name} '{self.value}' [{self.position}]>"


class Tokenizer:
    def __init__(self, string: str):
        self.string = string
        self.current_position: Position = Position()

    def _match_next_token(self):
        for pattern, token_type in regex_map.items():
            potential_match = match(pattern, self.string)
            if potential_match:
                s = potential_match.group(0)
                self.string = self.string[len(s):]
                t = Token(token_type, s, deepcopy(self.current_position))
                self.current_position.col += len(s)
                return t
        return None

    def generator(self):
        while len(self.string) > 0:
            token = self._match_next_token()
            if token is None:
                print(
                    f'Invalid token[{self.current_position}]: {self.string}', file=stderr
                )
                return
            if token.token_type == TokenType.WHITESPACE:
                newline_pos = token.value.rfind('\n')
                if newline_pos != -1:
                    self.current_position.col = newline_pos + 1
                    self.current_position.row += token.value.count('\n')
                continue
            yield token
