class ErrorReporter:
    had_error: bool = False

    # Public methods

    @staticmethod
    def error(line: int, message: str) -> None:
        ErrorReporter.__report(line, '', message)


    # Private methods

    @staticmethod
    def __report(line: int, where: str, message: str) -> None:
        print(f'[line {line}] Error{where}: {message}')

        ErrorReporter.had_error = True
