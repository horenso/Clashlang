
from abc import abstractmethod
from audioop import mul
from tokenizer import Token, TokenType, Tokenizer
from typing import Iterator, Optional


class Node():
    def __init__(self, token: Token):
        self.token = token

    def __repr__(self) -> str:
        return f'<Node {self.token.__repr__()}>'

    @abstractmethod
    def eval(self):
        pass


class Number(Node):
    def eval(self):
        return float(self.token.value)

    def __str__(self) -> str:
        return f'[{self.token.value}]'


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
        return f'[{str(self.left_operand)} {self.token.value} {str(self.right_operand)}]'


class Parser():
    def __init__(self, content: str):
        self.tokens = Tokenizer(content).generator()

    def _accept(self, token_type: TokenType) -> Optional[Token]:
        if self.cur_token == None:
            return None
        if self.cur_token.token_type == token_type:
            current = self.cur_token
            self.cur_token = next(self.tokens, None)
            return current
        return None

    def parse(self) -> Optional[Node]:
        self.cur_token = next(self.tokens, None)
        if self.cur_token == None:
            print('Empty expression')
            return None
        result = self.E()
        if result:
            if self.cur_token != None:
                excess = list(self.tokens)
                excess.insert(0, self.cur_token)
                print(f'Excess: {excess}')
                return None
            return result
        return None

    # E -> T {+ T}
    #    | T {- T}
    def E(self) -> Optional[Node]:
        # print('E()', self.cur_token)
        t_node = self.T()
        if not t_node:
            return None
        while (True):
            plus_token = self._accept(TokenType.OP_PLUS)
            if plus_token:
                t2_node = self.T()
                if not t2_node:
                    return None
                t_node = BinOperation(plus_token, t_node, t2_node)
                continue
            minus_token = self._accept(TokenType.OP_MINUS)
            if minus_token:
                t2_token = self.T()
                if not t2_token:
                    return None
                t_node = BinOperation(minus_token, t_node, t2_token)
                continue
            return t_node

    # T -> F {* F}
    #    | F {/ F}
    def T(self) -> Optional[Node]:
        f_node = self.F()
        if not f_node:
            return None
        while (True):
            mult_token = self._accept(TokenType.OP_MULT)
            if mult_token:
                f2_token = self.F()
                if not f2_token:
                    return None
                f_node = BinOperation(mult_token, f_node, f2_token)
                continue
            div_token = self._accept(TokenType.OP_DIV)
            if div_token:
                f2_token = self.F()
                if not f2_token:
                    return None
                result = BinOperation(div_token, f_node, f2_token)
                f_node = result
                continue
            return f_node

    # F -> num
    #    | (E)
    def F(self) -> Optional[Node]:
        # print('F()', self.cur_token)
        number_token = self._accept(TokenType.NUMBER)
        if number_token:
            return Number(number_token)
        if self._accept(TokenType.PAR_L):
            e = self.E()
            if e and self._accept(TokenType.PAR_R):
                return e
        return None


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
