import F0FTokens
from Parser_Generators import First, Follow, LL_1_parsing_table, LL_1_top_to_down_parser
from F0FGrammar import Grammar, Terminal, NonTerminal, Production, Sentential_Form, Symbol, EOF, Epsilon
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
        parser = LL_1_top_to_down_parser(self.Grammar, PT)
        return parser
   
# f = open('1st_test.txt', 'r')
# code = f.read()
# f.close()
code = "// First F0F program \nprint(\"Hello World!\"); \nint x = 56; \nint y = x + 5.7; \nvoid LOL(bool f, char c){ \nwhile(false){} \n	return;\n}\n"
lexer = F0FLexer.F0FLexer(code)
print(code)
print()
print(lexer.tokens)