from token import Token


class RuntimeError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        super(message)

        self.token = token
