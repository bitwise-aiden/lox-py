import sys

from error_reporter import ErrorReporter
from scanner import Scanner


class Velox:
    # Public methods

    @staticmethod
    def run_file(path: str) -> None:
        with open(path, 'r') as in_file:
            source = in_file.read()

            Velox.__run(source)

            if ErrorReporter.had_error:
                sys.exit(65)


    @staticmethod
    def run_prompt() -> None:
        try:
            while True:
                line = input('> ')

                Velox.__run(line)

                ErrorReporter.had_error = False
        except EOFError:
            pass


    # Private methods

    @staticmethod
    def __run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)


if __name__ == '__main__':
    _, *args = sys.argv

    if len(args) > 1:
        print('Usage: velox [script]')
        sys.exit(64)
    elif len(args) == 1:
        Velox.run_file(args[0])
    else:
        Velox.run_prompt()