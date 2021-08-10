from error_reporter import ErrorReporter
from expr import *
from token import Token
from token_type import TokenType


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0


    def parse(self) -> Expr:
        try:
            return self.__expression()
        except ParseError as error:
            return None


    # Private methods
    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1


    def __check(self, type: TokenType) -> bool:
        if self.__is_at_end():
            return False

        return self.__peek().type == type


    def __comparison(self) -> Expr:
        expr = self.__term()

        while self.__match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.__previous()
            right = self.__term()
            expr = ExprBinary(expr, operator, right)

        return expr


    def __consume(self, type: TokenType, message: str) -> Token:
        if self.__check(type):
            return self.__advance()

        raise self.__error(self.__peek(), message)


    def __equality(self) -> Expr:
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = ExprBinary(expr, operator, right)

        return expr


    def __error(self, token: Token, message: str) -> ParseError:
        ErrorReporter.error(token, message)
        return ParseError()


    def __expression(self) -> Expr:
        return self.__equality()


    def __factor(self) -> Expr:
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = ExprBinary(expr, operator, right)

        return expr


    def __is_at_end(self) -> bool:
        return self.__peek().type == TokenType.EOF


    def __match(self, *types: list[TokenType]) -> bool:
        for type in types:
            if self.__check(type):
                self.__advance()
                return True

        return False


    def __peek(self) -> Token:
        return self.__tokens[self.__current]


    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]


    def __primary(self) -> Expr:
        if self.__match(TokenType.FALSE):
            return ExprLiteral(False)

        if self.__match(TokenType.TRUE):
            return ExprLiteral(True)

        if self.__match(TokenType.NIL):
            return ExprLiteral(None)

        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return ExprLiteral(self.__previous().literal)

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(
                TokenType.RIGHT_PAREN,
                "Expect ')' after expression."
            )
            return ExprGourping(expr)

        raise self.__error(self.__peek(), "Expect expression.")


    def __synchronize(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().type == TokenType.SEMICOLON:
                return

            if self.__peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.__advance()


    def __term(self) -> Expr:
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = ExprBinary(expr, operator, right)

        return expr


    def __unary(self) -> Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return ExprUnary(operator, right)

        return self.__primary()
