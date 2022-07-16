from typing import Any, ForwardRef

from runtime_error import RuntimeError
from token import Token


class Environment:
    # Lifecycle methods

    def __init__(
        self,
        enclosing: ForwardRef('Environment') = None
    ) -> None:
        self.enclosing = enclosing
        self.__values = {}


    # Public methods

    def assign(
        self,
        name: Token,
        value: Any
    ) -> None:
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f'Undefined variable \'{name.lexeme}\'.')


    def assign_at(
        self,
        distance: int,
        name: Token,
        value: Any
    ) -> None:
        self.__ancestor(distance).__values[name.lexeme] = value

    def define(
        self,
        name: str,
        value: Any,
    ) -> None:
        self.__values[name] = value


    def get(
        self,
        name: Token,
    ) -> Any:
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(name, f'Undefined variable \'{name.lexeme}\'.')


    def get_at(
        self,
        distance: int,
        name: str,
    ) -> Any:
        return self.__ancestor(distance).__values.get(name)


    # Private methods

    def __ancestor(
        self,
        distance: int,
    ) -> ForwardRef('Environment'):
        environment = self

        for _ in range(distance):
            environment = environment.enclosing

        return environment
