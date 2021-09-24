from typing import Any

from environment import Environment
from error_reporter import ErrorReporter
import expr as Expr
from runtime_error import RuntimeError
import stmt as Stmt
from token import Token
from token_type import TokenType


class Interpreter(Expr.Visitor[Any], Stmt.Visitor[None]):
    # Lifecycle methods

    def __init__(
        self,
    ) -> None:
        self.__environment = Environment()


    # Public methods

    def interpret(
        self,
        statements: list[Stmt.Stmt],
    ) -> None:
        try:
            for statement in statements:
                self.__execute(statement)
        except RuntimeError as error:
            ErrorReporter.runtime_error(error)


    def visit_ExprAssign(
        self,
        expr: Expr.ExprAssign,
    ) -> Any:
        value = self.__evaluate(expr.value)

        self.__environment.assign(expr.name, value)

        return value


    def visit_ExprBinary(
        self,
        expr: Expr.ExprBinary,
    ) -> Any:
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) - float(right)

        if expr.operator.type == TokenType.SLASH:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) / float(right)

        if expr.operator.type == TokenType.STAR:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)

            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

            raise RuntimeError(
                expr.operator,
                'Operands must be two numbers or two strings.',
            )

        if expr.operator.type == TokenType.GREATER:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) > float(right)

        if expr.operator.type == TokenType.GREATER_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)

        if expr.operator.type == TokenType.LESS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) < float(right)

        if expr.operator.type == TokenType.LESS_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.__is_equal(left, right)

        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.__is_equal(left, right)

        return None


    def visit_ExprGrouping(
        self,
        expr: Expr.ExprGrouping,
    ) -> Any:
        return self.__evaluate(
            expr.expression,
        )


    def visit_ExprLiteral(
        self,
        expr: Expr.ExprLiteral,
    ) -> Any:
        return expr.value


    def visit_ExprUnary(
        self,
        expr: Expr.ExprUnary,
    ) -> Any:
        right = self.__evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -float(right)

        if expr.operator.type == TokenType.BANG:
            return not self.__is_truthy(right)

        return None


    def visit_ExprVariable(
        self,
        expr: Expr.ExprVariable,
    ) -> Any:
        return self.__environment.get(expr.name)


    def visit_StmtBlock(
        self,
        stmt: Stmt.StmtBlock,
    ) -> None:
        self.__execute_block(stmt.statements, Environment(self.__environment))


    def visit_StmtExpression(
        self,
        stmt: Stmt.StmtExpression,
    ) -> None:
        self.__evaluate(stmt.expression)


    def visit_StmtPrint(
        self,
        stmt: Stmt.StmtPrint,
    ) -> None:
        value = self.__evaluate(stmt.expression)

        print(self.__stringify(value))


    def visit_StmtVar(
        self,
        stmt: Stmt.StmtVar,
    ) -> None:
        value = None

        if stmt.initializer != None:
            value = self.__evaluate(stmt.initializer)

        self.__environment.define(stmt.name.lexeme, value)


    # Private methods

    def __check_number_operand(
        self,
        operator: Token,
        operand: Any,
    ) -> None:
        if isinstance(operand, float):
            return

        raise RuntimeError(operator, 'Operand must be a number.')


    def __check_number_operands(
        self,
        operator: Token,
        left: Any,
        right: Any,
    ) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RuntimeError(operator, 'Operands must be a numbers.')


    def __evaluate(
        self,
        expr: Expr.Expr,
    ) -> Any:
        return expr.accept(self)


    def __execute(
        self,
        stmt: Stmt.Stmt
    ) -> None:
        stmt.accept(self)


    def __execute_block(
        self,
        statements: list[Stmt.Stmt],
        environment: Environment,
    ) -> None:
        previous = self.__environment

        try:
            self.__environment = environment

            for statement in statements:
                self.__execute(statement)
        finally:
            self.__environment = previous


    def __is_equal(
        self,
        a: Any,
        b: Any,
    ) -> bool:
        return a == b


    def __is_truthy(
        self,
        obj: Any,
    ) -> bool:
        if obj == None:
            return False

        if isinstance(obj, bool):
            return bool(obj)

        return True


    def __stringify(
        self,
        obj: Any,
    ) -> str:
        if obj == None:
            return 'nil'

        if isinstance(obj, float):
            text = str(obj)

            if text.endswith('.0'):
                text = text[:-2]

            return text

        if isinstance(obj, bool):
            if obj:
                return 'true'
            else:
                return 'false'

        return str(obj)
