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
    ) -> None:
        self.__declaration = declaration
        self.__closure = closure


    def __str__(
        self
    ) -> str:
        return f'<fn {self.__declaration.name.lexeme}>'


    # Public methods

    def arity(
        self,
    ) -> int:
        return len(self.__declaration.params)


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
            return return_value.value
