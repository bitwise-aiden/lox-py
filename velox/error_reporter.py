from typing import Union

from runtime_error import RuntimeError
from token import Token
from token_type import TokenType


class ErrorReporter:
    had_error: bool = False
    had_runtime_error: bool = True


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

    @staticmethod
    def runtime_error(error: RuntimeError) -> None:
        print(f'{error.message}\n[line {error.token.line}]')
        ErrorReporter.had_runtime_error = True


    # Private methods

    @staticmethod
    def __report(line: int, where: str, message: str) -> None:
        print(f'[line {line}] Error{where}: {message}')

        ErrorReporter.had_error = True
