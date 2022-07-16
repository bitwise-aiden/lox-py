from typing import ForwardRef

from .velox_function import VeloxFunction
from velox_callable import VeloxCallable
from velox_instance import VeloxInstance


class VeloxClass(VeloxCallable):
    # Lifecycle methods

    def __init__(
        self,
        name: str,
        superclass: ForwardRef('VeloxClass'),
        methods: dict[str, VeloxFunction]
    ) -> None:
        self.name = name
        self.__superclass = superclass
        self.__methods = methods


    def __str__(
        self,
    ) -> str:
        return self.name


    # Public methods

    def arity(
        self,
    ) -> int:
        initializer = self.find_method('init')

        if initializer == None:
            return 0

        return initializer.arity()



    def call(
        self,
        interpreter: ForwardRef('Interpreter'),
        arguments: list, # TODO
    ): # TODO
        instance = VeloxInstance(self)

        initializer = self.find_method('init')

        if initializer != None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance


    def find_method(
        self,
        name: str,
    ) -> VeloxFunction:
        if name in self.__methods:
            return self.__methods[name]

        if self.__superclass != None:
            return self.__superclass.find_method(name)
