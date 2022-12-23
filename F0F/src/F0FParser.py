from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens, symbols_tokens, keywords_tokens
from F0FGrammar import Terminal, NonTerminal, Production, Sentential_Form, Symbol, EOF, Epsilon, Grammar, F0F_LL_1
from F0FErrors import ParsingError
import F0FLexer
from Parser_Generators import First, Follow, LL_1_parsing_table, LL_1_td_parser

class DT_node:
    def __init__(self, symbol:Symbol, children:list = None):
        self.symbol = symbol
        self.children = children
        if children == None:
            self.children = []
        pass

    def is_leaf(self):
        return self.children == None or len(self.children) <= 0
    
    def add_child(self, child:Symbol):
        added_child = DT_node(child)
        self.children.append(added_child)
        return added_child

    def __repr__(self):
        return  self.__str__()

    def __str__(self):
        return str(self.symbol)

    def __iter__(self):
        return iter(self.children)

class Derivation_Tree:
    def __init__(self, root:DT_node = None):
        self.root = root
        if root:
            self.initialized = True
        else: 
            self.initialized = False

        pass

    def derivation_tree_from_prod_list(self,Prod:list):
        ind = 0
        pr: Production = Prod[ind].Head
        self.root = DT_node(pr)
        current_nt = []
        # current_nt.append(self.root)
        for b in Prod[ind].Body:
            child = self.root.add_child(b)
            if type(b) is NonTerminal:
                current_nt.append(child)
            
        ind += 1
        while ind < len(Prod):
            pr = Prod[ind]
            for k in range(len(current_nt)):
                if current_nt[k].symbol == pr.Head:
                    break
            # if pr.Head != current_nt[0].symbol:
            #     print('not working')
            #     return
            for b in Prod[ind].Body:
                child = current_nt[k].add_child(b)
                current_nt.append(child)
            current_nt.remove(current_nt[k])
            ind += 1

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

    def DFS(self):
        pass

class F0FParser:
    def __init__(self):
        self.lexer = None
        self.lookahead = None
        self.left_parse = None
    
    def begin(self):
        """
        Begin parsing from starting symbol and match EOF.
        """
        raise NotImplementedError()

    def report(self, production):
        """
        Adds production to the left parse that is being build.
        """
        self.left_parse.append(production)
        
    def error(self, msg=None):
        """
        Raises a parsing error.
        """
        raise ParsingError(msg)

    def match(self, token_type):
        """
        Consumes one token from the lexer if lookahead matches the given token type.
        Raises parsing error otherwise.
        """
        if token_type == self.lookahead:
            try:
                self.lookahead = self.lexer.next_token().token_type
            except AttributeError:
                self.lookahead = None
        else:
            self.error('Unexpected token')
    
    pass


G = F0F_LL_1()
 
firsts = First(G)
follows = Follow(G, firsts)
# print(follows)
ll_1_table  = LL_1_parsing_table(G, firsts, follows)
ll1_parser = LL_1_td_parser(G, ll_1_table, firsts, follows)

code = "// First F0F program \nprint \"Hello World!\" ; \nint x = 56; \nint y = x + 5.7; \nfun void LOL(bool f, string c){ \nwhile(false){} \n	return;\n}\n"
lexer = F0FLexer.F0FLexer(code)
# print(code)
# print()
# print(lexer.tokens)
tree_list = ll1_parser(lexer.tokens)
tree = Derivation_Tree()
tree.derivation_tree_from_prod_list(tree_list)
print(tree)
