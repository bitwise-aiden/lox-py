from typing import Any


class VeloxReturn(Exception):
    # Lifecycle methods

    def __init__(
        self,
        value: Any
    ) -> None:
        super().__init__()

        self.value = value
