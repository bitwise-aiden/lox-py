import time
from typing import Any, ForwardRef

from velox_callable import VeloxCallable


class Clock(VeloxCallable):
    # Lifecylce methods

    def __str__(
        self,
    ) -> str:
        return '<native fn>'


    # Public functions

    def arity(
        self,
    ) -> int:
        return 0


    def call(
        self,
        interpreter: ForwardRef('Interpreter'),
        arguments: list[Any],
    ) -> float:
        return time.time()
