from typing import Any, ForwardRef

from runtime_error import RuntimeError
from token import Token


class Environment:
    # Lifecycle methods

    def __init__(
        self,
        enclosing: ForwardRef('Environment') = None
    ) -> None:
        self.__enclosing = enclosing
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

        if self.__enclosing:
            self.__enclosing.assign(name, value)
            return

        raise RuntimeError(name, f'Undefined variable \'{name.lexeme}\'.')

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

        if self.__enclosing:
            return self.__enclosing.get(name)

        raise RuntimeError(name, f'Undefined variable \'{name.lexeme}\'.')
