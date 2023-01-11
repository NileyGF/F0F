import sys
import F0FTokens
from Visitor import Interpreter,Resolver
from Parser_Generators import First, Follow, LL_1_parsing_table, LL_1_td_parser
from F0FGrammar import Grammar, F0F
import F0FLexer
from F0FParser import LL1_Parser, Parse_Tree
from AST import AST


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
    tree.parse_tree_from_prod_list(parser.left_parse,lexer.tokens)
    ast = AST.ast_from_parse_tree(tree)
    interpreter = Interpreter()
    # resolver
    resolver = Resolver(interpreter)
    resolver.begin(ast)
    # interpret
    interpreter.interpret(ast.root)

    if had_error:
        return had_error, error_list

    #interpreter
    return had_error, error_list

def main(file_path:str='F0F/src/code_examples/Basic.txt'):
    if file_path != None:
        runFile(file_path)
    else:
        print("Usage error: you must pass a file path")

if __name__ == "__main__":
    main(sys.argv[1])

