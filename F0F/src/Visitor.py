from AST_nodes import *
from F0FDefinitions import *
from F0FErrors import SemanticError, RuntimeF0FError

class Visitor:
    def visitLiteralExpr(expr:Literal):
        pass
    def visitTypeExpr(expr:Type):
        pass
    def visitIdentifierExpr(expr:Identifier):
        pass
    def visitVariableExpr(expr:Variable):
        pass   
    def visitUnaryExpr(expr:UnaryNode):
        pass 
    def visitBinaryExpr(expr:BinaryNode):
        pass
    def visitCallExpr(expr:Call):
        pass    
    def visitAssignExpr(expr:Assignment):
        pass


    def visitVarDeclStmt(stmt:Variable):
        pass    
    def visitFunctionStmt(stmt:Function):
        pass    
    def visitWhileStmt(stmt:While):
        pass   
    def visitForStmt(stmt:For):
        pass     
    def visitStmtList(stmt:list):
        pass     
    def visitIfStmt(stmt:If):
        pass    
    def visitReturnStmt(stmt:Return):
        pass    

class Interpreter(Visitor):
    def __init__(self):
        super().__init__()
        self.had_semantic_error = False
        self.had_runtime_error = False
        self.locals  = {} # [Node] = depth
        self.globals = None
        self.enviroment = None
    def interpret(self, program:Program):
        try:
            for stmt in program.declarations:
                # execute it
                stmt.visit(self)
            program.forge.visit(self)
        except:
            pass

    def evaluate(self,expr:Node):
        return expr.visit(self)
    def executeBlock(self,statements:list,enviroment):
        previous = self.enviroment
        try: 
            self.enviroment = enviroment
            for stmt in statements:
                # execute it
                stmt.visit(self)
        finally:
            self.enviroment = previous


    def visitLiteralExpr(self,expr:Literal):
        return expr.value
    def visitIdentifierExpr(self,expr:Identifier):
        return expr.name
    def visitVariableExpr(self,expr:Variable):
        distance = self.locals.get(expr)
        if distance is None:
            return self.globals.get(expr.name)
        else:
            return self.enviroment.getAt(distance,expr.name.lex)
    def visitUnaryExpr(self,expr:UnaryNode):
        value = self.evaluate(expr.node)
        if expr is Logic_NOT:
            if type(value) != bool:
                error = SemanticError(expr.main_token,'Invalid ! operation with a non boolean value.')
                expr.semantic_errors.append(error)
                self.had_semantic_error = True
                raise error
        elif expr is Negate:
            try: 
                value = float(value)
            except:
                error = SemanticError(expr.main_token,'Invalid negate operation with a non numeric value.')
                expr.semantic_errors.append(error) 
                self.had_semantic_error = True
                raise error
        return expr.operate(value)
    def visitBinaryExpr(self,expr:BinaryNode):
        lvalue = self.evaluate(expr.left)
        rvalue = self.evaluate(expr.right)
        if expr is Eql:
            return expr.operate(lvalue,rvalue)
        if expr is Logic_AND or expr is Logic_OR:
            try:
                lvalue = Bool(lvalue)
                rvalue = Bool(rvalue)
                return expr.operate(lvalue, rvalue)
            except:
                error = SemanticError(expr.main_token,'Operands must be boolean expressions.')
                expr.semantic_errors.append(error) 
                self.had_semantic_error = True
                raise error
        else:
            try:
                lvalue = float(lvalue)
                rvalue = float(rvalue)
            except:
                error = SemanticError(expr.main_token,'Operands must be numbers.')
                expr.semantic_errors.append(error) 
                self.had_semantic_error = True
                raise error

            if expr is Div or expr is Module:
                if rvalue == 0:
                    error = RuntimeF0FError(expr.main_token,'Zero division error.')
                    # expr.semantic_errors.append(error) 
                    self.had_runtime_error = True
                    raise error

        return expr.operate(lvalue,rvalue)
    def visitCallExpr(self,expr:Call):
        caller = self.evaluate(expr.caller)
        evaluated_args = []
        for arg in expr.arguments:
            evaluated_args.append(self.evaluate(arg))
        if caller is Callable:
            caller:Callable
            if len(evaluated_args)!=caller.arity():
                error = RuntimeF0FError(expr.main_token, "Expected " + caller.arity() + " arguments, but got " + len(evaluated_args) + ".")
                self.had_runtime_error = True
                raise error
            else:
                return caller.call(self,evaluated_args)
        else:
            error = RuntimeF0FError(expr.main_token,"This object its not callable.")
            self.had_runtime_error = True
            raise error

    def visitAssignExpr(self,expr:Assignment):
        value = self.evaluate(expr.right)
        distance = self.locals.get(expr)
        if distance is None:
            self.globals.assign(expr.left,value)
        else:
            self.enviroment.assignAt(distance,expr.left,value)
        return value

    def visitVarDeclStmt(self,stmt:VariableDecl):
        if stmt.initialized():
            value = self.evaluate(stmt.initializer)
        self.enviroment.define(stmt.var.name.lex, value)
    def visitFunctionStmt(self,stmt:Function):
        funct = F0FFunctions(stmt,self.enviroment,False)
        self.enviroment.define(stmt.name.lex, funct)
    def visitWhileStmt(self,stmt:While):
        cond = self.evaluate(stmt.condition)
        while cond:
            self.visitStmtList(stmt.body)
            cond = self.evaluate(stmt.condition)
    def visitForStmt(self,stmt:For):
        self.visitVarDeclStmt(stmt.initializer)
        cond = self.evaluate(stmt.loop.condition)
        while cond:
            self.visitStmtList(stmt.loop.body)
            cond = self.evaluate(stmt.loop.condition)
    def visitStmtList(self,stmts:list):
        self.executeBlock(stmts,Enviroment(self.enviroment))
    def visitIfStmt(self,stmt:If):
        cond = self.evaluate(stmt.condition)
        if cond:
            self.visitStmtList(stmt.body)
        else:
            stmt.else_branch.visit(self)
    def visitReturnStmt(self,stmt:Return):
        if stmt.expression != None:
            value = self.evaluate(stmt.expression)
        raise Return_asExc(value)