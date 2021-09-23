from expr import *


class AstPrinter(Visitor[str]):
    # Public methods

    def print(
        self,
        expr: Expr,
    ) -> str:
        return expr.accept(self)


    def visit_ExprBinary(
        self,
        expr: ExprBinary,
    ) -> str:
        return self.__parenthesize(
            expr.operator.lexeme,
            expr.left,
            expr.right,
        )


    def visit_ExprGrouping(
        self,
        expr: ExprGrouping,
    ) -> str:
        return self.__parenthesize(
            'group',
            expr.expression,
        )


    def visit_ExprLiteral(
        self,
        expr: ExprLiteral,
    ) -> str:
        if expr.value == None:
            return 'nil'

        return str(expr.value)


    def visit_ExprUnary(
        self,
        expr: ExprUnary,
    ) -> str:
        return self.__parenthesize(
            expr.operator.lexeme,
            expr.right,
        )


    # Private methods

    def __parenthesize(
        self,
        name: str,
        *exprs: list[Expr],
    ) -> str:
        exprs = [
            expr.accept(self)
            for expr in exprs
        ]

        return f'({name} {" ".join(exprs)})'
