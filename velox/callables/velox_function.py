from typing import Any, ForwardRef

from environment import Environment
import stmt as Stmt
from velox_callable import VeloxCallable
from velox_return import VeloxReturn


class VeloxFunction(VeloxCallable):
    # Lifecycle methods

    def __init__(
        self,
        declaration: Stmt.StmtFunction,
        closure: Environment,
        is_initializer: bool
    ) -> None:
        self.__declaration = declaration
        self.__closure = closure
        self.__is_initializer = is_initializer


    def __str__(
        self
    ) -> str:
        return f'<fn {self.__declaration.name.lexeme}>'


    # Public methods

    def arity(
        self,
    ) -> int:
        return len(self.__declaration.params)


    def bind(
        self,
        instance: ForwardRef('VeloxInstance'),
    ) -> ForwardRef('VeloxFunction'):
        environment = Environment(self.__closure)

        environment.define('this', instance)

        return VeloxFunction(
            self.__declaration,
            environment,
            self.__is_initializer,
        )


    def call(
        self,
        interpreter: ForwardRef('Interpreter'),
        arguments: list[Any],
    ) -> Any:
        environment = Environment(self.__closure)

        for param, argument in zip(self.__declaration.params, arguments):
            environment.define(param.lexeme, argument)

        try:
            interpreter.execute_block(self.__declaration.body, environment)
        except VeloxReturn as return_value:
            if self.__is_initializer:
                return self.__closure.get_at(0, 'this')

            return return_value.value

        if self.__is_initializer:
            return self.__closure.get_at(0, 'this')
