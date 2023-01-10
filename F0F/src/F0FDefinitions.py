import AST_nodes
import time
from F0FErrors import *
class Return_asExc(RuntimeError):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
class Callable:
    def arity(self) -> int:
        pass
    def call(self,interpreter, arguments:list):
        pass
class globals_clock(Callable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter, arguments: list):
        return time.time()

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

class Enviroment:
    def __init__(self,enclosing=None):
        self.enclosing = enclosing
        self.values = {} # [string] = object

    def get(self,name):
        if self.values.get(name.lex):
            return self.values[name.lex]
        if self.enclosing != None:
            return self.enclosing.get(name)
        raise RuntimeF0FError(name,"Undefined variable '" + name.lex + "'.")
    
    def assign(self,name,value):
        if self.values.get(name.lex):
            self.values[name.lex] = value
            return
        if self.enclosing != None:
            self.enclosing.assign(name,value)
            return
        raise RuntimeF0FError(name,"Undefined variable '" + name.lex + "'.")
    
    def define(self,name:str,value):
        self.values[name] = value
    
    def ancestor(self,distance:int):
        env = self
        for i in range(distance):
            env = env.enclosing
        return env
    
    def getAt(self,distance:int,name:str):
        return self.ancestor(distance).values.get(name)
    
    def assignAt(self,distance:int,name,value):
        self.ancestor(distance).values.put(name.lex, value)
