from typing import Any, ForwardRef, Generic, TypeVar

from expr import Expr
from token import Token


T = TypeVar('T')


class Stmt:
    # Public methods

    def accept(
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        pass


class StmtBlock(Stmt):
    # Lifecycle methods

    def __init__(
        self,
        statements: list[Stmt],
    ) -> None:
        self.statements = statements


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_StmtBlock(self)


class StmtExpression(Stmt):
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
        return visitor.visit_StmtExpression(self)


class StmtIf(Stmt):
    # Lifecycle methods

    def __init__(
        self,
        condition: Expr,
        then_branch: Stmt,
        else_branch: Stmt,
    ) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_StmtIf(self)


class StmtPrint(Stmt):
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
        return visitor.visit_StmtPrint(self)


class StmtVar(Stmt):
    # Lifecycle methods

    def __init__(
        self,
        name: Token,
        initializer: Expr,
    ) -> None:
        self.name = name
        self.initializer = initializer


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_StmtVar(self)


class StmtWhile(Stmt):
    # Lifecycle methods

    def __init__(
        self,
        condition: Expr,
        body: Stmt,
    ) -> None:
        self.condition = condition
        self.body = body


    # Public methods

    def accept(
        self,
        visitor: ForwardRef('Visitor[T]'),
    ) -> T:
        return visitor.visit_StmtWhile(self)


class Visitor(Generic[T]):
    # Public methods

    def visit_StmtBlock(
        self,
        stmt: StmtBlock,
    ) -> T:
        pass


    def visit_StmtExpression(
        self,
        stmt: StmtExpression,
    ) -> T:
        pass


    def visit_StmtIf(
        self,
        stmt: StmtIf,
    ) -> T:
        pass


    def visit_StmtPrint(
        self,
        stmt: StmtPrint,
    ) -> T:
        pass


    def visit_StmtVar(
        self,
        stmt: StmtVar,
    ) -> T:
        pass


    def visit_StmtWhile(
        self,
        stmt: StmtWhile,
    ) -> T:
        pass


