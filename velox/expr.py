from typing import Any, ForwardRef, Generic, TypeVar

from token import Token


T = TypeVar('T')


class Expr:
    def accept(visitor: ForwardRef("Visitor[T]")) -> T:
        pass


class ExprBinary(Expr):
    def __init__(
        self,
        left: Expr,
        operator: Token,
        right: Expr,
    ) -> None:
        self.left = left
        self.operator = operator
        self.right = right


    def accept(self, visitor: ForwardRef("Visitor[T]")) -> T:
        return visitor.visit_ExprBinary(self)


class ExprGrouping(Expr):
    def __init__(
        self,
        expression: Expr,
    ) -> None:
        self.expression = expression


    def accept(self, visitor: ForwardRef("Visitor[T]")) -> T:
        return visitor.visit_ExprGrouping(self)


class ExprLiteral(Expr):
    def __init__(
        self,
        value: Any,
    ) -> None:
        self.value = value


    def accept(self, visitor: ForwardRef("Visitor[T]")) -> T:
        return visitor.visit_ExprLiteral(self)


class ExprUnary(Expr):
    def __init__(
        self,
        operator: Token,
        right: Expr,
    ) -> None:
        self.operator = operator
        self.right = right


    def accept(self, visitor: ForwardRef("Visitor[T]")) -> T:
        return visitor.visit_ExprUnary(self)


class Visitor(Generic[T]):
    def visit_ExprBinary(
        self,
        expr: ExprBinary
    ) -> T:
        pass


    def visit_ExprGrouping(
        self,
        expr: ExprGrouping
    ) -> T:
        pass


    def visit_ExprLiteral(
        self,
        expr: ExprLiteral
    ) -> T:
        pass


    def visit_ExprUnary(
        self,
        expr: ExprUnary
    ) -> T:
        pass


