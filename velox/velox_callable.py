from typing import Any, ForwardRef


class VeloxCallable:
    # Public methods

    def arity(
        self,
    ) -> int:
        raise NotImplementedError()


    def call(
        self,
        interpreter: ForwardRef('Interpreter'),
        arguments: list[Any],
    ) -> Any:
        raise NotImplementedError()
