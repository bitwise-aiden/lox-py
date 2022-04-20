from typing import Any

from callables import Clock, VeloxClass, VeloxFunction
from environment import Environment
from error_reporter import ErrorReporter
import expr as Expr
from runtime_error import RuntimeError
import stmt as Stmt
from token import Token
from token_type import TokenType
from velox_callable import VeloxCallable
from velox_instance import VeloxInstance
from velox_return import VeloxReturn


class Interpreter(Expr.Visitor[Any], Stmt.Visitor[None]):
    # Lifecycle methods

    def __init__(
        self,
    ) -> None:
        self.__globals = Environment()
        self.__globals.define('clock', Clock)

        self.__locals = {}

        self.environment = self.__globals


    # Public methods


    def execute_block(
        self,
        statements: list[Stmt.Stmt],
        environment: Environment,
    ) -> None:
        previous = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.__execute(statement)
        finally:
            self.environment = previous


    def interpret(
        self,
        statements: list[Stmt.Stmt],
    ) -> None:
        try:
            for statement in statements:
                self.__execute(statement)
        except RuntimeError as error:
            ErrorReporter.runtime_error(error)


    def resolve(
        self,
        expr: Expr.Expr,
        depth: int,
    ) -> None:
        self.__locals[expr] = depth


    def visit_ExprAssign(
        self,
        expr: Expr.ExprAssign,
    ) -> Any:
        value = self.__evaluate(expr.value)

        distance = self.__locals.get(expr)

        if distance != None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.__globals.assign(expr.name, value)

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


    def visit_ExprCall(
        self,
        expr: Expr.ExprCall,
    ) -> Any:
        callee = self.__evaluate(expr.callee)

        arguments = [
            self.__evaluate(argument) for argument in expr.arguments
        ]

        if not isinstance(callee, VeloxCallable):
            raise RuntimeError(expr.paren, 'Can only call functions and classes.')


        if len(arguments) != callee.arity():
            raise RuntimeError(expr.paren, f'Expected {callee.arity()} arguments but got {len(arguments)}.')

        return callee.call(self, arguments)


    def visit_ExprGet(
        self,
        expr: Expr.ExprGet,
    ) -> Any:
        object = self.__evaluate(expr.object)

        if isinstance(object, VeloxInstance):
            return object.get(expr.name)

        raise RuntimeError(expr.name, 'Only instances have properties.')


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


    def visit_ExprLogical(
        self,
        expr: Expr.ExprLogical,
    ) -> Any:
        left = self.__evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.__is_truthy(left):
                return left
        else:
            if not self.__is_truthy(left):
                return left

        return self.__evaluate(expr.right)


    def visit_ExprSet(
        self,
        expr: Expr.ExprSet,
    ) -> Any:
        object = self.__evaluate(expr.object)

        if not isinstance(object, VeloxInstance):
            raise RuntimeError(expr.name, "Only instances have fields.")

        value = self.__evaluate(expr.value)

        object.set(expr.name, value)

        return value


    def visit_ExprThis(
        self,
        expr: Expr.ExprThis,
    ) -> Any:
        return self.__look_up_variable(expr.keyword, expr)


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
        return self.__look_up_variable(expr.name, expr)


    def visit_StmtBlock(
        self,
        stmt: Stmt.StmtBlock,
    ) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))


    def visit_StmtClass(
        self,
        stmt: Stmt.StmtClass,
    ) -> None:
        self.environment.define(stmt.name.lexeme, None)

        methods = {}
        for method in stmt.methods:
            is_initializer = method.name.lexeme == 'init'

            function = VeloxFunction(method, self.environment, is_initializer)

            methods[method.name.lexeme] = function

        klass = VeloxClass(stmt.name.lexeme, methods)

        self.environment.assign(stmt.name, klass)


    def visit_StmtExpression(
        self,
        stmt: Stmt.StmtExpression,
    ) -> None:
        self.__evaluate(stmt.expression)


    def visit_StmtFunction(
        self,
        stmt: Stmt.StmtFunction,
    ) -> None:
        function = VeloxFunction(stmt, self.environment, False)

        self.environment.define(stmt.name.lexeme, function)


    def visit_StmtIf(
        self,
        stmt: Stmt.StmtIf,
    ) -> None:
        if self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self.__execute(stmt.else_branch)


    def visit_StmtPrint(
        self,
        stmt: Stmt.StmtPrint,
    ) -> None:
        value = self.__evaluate(stmt.expression)

        print(self.__stringify(value))


    def visit_StmtReturn(
        self,
        stmt: Stmt.StmtReturn,
    ) -> None:
        value = None

        if stmt.value != None:
            value = self.__evaluate(stmt.value)

        raise VeloxReturn(value)


    def visit_StmtVar(
        self,
        stmt: Stmt.StmtVar,
    ) -> None:
        value = None

        if stmt.initializer != None:
            value = self.__evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)


    def visit_StmtWhile(
        self,
        stmt: Stmt.StmtVar,
    ) -> None:
        while self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.body)


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

        raise RuntimeError(operator, 'Operands must be numbers.')


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


    def __look_up_variable(
        self,
        name: Token,
        expr: Expr.Expr,
    ) -> Any:
        distance = self.__locals.get(expr)

        if distance != None:
            return self.environment.get_at(distance, name.lexeme)

        return self.__globals.get(name)


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
