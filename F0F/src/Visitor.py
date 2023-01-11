from AST_nodes import *
from F0FDefinitions import *
from F0FErrors import SemanticError, RuntimeF0FError

class Visitor:
    def visitLiteralExpr(self,expr:Literal):
        pass
    def visitIdentifierExpr(self,expr:Identifier):
        pass
    def visitUnaryExpr(self,expr:UnaryNode):
        pass 
    def visitBinaryExpr(self,expr:BinaryNode):
        pass
    def visitCallExpr(self,expr:Call):
        pass    
    def visitAssignExpr(self,expr:Assignment):
        pass


    def visitVarDeclStmt(self,stmt:VariableDecl):
        pass    
    def visitFunctionStmt(self,stmt:Function):
        pass    
    def visitWhileStmt(self,stmt:While):
        pass   
    def visitForStmt(self,stmt:For):
        pass     
    def visitStmtList(self,stmt:list):
        pass     
    def visitIfStmt(self,stmt:If):
        pass    
    def visitReturnStmt(self,stmt:Return):
        pass    
    def visitPrintStmt(self,stmt:Print):
        pass

class Resolver(Visitor):
    def __init__(self,interpreter):
        self.interpreter:Interpreter = interpreter
        self.scopes = []
        self.current_function = None
    
    def begin(self,ast):
        program = ast.root
        self.begin_scope()
        for stmt in program.declarations:
                # execute it
                self.resolve(stmt)
        self.resolve(program.forge)
        self.end_scope()

    def resolve(self,node):
        node.visit(self)
    
    def begin_scope(self):
        self.scopes.append(dict())
    def end_scope(self):
        self.scopes.pop()
    def declare(self,name:Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[len(self.scopes)-1]
        value = scope.get(name.lex)
        if value != None:
            raise RuntimeF0FError(name, "Variable with this name already declared in this scope.")
        scope[name.lex] = False
    def define(self,name:Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[len(self.scopes)-1]
        scope[name.lex] = True
    def resolve_local(self,expr,name:Token):
        for i in range(len(self.scopes)-1,-1,-1):
            scope = self.scopes[i]
            val = scope.get(name.lex)
            if val != None:
                self.interpreter.resolve(expr,len(self.scopes)-1-i)
                return

    def visitLiteralExpr(self,expr:Literal):
        return None
    def visitIdentifierExpr(self,expr:Identifier):
        self.resolve_local(expr,expr.main_token)
    def visitUnaryExpr(self,expr:UnaryNode):
        for i in range(len(self.scopes)-1,-1,-1):            
            node_solved = self.scopes[i].get(expr.node.main_token.lex)
            if node_solved != None:
                break
        if node_solved == None:
            self.resolve(expr.node)
    def visitBinaryExpr(self,expr:BinaryNode):
        for i in range(len(self.scopes)-1,-1,-1):
            left_solved = self.scopes[i].get(expr.left.main_token.lex)
            if left_solved != None:
                break
        for i in range(len(self.scopes)-1,-1,-1):            
            right_solved = self.scopes[i].get(expr.right.main_token.lex)
            if right_solved != None:
                break
        if left_solved == None:
            self.resolve(expr.left)
        if right_solved == None:
            self.resolve(expr.right)
    def visitCallExpr(self,expr:ParenCall):
        for i in range(len(self.scopes)-1,-1,-1):
            caller_solved = self.scopes[i].get(expr.caller.main_token.lex)
            if caller_solved != None:
                break
        if caller_solved == None:
            self.resolve(expr.caller)
        for arg in expr.arguments:
            self.resolve(arg)
    def visitAssignExpr(self,expr:Assignment):
        self.resolve(expr.right)
        self.resolve_local(expr, expr.left.main_token)


    def visitVarDeclStmt(self,stmt:VariableDecl):
        self.declare(stmt.name.main_token)
        if stmt.initializer != None:
            self.resolve(stmt.initializer)
        self.define(stmt.name.main_token)
    def visitFunctionStmt(self,stmt:Function):
        enclosing_function = self.current_function
        self.current_function = 'function'
        self.declare(stmt.name.main_token)
        self.define(stmt.name.main_token)

        self.begin_scope()
        for p in stmt.parameters:
            self.declare(p.main_token)
            self.define(p.main_token)
        self.visitStmtList(stmt.body)
        self.end_scope()
        self.current_function = enclosing_function
    def visitWhileStmt(self,stmt:While):
        self.resolve(stmt.condition)
        self.visitStmtList(stmt.body)
    def visitForStmt(self,stmt:For):
        self.resolve(stmt.initializer)
        self.resolve(stmt.loop)
    def visitStmtList(self,stmt:list):
        for s in stmt:
            self.resolve(s)
    def visitIfStmt(self,stmt:If):
        self.resolve(stmt.condition)
        self.visitStmtList(stmt.body)
        if stmt.else_branch != None:
            self.visitStmtList(stmt.else_branch.body)
    def visitReturnStmt(self,stmt:Return):
        if self.current_function == None:
            raise RuntimeF0FError(stmt.main_token,"Cannot return from top-level code.")
        if stmt.expression != None:
            self.resolve(stmt.expression)
    def visitPrintStmt(self,stmt:Print):
        self.resolve(stmt.expression)

class Interpreter(Visitor):
    def __init__(self):
        super().__init__()
        self.had_semantic_error = False
        self.had_runtime_error = False
        self.locals  = {} # [Node] = depth
        self.globals = Enviroment()
        self.enviroment = self.globals
        self.globals.define('clock',globals_clock())

    def interpret(self, program:Program):
        # try:
            for stmt in program.declarations:
                # execute it
                stmt.visit(self)
            program.forge.visit(self)
            forge = self.enviroment.getAt(0,'Forge')
            forge.call(self,[None,-1000,1000])
        # except Exception as error:
        #     print(error)

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
    def resolve(self,expr:Node,depth:int):
        self.locals[expr] = depth

    def visitLiteralExpr(self,expr:Literal):
        return expr.value
    def visitIdentifierExpr(self,expr:Identifier):
        # distance = self.locals.get(expr)
        try:
            return self.enviroment.get(expr.main_token)
        except:
            return self.globals.get(expr.main_token)
        
        # return expr.name
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
        if isinstance(expr.caller,Identifier):
            caller = self.enviroment.get(expr.caller.main_token)
        else: print(type(expr.caller))
        # return caller.call(self,evaluated_args)
        evaluated_args = []
        for arg in expr.arguments:
            evaluated_args.append(self.evaluate(arg))
        if isinstance(caller,Callable):
            caller:Callable
            if len(evaluated_args)!=caller.arity():
                error = RuntimeF0FError(expr.main_token, "Expected " + caller.arity() + " arguments, but got " + len(evaluated_args) + ".")
                self.had_runtime_error = True
                raise error
            else:
                return caller.call(self,evaluated_args)
        else:
            error = RuntimeF0FError(expr.main_token,"This object it\'s not callable.")
            self.had_runtime_error = True
            raise error

    def visitAssignExpr(self,expr:Assignment):
        value = self.evaluate(expr.right)
        distance = self.locals.get(expr)
        if distance is None:
            self.globals.assign(expr.left.main_token,value)
        else:
            self.enviroment.assign(expr.left.main_token,value)
        return value

    def visitVarDeclStmt(self,stmt:VariableDecl):
        value = None
        if stmt.initialized():
            value = self.evaluate(stmt.initializer)
        self.enviroment.define(stmt.name.lex, value)
    def visitFunctionStmt(self,stmt:Function):
        funct = F0FFunctions(stmt,self.enviroment)
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
            if stmt.else_branch == None:
                return
            stmt.else_branch.visit(self)
    def visitReturnStmt(self,stmt:Return):
        if stmt.expression != None:
            value = self.evaluate(stmt.expression)
        raise Return_asExc(value)
    def visitPrintStmt(self,stmt:Print):
        value = self.evaluate(stmt.expression)
        strn = str(value)
        if isinstance(value,float):
            if strn.endswith('.0'):
                strn = strn[:len(strn)-2]
        print(strn)

