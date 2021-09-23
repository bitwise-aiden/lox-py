from typing import Any, ForwardRef, Generic, TypeVar

from token import Token


T = TypeVar('T')


class Expr:
    # Public methods

    def accept(
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        pass


class ExprBinary(Expr):
    # Lifecycle methods

    def __init__(
        self,
        left: Expr,
        operator: Token,
        right: Expr,
    ) -> None:
        self.left = left
        self.operator = operator
        self.right = right


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_ExprBinary(self)


class ExprGrouping(Expr):
    # Lifecycle methods

    def __init__(
        self,
        expression: Expr,
    ) -> None:
        self.expression = expression


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_ExprGrouping(self)


class ExprLiteral(Expr):
    # Lifecycle methods

    def __init__(
        self,
        value: Any,
    ) -> None:
        self.value = value


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_ExprLiteral(self)


class ExprUnary(Expr):
    # Lifecycle methods

    def __init__(
        self,
        operator: Token,
        right: Expr,
    ) -> None:
        self.operator = operator
        self.right = right


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_ExprUnary(self)


class Visitor(Generic[T]):
    # Public methods

    def visit_ExprBinary(
        self,
        expr: ExprBinary,
    ) -> T:
        pass


    def visit_ExprGrouping(
        self,
        expr: ExprGrouping,
    ) -> T:
        pass


    def visit_ExprLiteral(
        self,
        expr: ExprLiteral,
    ) -> T:
        pass


    def visit_ExprUnary(
        self,
        expr: ExprUnary,
    ) -> T:
        pass
