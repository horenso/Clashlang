from optparse import Option
from node import AssigmentNode, Node, BinOpNode, IdNode, NumNode
from lexer import Token, TokenType
from typing import Iterator, Optional

# Grammar:
# S -> AssignS
#    | printS

# E -> T {+|- T}*
# T -> F {*|/ F}*
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


class Parser():
    def __init__(self, token_generator: Iterator[Token]):
        self.token_generator = token_generator
        self.cur_token = next(self.token_generator, None)

    def accept(self, token_type: TokenType) -> Optional[Token]:
        if self.cur_token is None:
            return None
        if self.cur_token.token_type == token_type:
            current = self.cur_token
            self.cur_token = next(self.token_generator, None)
            return current
        return None

    def parse(self) -> Optional[Node]:
        if self.cur_token is None:
            print('Empty statement')
            return None
        result = self.Stmt()
        if result:
            if self.cur_token is not None:
                excess = list(self.token_generator)
                excess.insert(0, self.cur_token)
                print(f'Excess: {excess}')
                return None
            return result
        return None

    def Block(self) -> Optional[Node]:
        if not self.accept(TokenType.CURL_L):
            return None
        stmts = []
        while True:
            stmt_node = self.Stmt()
            if stmt_node:
                stmts.append(stmt_node)
            else:
                break
        if not self.accept(TokenType.CURL_R):
            return None
        return

    # S -> let id = E;
    #    | ifS
    #    | E;
    def Stmt(self) -> Optional[Node]:
        if self.accept(TokenType.LET):
            id_token = self.accept(TokenType.IDENTIFIER)
            if not id_token:
                return None
            if not self.accept(TokenType.ASSIGN):
                return None
            expression_node = self.Expr()
            if not expression_node:
                return None
            if not self.accept(TokenType.SEMICOLON):
                return None
            return AssigmentNode(id_token, expression_node)
        if_node = self.If_Stmt()
        if if_node:
            return if_node
        expression_node = self.Expr()
        if not expression_node:
            return None
        if not self.accept(TokenType.SEMICOLON):
            return None
        return expression_node

    def If_Stmt(self) -> Optional[Node]:
        pass

    # E -> T {+|- T}*
    def Expr(self) -> Optional[Node]:
        # print('E()', self.cur_token)
        t_node = self.Term()
        if not t_node:
            return None
        while (True):
            plus_token = self.accept(TokenType.OP_PLUS)
            if plus_token:
                t2_node = self.Term()
                if not t2_node:
                    return None
                t_node = BinOpNode(plus_token, t_node, t2_node)
                continue
            minus_token = self.accept(TokenType.OP_MINUS)
            if minus_token:
                t2_token = self.Term()
                if not t2_token:
                    return None
                t_node = BinOpNode(minus_token, t_node, t2_token)
                continue
            return t_node

    # T -> F {*|/ F}*
    def Term(self) -> Optional[Node]:
        f_node = self.Factor()
        if not f_node:
            return None
        while (True):
            mult_token = self.accept(TokenType.OP_MULT)
            if mult_token:
                f2_token = self.Factor()
                if not f2_token:
                    return None
                f_node = BinOpNode(mult_token, f_node, f2_token)
                continue
            div_token = self.accept(TokenType.OP_DIV)
            if div_token:
                f2_token = self.Factor()
                if not f2_token:
                    return None
                result = BinOpNode(div_token, f_node, f2_token)
                f_node = result
                continue
            return f_node

    # F -> num | (E) | id
    def Factor(self) -> Optional[Node]:
        # print('F()', self.cur_token)
        number_token = self.accept(TokenType.LITERAL_NUM)
        if number_token:
            return NumNode(number_token)
        if self.accept(TokenType.PAR_L):
            e = self.Expr()
            if e and self.accept(TokenType.PAR_R):
                return e
        id_token = self.accept(TokenType.IDENTIFIER)
        if id_token:
            return IdNode(id_token)
        return None
