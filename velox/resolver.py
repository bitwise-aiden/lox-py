from typing import Any, Union

from error_reporter import ErrorReporter
import expr as Expr
from function_type import FunctionType
from interpreter import Interpreter
import stmt as Stmt
from token import Token

class Resolver(Expr.Visitor[None], Stmt.Visitor[None]):
    # Lifecycle methods

    def __init__(
        self,
        interpreter: Interpreter,
    ) -> None:
        self.__interpreter = interpreter

        self.__current_function = FunctionType.NONE
        self.__scopes = []


    # Public methods

    def resolve(
        self,
        *statements: list[Union[Expr.Expr,Stmt.Stmt]],
    ) -> None:
        for statement in statements:
            statement.accept(self)


    def visit_ExprAssign(
        self,
        expr: Expr.ExprAssign,
    ) -> None:
        self.resolve(expr.value)

        self.__resolve_local(expr, expr.name)


    def visit_ExprBinary(
        self,
        expr: Expr.ExprBinary,
    ) -> None:
        self.resolve(expr.left)

        self.resolve(expr.right)


    def visit_ExprCall(
        self,
        expr: Expr.ExprCall,
    ) -> None:
        self.resolve(expr.callee)

        for argument in expr.arguments:
            self.resolve(argument)


    def visit_ExprGrouping(
        self,
        expr: Expr.ExprGrouping,
    ) -> None:
        self.resolve(expr.expression)


    def visit_ExprLiteral(
        self,
        expr: Expr.ExprLiteral,
    ) -> None:
        pass


    def visit_ExprLogical(
        self,
        expr: Expr.ExprLogical,
    ) -> None:
        self.resolve(expr.left)

        self.resolve(expr.right)


    def visit_ExprUnary(
        self,
        expr: Expr.ExprUnary,
    ) -> None:
        self.resolve(expr.right)


    def visit_ExprVariable(
        self,
        expr: Expr.ExprVariable,
    ) -> None:
        if len(self.__scopes) != 0 and self.__scopes[-1].get(expr.name.lexeme) == False:
            ErrorReporter.error(expr.name, 'Can\'t read local variable in it\'s own initializer.')

        self.__resolve_local(expr, expr.name)


    def visit_StmtBlock(
        self,
        stmt: Stmt.StmtBlock,
    ) -> None:
        self.__begin_scope()

        self.resolve(*stmt.statements)

        self.__end_scope()


    def visit_StmtExpression(
        self,
        stmt: Stmt.StmtExpression,
    ) -> None:
        self.resolve(stmt.expression)


    def visit_StmtFunction(
        self,
        stmt: Stmt.StmtFunction,
    ) -> None:
        self.__declare(stmt.name)

        self.__define(stmt.name)

        self.__resolve_function(stmt, FunctionType.FUNCTION)


    def visit_StmtIf(
        self,
        stmt: Stmt.StmtIf,
    ) -> None:
        self.resolve(stmt.condition)

        self.resolve(stmt.then_branch)

        if stmt.else_branch != None:
             self.resolve(stmt.else_branch)


    def visit_StmtPrint(
        self,
        stmt: Stmt.StmtPrint,
    ) -> None:
        self.resolve(stmt.expression)


    def visit_StmtReturn(
        self,
        stmt: Stmt.StmtReturn,
    ) -> None:
        if self.__current_function == FunctionType.NONE:
            ErrorReporter.error(stmt.keyword, 'Can\'t return from top-level code.')

        if stmt.value != None:
            self.resolve(stmt.value)


    def visit_StmtVar(
        self,
        stmt: Stmt.StmtVar,
    ) -> None:
        self.__declare(stmt.name)

        if stmt.initializer != None:
            self.resolve(stmt.initializer)

        self.__define(stmt.name)


    def visit_StmtWhile(
        self,
        stmt: Stmt.StmtWhile,
    ) -> None:
        self.resolve(stmt.condition)

        self.resolve(stmt.body)


    # Private methods

    def __begin_scope(
        self,
    ) -> None:
        self.__scopes.append({})


    def __declare(
        self,
        name: Token,
    ) -> None:
        if len(self.__scopes) == 0:
            return

        scope = self.__scopes[-1]

        if name in scope:
            ErrorReporter.error(name, 'Already a variable with this name in this scope.')

        scope[name.lexeme] = False


    def __define(
        self,
        name: Token,
    ) -> None:
        if len(self.__scopes) == 0:
            return

        self.__scopes[-1][name.lexeme] = True


    def __end_scope(
        self,
    ) -> None:
        self.__scopes.pop()


    def __resolve_function(
        self,
        function: Stmt.StmtFunction,
        type: FunctionType,
    ) -> None:
        enclosing_function = self.__current_function
        self.__current_function = type

        self.__begin_scope()

        for param in function.params:
            self.__declare(param)

            self.__define(param)

        self.resolve(*function.body)

        self.__end_scope()

        self.__current_function = enclosing_function


    def __resolve_local(
        self,
        expr: Expr.Expr,
        name: Token,
    ) -> None:
        for i, scope in enumerate(self.__scopes[::-1]):
            if name.lexeme in scope:
                self.__interpreter.resolve(expr, i)
