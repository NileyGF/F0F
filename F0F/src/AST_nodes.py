from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens
from F0FGrammar import Terminal, NonTerminal, Production, Sentential_Form, Symbol, EOF, Epsilon
from F0FErrors import SemanticError
from F0FParser import PT_node,Parse_Tree
import Visitor

class Node:
    def __init__(self) -> None:
        self.semantic_errors =[]

    def evaluate(self):
        raise NotImplementedError()

class AtomicNode(Node):
    def __init__(self,token:Token):
        super().__init__()
        self.lex = token.lex
class UnaryNode(Node):
    def __init__(self, node:Node):
        super().__init__()
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()
class BinaryNode(Node):
    def __init__(self, left:Node, right:Node):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

class Literal(AtomicNode):
    def evaluate(self):
        return self.value
class NULL(Literal):
    def __init__(self,token:Token):
        super().__init__(token)
        self.value = None
class Bool(Literal):
    # primary -> true 
    # primary -> false
    pass
class TRUE(Bool):
    def __init__(self,token:Token):
        super().__init__(token)
        self.value = True
class FALSE(Bool):
    def __init__(self,token:Token):
        super().__init__(token)
        self.value = False

class Num(Literal):
    pass
class Integer(Num):
    def __init__(self,token:Token):
        super().__init__(token)
        try:
            self.value = int(token.lex)
        except:
            error = SemanticError(token.line,'The value is not an integer.')
            print(error)
            self.semantic_errors.append(error)
class Decimal(Num):
    def __init__(self,token:Token):
        super().__init__(token)
        try:
            self.value = float(token.lex)
        except:            
            error = SemanticError(token.line,'The value is not numeric.')
            print(error)
            self.semantic_errors.append(error)

class String_chain(Literal):
    def __init__(self, token: Token):
        super().__init__(token)
        try:
            self.value = str(token.lex)
        except:            
            error = SemanticError(token.line,'The value is not a string.')
            print(error)
            self.semantic_errors.append(error)

class Type(Node):
    pass
class INT(Type):
    def __init__(self):
        super().__init__()
class DOUBLE(Type):
    def __init__(self):
        super().__init__()
class VOID(Type):
    def __init__(self):
        super().__init__()
class BOOL(Type):
    def __init__(self):
        super().__init__()
class STRING(Type):
    def __init__(self):
        super().__init__()
class MFUN(Type):
    def __init__(self):
        super().__init__()
class POINT(Type):
    def __init__(self):
        super().__init__()

class Identifier(AtomicNode):
    def __init__(self, token:Token):
        super().__init__(token)
        self.name=token.lex
    def evaluate(self):
        return self.name


class Variable(Node):
    def __init__(self, type:Type, id:Identifier):
        self.type = type
        self.name = id

# class Expr(Node):
#     """ expression -> call = expression
#         expression -> operation
#     """    
#     pass



# class Argument(Expr):
#     def __init__(self,expression:Expr):
#             self.expression = expression
#     def accept(self,visitor: Visitor):
#         return visitor.visitUnaryExpr(self)
#     def evaluate(self):
#         return self.expression.evaluate()

# class Parameter(Node):
#     def __init__(self,var:Variable):
#             self.variable = var
#     def accept(self,visitor: Visitor):
#         return visitor.visitVariableExpr(self)
#     def evaluate(self):
#         return self.variable.evaluate()



class Logic_NOT(UnaryNode):
    def __init__(self, node:Node):
        super().__init__(node)
    def evaluate(self):
        value = self.node.evaluate()
        try:
            value = bool(value)
            return self.operate(value)
        except:
            error = SemanticError('Invalid ! operation with a non boolean value.')
            print(error)
            self.semantic_errors.append(error) 
    @staticmethod
    def operate(value):
        return not value
class Negate(UnaryNode):
    def __init__(self, node:Node):
        super().__init__(node)
    def evaluate(self):
        value = self.node.evaluate()
        try:
            value = float(value)
            return self.operate(value)
        except:
            error = SemanticError('Invalid negate operation with a non numeric value.')
            print(error)
            self.semantic_errors.append(error) 
    @staticmethod
    def operate(value):
        return  0 - value
    pass

class Factor(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)
class Mult(Factor):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue * rvalue
    
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Product operands must be numbers.')
            print(error)
            self.semantic_errors.append(error) 
class Div(Factor):
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            if rvalue == 0:
                error = SemanticError('Zero division error.')
                print(error)
                self.semantic_errors.append(error) 
                return
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Division operands must be numbers..')
            print(error)
            self.semantic_errors.append(error) 

    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue / rvalue
    pass
class Module(Factor):
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            if rvalue == 0:
                error = SemanticError('Zero division error.')
                print(error)
                self.semantic_errors.append(error) 
                return
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Module operands must be numbers.')
            print(error)
            self.semantic_errors.append(error) 

    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue % rvalue    
    pass

