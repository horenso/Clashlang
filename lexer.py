from enum import Enum, auto, unique
from re import match
from typing import Mapping
from sys import stderr
from copy import deepcopy
from textwrap import shorten
from typing import Type
from attr import define, field


@define
class Position:
    col = field(default=1)
    row = field(default=1)


@unique
class TokenType(Enum):
    WHITESPACE = "[\s\n\t\r]"
    SEMICOLON = ";"

    IF = "if"
    ELSE = "else"
    LET = "let"
    FN = "fn"

    LITERAL_BOOL = "true|false"
    LITERAL_NUM = "\d+(\.\d+)?"
    LITERAL_STR = '"(.*)"'

    OP_PLUS = "\+"
    OP_MINUS = "\-"
    OP_MULT = "\*"
    OP_POWER = "\*\*"
    OP_DIV = "/"
    PAR_L = "\("
    PAR_R = "\)"
    CURL_L = "{"
    CURL_R = "}"
    BRK_L = "["
    BRK_R = "]"
    EQUALS = "="
    IDENTIFIER = "[a-zA-Z]([a-zA-Z0-9])*"


@define(kw_only=True)
class Token:
    token_type: TokenType = field()
    value: any = field()
    position: Position = field()


@define()
class Lexer:
    string: str = field()
    current_position: Position = field(factory=Position)

    def _match_next_token(self):
        for possible_token in TokenType:
            pattern = possible_token.value
            token_type = possible_token
            potential_match = match(pattern, self.string)
            if potential_match:
                s = potential_match.group(0)
                self.string = self.string[len(s) :]
                t = Token(
                    token_type=token_type,
                    value=s,
                    position=deepcopy(self.current_position),
                )
                self.current_position.col += len(s)
                return t
        return None

    def lex(self):
        while len(self.string) > 0:
            token = self._match_next_token()
            if token is None:
                print(
                    f"Invalid token[{self.current_position}]: {self.string}",
                    file=stderr,
                )
                return
            if token.token_type == TokenType.WHITESPACE:
                newline_pos = token.value.rfind("\n")
                if newline_pos != -1:
                    self.current_position.col = newline_pos + 1
                    self.current_position.row += token.value.count("\n")
                continue
            yield token
