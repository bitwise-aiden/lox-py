import expr as Expr


class AstPrinter(Expr.Visitor[str]):
    # Public methods

    def print(
        self,
        expr: Expr.Expr,
    ) -> str:
        return expr.accept(self)


    def visit_ExprBinary(
        self,
        expr: Expr.ExprBinary,
    ) -> str:
        return self.__parenthesize(
            expr.operator.lexeme,
            expr.left,
            expr.right,
        )


    def visit_ExprGrouping(
        self,
        expr: Expr.ExprGrouping,
    ) -> str:
        return self.__parenthesize(
            'group',
            expr.expression,
        )


    def visit_ExprLiteral(
        self,
        expr: Expr.ExprLiteral,
    ) -> str:
        if expr.value == None:
            return 'nil'

        return str(expr.value)


    def visit_ExprUnary(
        self,
        expr: Expr.ExprUnary,
    ) -> str:
        return self.__parenthesize(
            expr.operator.lexeme,
            expr.right,
        )


    # Private methods

    def __parenthesize(
        self,
        name: str,
        *exprs: list[Expr.Expr],
    ) -> str:
        exprs = [
            expr.accept(self)
            for expr in exprs
        ]

        return f'({name} {" ".join(exprs)})'