class Pow(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Power(^) operands must be numbers..')
            print(error)
            self.semantic_errors.append(error) 

    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue ** rvalue
    pass

class Term(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)
    pass
class Sum(Term):
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Invalid sum operation.')
            print(error)
            self.semantic_errors.append(error) 
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue + rvalue
    pass
class Minus(Term):
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Substraction operands must be numbers.')
            print(error)
            self.semantic_errors.append(error) 
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue - rvalue
    pass

class Comparison(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Comparison operands must be numbers.')
            print(error)
            self.semantic_errors.append(error) 
class Less(Comparison):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue < rvalue
    pass
class Less_Equal(Comparison):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue <= rvalue
    pass
class Greater(Comparison):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue > rvalue
    pass
class Greater_Equal(Comparison):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue >= rvalue
    pass

class Eql(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)
    pass
class Equality(Eql):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue == rvalue
    pass
class Unequality(Eql):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue != rvalue
    pass

class Logic_OR(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = Bool(lvalue)
            rvalue = Bool(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Invalid || operation')
            print(error)
            self.semantic_errors.append(error)
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue or rvalue
class Logic_AND(BinaryNode):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right)

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = Bool(lvalue)
            rvalue = Bool(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            error = SemanticError('Invalid && operation')
            print(error)
            self.semantic_errors.append(error)
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue and rvalue

class Call(Node):
    """
        call -> primary call_type 
        call_type -> . id call_type
        call_type -> [ expression ] call_type
        call_type -> ( arguments ) call_type
        call_type -> epsilon
    """
    def __init__(self,caller):
        self.caller = caller
    def accept(self, visitor: Visitor):
        return visitor.visitCallExpr(self)
    pass
class DotCall(Call):
    """ call_type -> . id call_type """
    def __init__(self,caller,property):
        super().__init__(caller)
        self.property = property
class ParenCall(Call):
    """ call_type -> ( arguments ) call_type """
    def __init__(self, caller,args:list):
        super().__init__(caller)
        self.arguments = args

class Assignment(Node):
    """
        expression -> call = expression
    """
    def __init__(self,call:Call,expression:Node):
        super().__init__()
        self.left = call
        self.right = expression
    def accept(self,visitor: Visitor):
        return visitor.visitAssignExpr(self)
    pass
class Statement(Node):
    """
        statement -> expression ;
        statement -> for_statement
        statement -> while_statement
        statement -> if_statement
        statement -> return_statement
    """
    pass
class ExpressionStmt(Statement):
    """ statement -> expression ; """
    def __init__(self,expression:Expr):
        self.expression = expression
    def accept(self, visitor: Visitor):
        return visitor.visitExpressionStmt

class VariableDecl(Statement):
    """
        var_decl -> type id var_value
        var_value -> = expression ;
        var_value -> ;   
    """
    def __init__(self, var:Variable, initializer:Node=None):
        super().__init__()
        self.var = var
        self.initializer = initializer
    def initialized(self):
        return (self.initializer == None)
    def accept(self, visitor: Visitor):
        return visitor.visitVarStmt(self)

class Function(Statement):
    """ funct_decl -> fun type id ( parameters ) { statement_list } """
    def __init__(self,type:Type, id:Identifier, parameters_list:list, body:list):
        super().__init__()
        self.type = type
        self.name = id
        self.parameters = parameters_list
        self.body = body
    def accept(self, visitor: Visitor):
        return visitor.visitFunctionStmt(self)
class Forge(Function):
    """ F0F -> Forge ( parameters ) { statement_list } """
    def __init__(self,forge:Token, parameters_list: list, body: list):
        super().__init__(POINT(), Identifier(forge), parameters_list, body)

class While(Statement):
    """ while_statement -> while ( expression ) { statement_list } """
    def __init__(self, condition:Node, body:list):
        super().__init__()
        self.condition = condition
        self.body = body
    def accept(self, visitor: Visitor):
        return visitor.visitWhileStmt(self)
class For(Statement):
    def __init__(self,initializer:VariableDecl, loop:While):
        super().__init__()
        self.initializer = initializer
        self.loop = loop
class Else(Statement):
    """
        else_stmt -> else { statement_list }
    """
    def __init__(self, body:list):
        self.body = body
    def accept(self, visitor: Visitor):
        return visitor.visitIfStmt(self)
class If(Statement):
    """
        if_statement -> if ( expression ) { statement_list } else_stmt
    """
    def __init__(self, condition:Node, body:list, else_branch:Else=None):
        super().__init__()
        self.condition = condition
        self.body = body
        self.else_branch = else_branch
    def accept(self, visitor: Visitor):
        return visitor.visitIfStmt(self)
class Return(Statement):
    """
        return_statement -> return ret
        ret -> expression ;
        ret -> ;
    """
    def __init__(self, expression:Node=None):
        super().__init__()
        self.expression = expression
    def accept(self, visitor: Visitor):
        return visitor.visitReturnStmt(self)

class Program(Node):
    def __init__(self, declarations:list, forge:Forge):
        super().__init__()
        self.declarations = declarations
        self.forge = forge
    def evaluate(self):
        return super().evaluate()
    
# class StatementList(Node):
#     """
#         statement_list -> var_decl statement_list
#         statement_list -> statement statement_list
#         statement_list -> epsilon
#     """
#     def __init__(self,list:list):
#         self.list = list



class Visitor:
    def  visitAssignExpr(expr:Assignment):
        pass
    def  visitBinaryExpr(expr:BinaryNode):
        pass
    def  visitCallExpr(expr:Call):
        pass
    def  visitLiteralExpr(expr:Literal):
        pass
    def  visitUnaryExpr(expr:UnaryNode):
        pass
    def  visitVariableExpr(expr:Variable):
        pass    


    def visitExpressionStmt(stmt:ExpressionStmt):
        pass    
    def visitFunctionStmt(stmt:Function):
        pass    
    def visitIfStmt(stmt:If):
        pass    
    def visitReturnStmt(stmt:Return):
        pass    
    def visitVarStmt(stmt:Variable):
        pass    
    def visitWhileStmt(stmt:While):
        pass    
    pass

