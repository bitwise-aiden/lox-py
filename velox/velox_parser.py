from error_reporter import ErrorReporter
import expr as Expr
import stmt as Stmt
from token import Token
from token_type import TokenType


class ParseError(Exception):
    pass


class Parser:
    # Lifecycle methods

    def __init__(
        self,
        tokens: list[Token],
    ) -> None:
        self.__tokens = tokens
        self.__current = 0


    # Public methods

    def parse(
        self,
    ) -> list[Stmt.Stmt]:
        statements = []

        while (not self.__is_at_end()):
            statements.append(self.__declaration())

        return statements


    # Private methods

    def __advance(
        self,
    ) -> Token:
        if not self.__is_at_end():
            self.__current += 1

        return self.__previous()


    def __assignment(
        self,
    )-> Expr.Expr:
        expr = self.__equality()

        if self.__match(TokenType.EQUAL):
            equals = self.__previous()
            value = self.__assignment()

            if isinstance(expr, Expr.ExprVariable):
                name = expr.name
                return Expr.ExprAssign(name, value)

            self.__error(equals, 'Invalid assignment target.')

        return expr


    def __block(
        self,
    ) -> list[Stmt.Stmt]:
        statements = []

        while not (self.__check(TokenType.RIGHT_BRACE) or self.__is_at_end()):
            statements.append(self.__declaration())

        self.__consume(TokenType.RIGHT_BRACE, 'Expect \'}\' after block.')

        return statements


    def __check(
        self,
        type: TokenType,
    ) -> bool:
        if self.__is_at_end():
            return False

        return self.__peek().type == type


    def __comparison(
        self,
    ) -> Expr.Expr:
        expr = self.__term()

        while self.__match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.__previous()
            right = self.__term()
            expr = Expr.ExprBinary(expr, operator, right)

        return expr


    def __consume(
        self,
        type: TokenType,
        message: str,
    ) -> Token:
        if self.__check(type):
            return self.__advance()

        raise self.__error(self.__peek(), message)


    def __declaration(
        self,
    ) -> Stmt:
        try:
            if self.__match(TokenType.VAR):
                return self.__var_declaration()

            return self.__statement()
        except ParseError:
            self.__synchronize()


    def __equality(
        self,
    ) -> Expr.Expr:
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = Expr.ExprBinary(expr, operator, right)

        return expr


    def __error(
        self,
        token: Token,
        message: str,
    ) -> ParseError:
        ErrorReporter.error(token, message)
        return ParseError()


    def __expression(
        self,
    ) -> Expr.Expr:
        return self.__assignment()


    def __expression_statement(
        self,
    ) -> Stmt.Stmt:
        expr = self.__expression()

        self.__consume(TokenType.SEMICOLON, 'Expected \';\' after expression')

        return Stmt.StmtExpression(expr)


    def __factor(
        self,
    ) -> Expr.Expr:
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = Expr.ExprBinary(expr, operator, right)

        return expr


    def __is_at_end(
        self,
    ) -> bool:
        return self.__peek().type == TokenType.EOF


    def __match(
        self,
        *types: list[TokenType],
    ) -> bool:
        for type in types:
            if self.__check(type):
                self.__advance()
                return True

        return False


    def __peek(
        self,
    ) -> Token:
        return self.__tokens[self.__current]


    def __previous(
        self,
    ) -> Token:
        return self.__tokens[self.__current - 1]


    def __primary(
        self,
    ) -> Expr.Expr:
        if self.__match(TokenType.FALSE):
            return Expr.ExprLiteral(False)

        if self.__match(TokenType.TRUE):
            return Expr.ExprLiteral(True)

        if self.__match(TokenType.NIL):
            return Expr.ExprLiteral(None)

        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Expr.ExprLiteral(self.__previous().literal)

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(
                TokenType.RIGHT_PAREN,
                'Expect \')\' after expression.'
            )
            return Expr.ExprGrouping(expr)

        if self.__match(TokenType.IDENTIFIER):
            return Expr.ExprVariable(self.__previous())

        raise self.__error(self.__peek(), 'Expect expression.')


    def __print_statement(
        self,
    ) -> Stmt.Stmt:
        value = self.__expression()

        self.__consume(TokenType.SEMICOLON, 'Expected \';\' after value.')

        return Stmt.StmtPrint(value)


    def __statement(
        self
    ) -> Stmt.Stmt:
        if self.__match(TokenType.PRINT):
            return self.__print_statement()

        if self.__match(TokenType.LEFT_BRACE):
            return Stmt.StmtBlock(self.__block())

        return self.__expression_statement()


    def __synchronize(
        self,
    ) -> None:
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


    def __term(
        self,
    ) -> Expr.Expr:
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = Expr.ExprBinary(expr, operator, right)

        return expr


    def __unary(
        self,
    ) -> Expr.Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return Expr.ExprUnary(operator, right)

        return self.__primary()


    def __var_declaration(
        self,
    ) -> Stmt.Stmt:
        name = self.__consume(TokenType.IDENTIFIER, 'Expected variable name.')

        initializer = None
        if self.__match(TokenType.EQUAL):
            initializer = self.__expression()

        self.__consume(TokenType.SEMICOLON, 'Expect \';\' after variable declaration')

        return Stmt.StmtVar(name, initializer)
