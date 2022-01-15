
from abc import abstractmethod
from tokenizer import Token, TokenType, Tokenizer
from typing import Iterator


class Node():
    def __init__(self, token: Token):
        self.token = token

    @abstractmethod
    def eval(self):
        pass


class Number(Node):
    def eval(self):
        return float(self.token.value)

    def __str__(self) -> str:
        self.token.value


class BinOperation(Node):
    def __init__(self, token: Token, left_operand: Node, right_operand: Node):
        super().__init__(token)
        self.left_operand = left_operand
        self.right_operand = right_operand

    def eval(self):
        token_type = self.token.token_type
        if token_type == TokenType.OP_PLUS:
            return self.left_operand.eval() + self.right_operand.eval()
        if token_type == TokenType.OP_MINUS:
            return self.left_operand.eval() - self.right_operand.eval()
        if token_type == TokenType.OP_MULT:
            return self.left_operand.eval() * self.right_operand.eval()
        if token_type == TokenType.OP_DIV:
            return self.left_operand.eval() / self.right_operand.eval()

    def __str__(self) -> str:
        return f'{str(self.left_operand)} {self.token.value} {str(self.right_operand)}'


class Parser():
    def __init__(self, content: str):
        self.tokens = Tokenizer(content).generator()

    def _accept(self, token_type: TokenType) -> bool:
        if self.cur_token == None:
            return False
        if self.cur_token.token_type == token_type:
            self.cur_token = next(self.tokens, None)
            return self.cur_token != None
        return False

    def parse(self) -> bool:
        self.cur_token = next(self.tokens, None)
        if self.cur_token == None:
            print('Empty expression')
            return False
        result = self.E()
        if result and self.cur_token != None:
            excess = list(self.tokens)
            excess.insert(0, self.cur_token)
            print(f'Excess: {excess}')
        return result and self.cur_token == None

    # E -> T {+ T}
    #    | T {- T}
    def E(self) -> bool:
        # print('E()', self.cur_token)
        if not self.T():
            return False
        while (True):
            if self._accept(TokenType.OP_PLUS):
                if not self.T():
                    return False
                continue
            if self._accept(TokenType.OP_MINUS):
                if not self.T():
                    return False
                continue
            return True

    # T -> F {* F}
    #    | F {/ F}
    def T(self) -> bool:
        # print('F()', self.cur_token)
        if not self.F():
            return False
        while (True):
            if self._accept(TokenType.OP_MULT):
                if not self.F():
                    return False
                continue
            if self._accept(TokenType.OP_DIV):
                if not self.F():
                    return False
                continue
            return True

    # F -> num
    #    | (E)
    def F(self) -> bool:
        # print('F()', self.cur_token)
        if self._accept(TokenType.NUMBER):
            return True
        return self._accept(TokenType.PAR_L) and self.E() and self._accept(TokenType.PAR_R)


# Grammar:
# E -> T {+ T}
#    | T {- T}
# T -> F {* F}
#    | F {/ F}
# F -> num
#    | (E)

# Example:
# 1 + 2 * ((3 + 4) * 5)
#
#     (+)
#    /   \
#   1    (*)
#       /   \
#      2    (*)
#          /   \
#        (+)    5
#       /   \
#      3     4
