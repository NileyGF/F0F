from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens

class Node:
    def evaluate(self):
        raise NotImplementedError()

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

class Expr:
    pass

class Bool(AtomicNode):
    # primary -> true 
    # primary -> false
    def __init__(self, lex:str):
        if lex == 'true' or lex == 'false':
            if lex == 'true':
                self.value = True
            elif lex == 'false':
                self.value = False
            super().__init__(lex)
        else: print('semantic error')

    def evaluate(self):
        return self.value
    pass
class Num(AtomicNode):
    def __init__(self, lex:str):
        self.value = float(lex)
        super().__init__(lex)    

    def evaluate(self):
        return self.value
    pass
class Integer(Num):
    def __init__(self, lex: str):
        super().__init__(lex)
        try:
            self.value = int(lex)
        except:
            print('semantic error')
    pass
class Decimal(Num):
    def __init__(self, lex: str):
        super().__init__(lex)
        try:
            self.value = float(lex)
        except:
            print('semantic error')
    pass
class String_chain(AtomicNode):
    def __init__(self, lex:str):
        super().__init__(lex)
        try:
            self.value = str(lex)
        except:
            print('semantic error') 
        
    def evaluate(self):
        return self.value
    pass

class Logic_NOT(UnaryNode):
    def __init__(self, node:Node):
        super().__init__(node)
        
    @staticmethod
    def operate(value):
        return not value
    pass
class Negate(UnaryNode):
    def __init__(self, node:Num):
        super().__init__(node)
        
    @staticmethod
    def operate(value):
        return  0 - value
    pass

class Factor(BinaryNode):
    def __init__(self, left:Node, right:Node):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            print('semantic error') 
    pass
class Mult(Factor):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue * rvalue
    pass
class Div(Factor):
    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            if rvalue == 0:
                print('zero division error') 
                return
            return self.operate(lvalue, rvalue)
        except:
            print('semantic error') 

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
                print('zero division error') 
                return
            return self.operate(lvalue, rvalue)
        except:
            print('semantic error') 

    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue % rvalue    
    pass
class Pow(Expr,BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue ** rvalue
    pass

class Term(Expr,BinaryNode):
    def __init__(self, left:Node, right:Node):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = float(lvalue)
            rvalue = float(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            print('semantic error') 
    pass
class Sum(Term):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue + rvalue
    pass
class Minus(Term):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue - rvalue
    pass

class Comparison(Expr,BinaryNode):
    def __init__(self, left:Node, right:Node):
        self.left = left
        self.right = right
    pass
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

class Eql(Expr,BinaryNode):
    def __init__(self, left:Node, right:Node):
        self.left = left
        self.right = right
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

class Logic_OR(Expr,BinaryNode):
    def __init__(self, left:Node, right:Node):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = Bool(lvalue)
            rvalue = Bool(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            print('semantic error') 
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue or rvalue
    pass
class Logic_AND(Expr,BinaryNode):
    def __init__(self, left:Node, right:Node):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        try:
            lvalue = Bool(lvalue)
            rvalue = Bool(rvalue)
            return self.operate(lvalue, rvalue)
        except:
            print('semantic error') 
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue and rvalue
    pass


class Assignment(Expr):
    """
        assignment -> call id = assignment
        assignment -> id = assignment
        assignment -> logic_or
    """
    pass


class Declaration:
    """ 
        declaration -> class_decl
        declaration -> funct_decl
        declaration -> var_decl
        declaration -> statement
    """
    pass

class Class(Declaration):
    """ class_decl -> class id { funct_list } """
    def __init__(self, id:TerminalsTokens, function_list:list ):
        super().__init__()
        self.name = id
        self.methods = function_list

class Function(Declaration):
    """ funct_decl -> fun id ( parameters ) block """
    def __init__(self, id:TerminalsTokens, parameters_list:list, body:list):
        super().__init__()
        self.name = id
        self.parameters = parameters_list
        self.body = body

class Variable(Declaration):
    """
        var_decl -> type id var_value
        var_value -> = expression ;
        var_value -> ;  
    """
    def __init__(self, type:TerminalsTokens, id:TerminalsTokens, initializer:Expr):
        super().__init__()
        self.name = id
        self.type = type
        self.initializer = initializer

class Statement:
    """
        statement -> expression ;
        statement -> for_statement
        statement -> while_statement
        statement -> if_statement
        statement -> print_statement8
        statement -> return_statement
        statement -> block 
    """
    pass

class Expression(Statement):
    def __init__(self, expression:Expr):
        super().__init__()
        self.expression = expression

class For(Statement):
    """
        for_statement -> for ( for_first expression ; expression ) statement
        for_first -> var_decl 
        for_first -> expression ; 
    """
    def __init__(self):
        super().__init__()

class While(Statement):
    """ while_statement -> while ( expression ) statement """
    def __init__(self, condition:Expr, body:Statement):
        super().__init__() 
        self.condition = condition
        self.body = body

class If(Statement):
    """
        if_statement -> if ( expression ) statement else_stmt
        else_stmt -> else statement
        else_stmt -> epsilon
    """
    def __init__(self, condition:Expr, body:Statement, else_branch:Statement):
        super().__init__()
        self.condition = condition
        self.body = body
        self.else_branch = else_branch

class Print(Statement):
    """ print_statement -> print expression ; """
    def __init__(self, expression:Expr):
        super().__init__()
        self.expression = expression

class Return(Statement):
    """
        return_statement -> return ret
        ret -> expression ;
        ret -> ;
    """
    def __init__(self, expression:Expr):
        super().__init__()
        self.expression = expression

class Block(Statement):
    """
        block -> { block_body }
        block_body -> declaration_list
        block_body -> epsilon
    """
    def __init__(self, declaration_list:list):
        super().__init__()
        self.declaration_list = declaration_list

class AST():
    def __init__(self):
        pass

    def ast_from_parse_tree(parse_tree_root):

        pass
