from F0FTokens import Token,TerminalsTokens
from F0FGrammar import Terminal, NonTerminal, Production, Symbol,Epsilon, Grammar, F0F
from F0FErrors import ParsingError
from Parser_Generators import First, Follow, LL_1_parsing_table
import pickle

class PT_node:
    def __init__(self, symbol:Symbol, children:list = None):
        self.symbol = symbol
        self.children = children
        if children == None:
            self.children = []

    def is_leaf(self):
        return self.children == None or len(self.children) <= 0
    
    def add_child(self, child:Symbol):
        added_child = PT_node(child)
        self.children.append(added_child)
        return added_child

    def __repr__(self):
        return  self.__str__()
    def __str__(self):
        return str(self.symbol)
    def __iter__(self):
        return iter(self.children)

class Parse_Tree:
    def __init__(self, root:PT_node = None):
        self.root = root
        if root:
            self.initialized = True
        else: 
            self.initialized = False

    def pt_node_from_Prod(Prod:list,prod_ind:int,tokens:list,tok_ind:int):
        prod:Production = Prod[prod_ind]
        head = prod.Head
        children = []
        for b in prod.Body:
            if type(b) is Terminal:
                if b.token_type == tokens[tok_ind].token_type:
                    children.append(PT_node(Symbol(token=tokens[tok_ind])))
                    tok_ind += 1
                else: 
                    print('nop')
                    raise Exception()
            elif b.IsEpsilon:
                children.append(PT_node(Epsilon()))
            else:
                child, tok_ind,prod_ind = Parse_Tree.pt_node_from_Prod(Prod,prod_ind+1,tokens,tok_ind)
                children.append(child)
        return PT_node(head,children), tok_ind, prod_ind 

    def parse_tree_from_prod_list(self,Prod:list,tokens):
        prod_ind = 0
        tok_ind = 0
        current_nt = []
        pr: Production = Prod[0]        
        self.root = Parse_Tree.pt_node_from_Prod(Prod,0,tokens,0) [0]
        # while prod_ind < len(Prod) and tok_ind < len(tokens):
        #     head = Prod[prod_ind].Head
        #     if prod_ind == 0:
        #         self.root = PT_node(head)
        #         head_node = self.root
        #     else:
        #         head_node = current_nt.pop()
        #         if head_node.symbol.token_type != head.token_type:
        #             print('why')
        #     local_children = []


        # pr: Production = Prod[ind].Head
        # self.root = PT_node(pr)
        # current_nt = []
        # # current_nt.append(self.root)
        # for b in Prod[ind].Body:
        #     child = self.root.add_child(b)
        #     if type(b) is NonTerminal:
        #         current_nt.append(child)
            
        # ind += 1
        # while ind < len(Prod):
        #     pr = Prod[ind]
        #     for k in range(len(current_nt)):
        #         if current_nt[k].symbol == pr.Head:
        #             break
        #     # if pr.Head != current_nt[0].symbol:
        #     #     print('not working')
        #     #     return
        #     for b in Prod[ind].Body:
        #         # if type(b) is Terminal:

        #         child = current_nt[k].add_child(b)
        #         current_nt.append(child)
        #     current_nt.remove(current_nt[k])
        #     ind += 1


    def __repr__(self,node = None , level=0):
        if not node: 
            node = self.root
            ret = str(node) + "\n"
        else:
            ret = '|' + '  '*level + "|_ " + str(node) + "\n"
        if node.children == None: 
            return ret
        for child in node.children:
            ret += self.__repr__(child, level+1)
        return ret

    # def reduce_tree()
