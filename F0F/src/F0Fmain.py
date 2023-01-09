import sys
import F0FTokens
from Parser_Generators import First, Follow, LL_1_parsing_table, LL_1_td_parser
from F0FGrammar import Grammar, F0F
import F0FLexer
from F0FParser import LL1_Parser, Parse_Tree
from AST import AST

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

def runFile(file_path:str):
    file = open(file_path,'r')
    source_code = file.read()
    file.close()
    had_error, error_list = run(source_code)
    if had_error:
        for er in error_list:
            print(er)

def run(code):
    lexer = F0FLexer.F0FLexer(code)
    had_error = lexer.had_error 
    error_list = lexer.lexer_errors
    G = F0F()
    parser = LL1_Parser(G)
    parser.begin(lexer.tokens)
    had_error = had_error or parser.had_error 
    error_list = error_list + parser.parser_errors
    if had_error:
        return had_error, error_list
    
    tree = Parse_Tree()
    tree.parse_tree_from_prod_list(parser.left_parse)
    # print(tree)
    ast = AST.ast_from_parse_tree(tree)
    # resolver
    
    # interpret
    ast.interpret()

    if had_error:
        return had_error, error_list

    #interpreter
    return had_error, error_list

def main(file_path:str=None):
    if file_path != None:
        runFile(file_path)
    else:
        print("Usage error: you must pass a file path")

# if __name__ == "__main__":
#     main(sys.argv[1])

f = open('F0F/src/code_examples/Basic.txt', 'r')
code = f.read()
f.close()
G = F0F()
run(code)
# firsts = First(G)
# follows = Follow(G, firsts)
# # print(follows)
# ll_1_table  = LL_1_parsing_table(G, firsts, follows)

# code = "// First F0F program \nprint \"Hello World!\" ; \nint x = 56; \nint y = x + 5.7; \nfun void LOL(bool f, string c){ \nwhile(false){} \n	return;\n}\n"
# lexer = F0FLexer.F0FLexer(code)
# had_error = lexer.had_error 
# error_list = lexer.lexer_errors
# G = F0F()
# parser = LL1_Parser(lexer.tokens,G)
# had_error = had_error or parser.had_error 
# error_list = error_list + parser.parser_errors
# # print('had error: ',had_error)
# # print(error_list)
# tree = Parse_Tree()
# tree.parse_tree_from_prod_list(parser.left_parse)
# print(tree)