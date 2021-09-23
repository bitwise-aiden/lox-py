from typing import Any

from error_reporter import ErrorReporter
from expr import *
from runtime_error import RuntimeError
from token import Token
from token_type import TokenType


class Interpreter(Visitor[Any]):
    def interpret(
        self,
        expression: Expr
    ) -> None:
        try:
            value = self.__evaluate(expression)
            print(self.__stringify(value))
        except RuntimeError as error:
            ErrorReporter.runtime_error(error)


    def visit_ExprBinary(
        self,
        expr: ExprBinary
    ) -> Any:
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.SLASH:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.PLUS:
            if type(left) == type(right) == float:
                return float(left) + float(right)
            elif type(left) == type(right) == str:
                return str(left) + str(right)

            raise RuntimeError(
                expr.operator,
                "Operands must be two numbers or two strings.",
            )
        elif expr.operator.type == TokenType.GREATER:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.__is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.__is_equal(left, right)

        return None


    def visit_ExprGrouping(
        self,
        expr: ExprGrouping
    ) -> Any:
        return self.__evaluate(
            expr.expression,
        )


    def visit_ExprLiteral(
        self,
        expr: ExprLiteral
    ) -> Any:
        return expr.value


    def visit_ExprUnary(
        self,
        expr: ExprUnary
    ) -> Any:
        right = self.__evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.__is_truthy(right)

        return None


    # Private methods

    def __check_number_operand(
        self,
        operator: Token,
        operand: Any
    ) -> None:
        if type(operand) == float:
            return

        raise RuntimeError(operator, "Operand must be a number.")


    def __check_number_operands(
        self,
        operator: Token,
        left: Any,
        right: Any
    ) -> None:
        if type(left) == type(right) == float:
            return

        raise RuntimeError(operator, "Operands must be a numbers.")


    def __evaluate(
        self,
        expr: Expr
    ) -> Any:
        return expr.accept(self)


    def __is_equal(
        self,
        a: Any,
        b: Any,
    ) -> bool:
        return a == b


    def __is_truthy(
        self,
        obj: Any
    ) -> bool:
        if obj == None:
            return False
        elif type(obj) == bool:
            return bool(obj)

        return True


    def __stringify(
        self,
        obj: Any
    ) -> str:
        if obj == None:
            return "nil"

        if type(obj) == float:
            text = str(obj)

            if text.endswith(".0"):
                text = text[:-2]

            return text
        elif type(obj) == bool:
            if obj:
                return "true"
            else:
                return "false"

        return str(obj)
