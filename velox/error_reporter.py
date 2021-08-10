from typing import Union

from token import Token
from token_type import TokenType


class ErrorReporter:
    had_error: bool = False

    # Public methods
    @staticmethod
    def error(where: Union[int, Token], message: str) -> None:
        if isinstance(where, int):
            ErrorReporter.__report(where, '', message)
        elif isinstance(where, Token):
            if where.type == TokenType.EOF:
                ErrorReporter.__report(token.line, ' at end', message)
            else:
                ErrorReporter.__report(
                    where.line,
                    f' at\'{where.lexeme}\'',
                    message,
                )


    # Private methods

    @staticmethod
    def __report(line: int, where: str, message: str) -> None:
        print(f'[line {line}] Error{where}: {message}')

        ErrorReporter.had_error = True
