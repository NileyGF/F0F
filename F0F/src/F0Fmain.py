import F0FTokens
from Parser_Generators import First, Follow, LL_1_parsing_table, LL_1_td_parser
from F0FGrammar import Grammar, F0F_LL_1
import F0FLexer

class F0F_language():
    def __init__(self, G:Grammar):
        self.Grammar = G
        self.fixed_tokens = F0FTokens.fixed_tokens
    
    @property
    def firsts(self):
        return First(self.Grammar)
    
    @property
    def follows(self):
        return Follow(self.Grammar)
    
    @property
    def table_LL1(self):
        return LL_1_parsing_table(self.Grammar, self.firsts, self.follows)
    
    @property
    def tokenizer(self):
        pass

    @property
    def parser(self):
        PT = LL_1_parsing_table(self.Grammar, self.firsts, self.follows)
        parser = LL_1_td_parser(self.Grammar, PT)
        return parser
   
# f = open('1st_test.txt', 'r')
# code = f.read()
# f.close()
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
tree = ll1_parser(lexer.tokens)
print(tree)