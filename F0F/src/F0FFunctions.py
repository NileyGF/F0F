import AST_nodes
class Return_asExc(RuntimeError):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
class Callable:
    def arity(self) -> int:
        pass
    def call(self,interpreter, arguments:list):
        pass

class F0FFunctions(Callable):
    def __init__(self,declaration:AST_nodes.Function,closure, isInitializer):
        super().__init__()
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer
    def arity(self) -> int:
        return len(self.declaration.parameters)
    def call(self, interpreter, arguments: list):
        return super().call(arguments)
