import sys
from typing import AnyStr, IO


class GenerateAst:
    # Public methods

    @staticmethod
    def define_ast(
        output_directory: str,
        base_name: str,
        types: list[str],
        imports: list[str],
    ) -> None:
        path = f'{output_directory}/{base_name.lower()}.py'

        with open(path, 'w') as writer:
            writer.write('from typing import Any, ForwardRef, Generic, TypeVar\n')
            writer.write('\n')

            for import_type in imports:
                module, import_type = import_type.split(':')

                writer.write(f'from {module.strip()} import {import_type.strip()}\n')
            writer.write('\n\n')

            writer.write('T = TypeVar(\'T\')\n')
            writer.write('\n\n')

            writer.write(f'class {base_name}:\n')
            writer.write('    # Public methods\n')
            writer.write('\n')
            writer.write('    def accept(\n')
            writer.write('        visitor: ForwardRef(\'Visitor[T]\'),\n')
            writer.write('    ) -> T:\n')
            writer.write('        pass\n')
            writer.write('\n\n')

            for type in types:
                class_name, fields = type.split(':')
                GenerateAst.__define_type(
                    writer,
                    base_name,
                    class_name.strip(),
                    fields.strip(),
                )
                writer.write('\n\n')

            GenerateAst.__define_visitor(
                writer,
                base_name,
                types,
            )


    # Private methods

    @staticmethod
    def __define_type(
        writer: IO[AnyStr],
        base_name: str,
        class_name: str,
        field_list: str,
    ) -> None:
        fields = field_list.split(', ')

        writer.write(f'class {base_name}{class_name}({base_name}):\n')
        writer.write('    # Lifecycle methods\n')
        writer.write('\n')
        writer.write('    def __init__(\n')
        writer.write('        self,\n')

        for field in fields:
            type, name = field.split(' ')

            writer.write(f'        {name}: {type},\n')
        writer.write('    ) -> None:\n')

        for field in fields:
            _, name = field.split(' ')

            writer.write(f'        self.{name} = {name}\n')
        writer.write('\n\n')

        writer.write('    # Public methods\n')
        writer.write('\n')

        writer.write('    def accept(\n')
        writer.write('        self,\n')
        writer.write('        visitor: ForwardRef(\'Visitor[T]\'),\n')
        writer.write('    ) -> T:\n')
        writer.write(f'        return visitor.visit_{base_name}{class_name}(self)\n')


    @staticmethod
    def __define_visitor(
        writer: IO[AnyStr],
        base_name: str,
        types: list[str],
    ) -> None:
        writer.write(f'class Visitor(Generic[T]):\n')
        writer.write('    # Public methods\n')
        writer.write('\n')

        for type in types:
            type_name = type.split(':')[0].strip()

            writer.write(f'    def visit_{base_name}{type_name}(\n')
            writer.write('        self,\n')
            writer.write(f'        {base_name.lower()}: {base_name}{type_name},\n')
            writer.write(f'    ) -> T:\n')
            writer.write('        pass\n')
            writer.write('\n\n')


if __name__ == '__main__':
    _, *args = sys.argv

    if len(args) != 1:
        print('Usage generate_ast <output directory>')
        sys.exit(64)
    else:
        output_directory = args[0]

        GenerateAst.define_ast(output_directory, 'Expr',
            [
                'Assign   : Token name, Expr value',
                'Binary   : Expr left, Token operator, Expr right',
                'Call     : Expr callee, Token paren, list[Expr] arguments',
                'Get      : Expr object, Token name',
                'Grouping : Expr expression',
                'Literal  : Any value',
                'Logical  : Expr left, Token operator, Expr right',
                'Set      : Expr object, Token name, Expr value',
                'Super    : Token keyword, Token method',
                'This     : Token keyword',
                'Unary    : Token operator, Expr right',
                'Variable : Token name',
            ],
            [
                'token : Token',
            ],
        )

        GenerateAst.define_ast(output_directory, 'Stmt',
            [
                'Block      : list[Stmt] statements',
                'Class      : Token name, ExprVariable superclass, list[Stmt] methods',
                'Expression : Expr expression',
                'Function   : Token name, list[Token] params, list[Stmt] body',
                'If         : Expr condition, Stmt then_branch, Stmt else_branch',
                'Print      : Expr expression',
                'Return     : Token keyword, Expr value',
                'Var        : Token name, Expr initializer',
                'While      : Expr condition, Stmt body',
            ],
            [
                'expr : Expr, ExprVariable',
                'token : Token',
            ],
        )
