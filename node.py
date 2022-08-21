
from abc import ABC, abstractmethod
from typing import List, Optional
from runtime import Runtime
from lexer import Token, TokenType


class Node(ABC):
    def __str__(self) -> str:
        return f'{type(self)}'

    @abstractmethod
    def eval(self, runtime: Runtime):
        pass


class BlockNode(Node):
    def __init__(self, stmts: List[Node]):
        self.stmts = stmts

    def eval(self, runtime: Runtime):
        for statement in self.stmts:
            statement.eval()


class NumNode(Node):
    def __init__(self, token: Token):
        self.token = token

    def eval(self, runtime: Runtime):
        return float(self.token.value)

    def __str__(self) -> str:
        return self.token.value


class IdNode(Node):
    def __init__(self, token: Token):
        self.token = token

    def eval(self, runtime: Runtime):
        return runtime.get_value(self.token.value) or 0.0

    def __str__(self) -> str:
        return f'{self.token.value}'


class IfNode(Node):
    def __init__(self, consequence: Node, alternative: Optional[Node]):
        self.consequence = consequence
        self.alternative = alternative


class BinOpNode(Node):
    def __init__(self, token: Token, left_operand: Node, right_operand: Node):
        self.token = token
        self.left_operand = left_operand
        self.right_operand = right_operand

    def eval(self, runtime: Runtime):
        token_type = self.token.token_type
        if token_type == TokenType.OP_PLUS:
            return self.left_operand.eval(runtime) + self.right_operand.eval(runtime)
        if token_type == TokenType.OP_MINUS:
            return self.left_operand.eval(runtime) - self.right_operand.eval(runtime)
        if token_type == TokenType.OP_MULT:
            return self.left_operand.eval(runtime) * self.right_operand.eval(runtime)
        if token_type == TokenType.OP_DIV:
            return self.left_operand.eval(runtime) / self.right_operand.eval(runtime)

    def __str__(self) -> str:
        return f'[{str(self.left_operand)} {self.token.value} {str(self.right_operand)}]'


class AssigmentNode(Node):
    def __init__(self, identifier_token: Token, expression_node: Node):
        self.id = identifier_token
        self.expression = expression_node

    def eval(self, runtime: Runtime):
        expression_result = self.expression.eval(runtime)
        runtime.assign_value(self.id.value, expression_result)
        return expression_result

    def __str__(self) -> str:
        return f'[{self.id.value} <- {str(self.expression)}]'
