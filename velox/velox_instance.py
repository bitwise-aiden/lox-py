from typing import Any, ForwardRef

from token import Token


class VeloxInstance:
    # Lifecycle methods

    def __init__(
        self,
        klass: ForwardRef('VeloxClass'),
    ) -> None:
        self.klass = klass
        self.__fields = {}


    def __str__(
        self,
    ) -> str:
        return f'{self.klass.name} instance'


    # Public methods

    def get(
        self,
        name: Token,
    ) -> Any:
        if name.lexeme in self.__fields:
            return self.__fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method:
            return method.bind(self)

        raise RuntimeError(name, f'Undefined property \'{name.lexeme}\'.')


    def set(
        self,
        name: Token,
        value: Any,
    ) -> None:
        self.__fields[name.lexeme] = value