class F0FParser:
    def __init__(self,tokens:list):
        self.lexer_tokens = tokens
        self.lookahead = None
        self.cursor = -1
        self.had_error = False
        self.parser_errors = []
        self.left_parse = None
     
    def begin(self):
        """
        Begin parsing from starting symbol and match EOF.
        """
        raise NotImplementedError()

    def synchronize(self,cursor=None):
        if cursor is None: cursor = self.cursor
        cursor += 1
        synch = [TerminalsTokens.function, TerminalsTokens.var, TerminalsTokens.For, TerminalsTokens.Forge,
                TerminalsTokens.If, TerminalsTokens.While, TerminalsTokens.Return]
        while not self.end_file():
            if self.lexer_tokens[cursor].token_type == TerminalsTokens.semicolon:
                return cursor
            if self.peek().token_type in synch:
                return cursor
            cursor += 1
        return cursor

    def error(self,token, msg):
        """
        Raises a parsing error.
        """
        self.had_error = True
        self.parser_errors.append(ParsingError(token,msg))
        return self.synchronize()

    def match(self,token_type):
        """
        Consumes one token from the lexer if lookahead matches the given token type.
        Raises parsing error otherwise.
        """
        if token_type == self.lookahead:
            try:
                self.lookahead = self.lexer_tokens[self.cursor]
                self.cursor+=1
            except AttributeError:
                self.lookahead = None
            return True
        else:
            return False
    def end_file(self):
        return self.cursor >= len(self.lexer_tokens)    
    def peek(self):
        """ returns current token """
        return self.lexer_tokens[self.cursor]

class LL1_Parser(F0FParser):
    def __init__(self, grammar:Grammar):      
        self.G = grammar
        self.firsts = First(self.G )
        self.follows = Follow(self.G , self.firsts)
        self.P_table = LL_1_parsing_table(self.G, self.firsts, self.follows)
        self.lexer_tokens = None
        self.lookahead = None
        self.cursor = -1
        self.had_error = False
        self.parser_errors = []
        self.left_parse = None
    
    def begin(self, tokens: list):
        self.lexer_tokens = tokens
        if self.lexer_tokens[len(self.lexer_tokens) - 1] != self.G.EOF:
            self.lexer_tokens.append(self.G.EOF)
        self.cursor = 0
        stack = [self.G.EOF, self.G.mainSymbol]
        self.left_parse = []
        
        ok, self.left_parse,_ = self.branching_parser(stack,self.cursor,self.left_parse)
        self.had_error = not ok

    def branching_parser(self,stack:list,cursor:int,left_parse:list,trying_prod:Production=None):
        if trying_prod != None:
            left_parse.append(trying_prod)
            if not trying_prod.Body.IsEpsilon:
                alpha = trying_prod.Body
                for i in range(len(alpha)-1,-1,-1):
                    stack.append(alpha[i])
        
        while len(stack) > 0:
            top:Symbol = stack.pop()            
            term:Token = self.lexer_tokens[cursor]
            if top.token_type.name == term.token_type.name:
                cursor+=1
            else:
                prod = self.P_table.get((top.token_type.name,term.token_type.name))
                if not prod:
                    if trying_prod is None:
                        cursor = self.error(self.lexer_tokens[cursor],"Un",cursor)
                    return False, left_parse, self.lexer_tokens[cursor]
                if type(prod) is Production:
                    prod:Production
                    left_parse.append(prod)
                    if not prod.Body.IsEpsilon:
                        alpha = prod.Body
                        for i in range(len(alpha)-1,-1,-1):
                            stack.append(alpha[i])
                elif type(prod) is list:
                    boolean_mask = [False] * len(prod)
                    tentative_output = [None] * len(prod)
                    for i in range(len(prod)):
                        b, output, problem = self.branching_parser(stack.copy(),cursor,left_parse.copy(),prod[i])
                        boolean_mask[i] = b
                        tentative_output[i] = output
                    right = 0
                    ind = -1
                    for i in range(len(boolean_mask)):
                        if boolean_mask[i]: 
                            ind = i
                            right += 1
                    if right == 1:
                        left_parse = tentative_output[ind]
                        return True, left_parse, None
                    else:
                        if trying_prod is None:
                            if problem is None: problem = self.lexer_tokens[cursor]
                            self.error(problem,"Unexpected token.",cursor)
                        return False, left_parse, problem

                else:
                    if trying_prod is None:
                        self.error(self.lexer_tokens[cursor],"Unexpected token.",cursor)
                    return False, left_parse, self.lexer_tokens[cursor]

        return True, left_parse, None
 
    def error(self,token, msg,cursor):
        """
        Raises a parsing error.
        """
        self.had_error = True
        self.parser_errors.append(ParsingError(token,msg))
        