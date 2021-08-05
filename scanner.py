from typing import Any

from error_reporter import ErrorReporter
from token import Token
from token_type import TokenType


class Scanner:
    KEYWORDS = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'fun': TokenType.FUN,
        'for': TokenType.FOR,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
    }


    def __init__(self, source) -> None:
        self.__source = source
        self.__start = 0
        self.__current = 0
        self.__line = 1
        self.__tokens = []


    # Public methods

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.__start = self.__current
            self.__scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))

        return self.__tokens


    # Private methods

    def __add_token(self, type: TokenType, literal: Any = None) -> None:
        text = self.__source[self.__start: self.__current]
        self.__tokens.append(Token(type, text, literal, self.__line))


    def __advance(self) -> str:
        c = self.__source[self.__current]

        self.__current += 1

        return c


    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False

        if self.__source[self.__current] != expected:
            return False

        self.__current += 1

        return True


    def __identifier(self) -> None:
        while self.__is_alpha_numeric(self.__peek()):
            self.__advance()

        value = self.__source[self.__start: self.__current]

        token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)

        self.__add_token(token_type)


    def __is_alpha(self, c: str) -> bool:
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'


    def __is_alpha_numeric(self, c: str) -> bool:
        return self.__is_alpha(c) or self.__is_digit(c)


    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)


    def __is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'


    def __number(self) -> None:
        while self.__is_digit(self.__peek()):
            self.__advance()

        if self.__peek() == '.' and self.__is_digit(self.__peek_next()):
            self.__advance()

            while self.__is_digit(self.__peek()):
                self.__advance()

        value = float(self.__source[self.__start: self.__current])

        self.__add_token(TokenType.NUMBER, value)


    def __peek(self) -> str:
        if self.__is_at_end():
            return '\0'

        return self.__source[self.__current]


    def __peek_next(self) -> str:
        if self.__current + 1 > len(self.__source):
            return '\0'

        return self.__source[self.__current]


    def __scan_token(self) -> None:
        c = self.__advance()

        if c == '(':
            self.__add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.__add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.__add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.__add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.__add_token(TokenType.COMMA)
        elif c == '.':
            self.__add_token(TokenType.DOT)
        elif c == '-':
            self.__add_token(TokenType.MINUS)
        elif c == '+':
            self.__add_token(TokenType.PLUS)
        elif c == ';':
            self.__add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.__add_token(TokenType.STAR)
        elif c == '!':
            if self.__match('='):
                self.__add_token(TokenType.BANG_EQUAL)
            else:
                self.__add_token(TokenType.BANG)
        elif c == '=':
            if self.__match('='):
                self.__add_token(TokenType.EQUAL_EQUAL)
            else:
                self.__add_token(TokenType.EQUAL)
        elif c == '<':
            if self.__match('='):
                self.__add_token(TokenType.LESS_EQUAL)
            else:
                self.__add_token(TokenType.LESS)
        elif c == '>':
            if self.__match('='):
                self.__add_token(TokenType.GREATER_EQUAL)
            else:
                self.__add_token(TokenType.GREATER)
        elif c == '/':
            if self.__match('/'):
                while self.__peek() != '\n' and not self.__is_at_end():
                    self.__advance()
            else:
                self.__add_token(TokenType.SLASH)
        elif c == ' ':
            pass
        elif c == '\r':
            pass
        elif c == '\t':
            pass
        elif c == '\n':
            self.__line += 1
        elif c == '"':
            self.__string()
        elif self.__is_digit(c):
            self.__number()
        elif self.__is_alpha(c):
            self.__identifier()
        else:
            ErrorReporter.error(self.__line, "Unexpected character.")


    def __string(self) -> None:
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == '\n':
                self.__line += 1

            self.__advance()

        if self.__is_at_end():
            ErrorReporter.error(self.__line, "Unterminated string.")

        self.__advance()

        value = self.__source[self.__start + 1: self.__current - 1]

        self.__add_token(TokenType.STRING, value)
