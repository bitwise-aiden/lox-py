import sys


class GenerateAst:
    @staticmethod
    def define_ast(
        output_directory: str,
        base_name: str,
        types: list[str]
    ) -> None:
        path = f'{output_directory}/{base_name.lower()}.py'

        with open(path, 'w') as writer:
            writer.write('from typing import Any, ForwardRef, Generic, TypeVar\n')
            writer.write('\n')

            writer.write('from token import Token\n')
            writer.write('\n\n')

            writer.write('T = TypeVar(\'T\')\n')
            writer.write('\n\n')

            writer.write(f'class {base_name}:\n')
            writer.write('    def accept(visitor: ForwardRef("Visitor[T]")) -> T:\n')
            writer.write('        pass\n')
            writer.write('\n\n')

            for type in types:
                class_name, fields = type.split(':')
                GenerateAst.define_type(
                    writer,
                    base_name,
                    class_name.strip(),
                    fields.strip(),
                )
                writer.write('\n\n')

            GenerateAst.define_visitor(
                writer,
                base_name,
                types,
            )

    @staticmethod
    def define_type(
        writer,
        base_name: str,
        class_name: str,
        field_list: str
    ) -> None:
        fields = field_list.split(', ')

        writer.write(f'class {base_name}{class_name}({base_name}):\n')

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

        writer.write('    def accept(self, visitor: ForwardRef("Visitor[T]")) -> T:\n')
        writer.write(f'        return visitor.visit_{base_name}{class_name}(self)\n')

    @staticmethod
    def define_visitor(
        writer,
        base_name: str,
        types: list[str],
    ) -> None:
        writer.write(f'class Visitor(Generic[T]):\n')

        for type in types:
            type_name = type.split(':')[0].strip()

            writer.write(f'    def visit_{base_name}{type_name}(\n')
            writer.write('        self,\n')
            writer.write(f'        {base_name.lower()}: {base_name}{type_name}\n')
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

        GenerateAst.define_ast(output_directory, 'Expr', [
            'Binary   : Expr left, Token operator, Expr right',
            'Grouping : Expr expression',
            'Literal  : Any value',
            'Unary    : Token operator, Expr right',
        ])