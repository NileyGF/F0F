# F0F
Domain Specific Language: Forge 0(Zero) Finder (F0F). 

It's main purpose is to develop methods to find functions's zeros.

It is used in the game at https://github.com/ArPaVa/Zero-Blacksmith-game

## To run the program
In the terminal, get to the path: F0F/F0F/src

There, run: python3 -m F0Fmain <file_path>

Where <file_path> is the path to the file with the code to execute in our Domain Specific Language.


## Grammar:
    program -> declaration_list F0F 

    declaration_list -> declaration declaration_list | epsilon

    declaration -> funct_decl | var_dec | statement

    statement_list -> var_decl statement_list | statement statement_list | epsilon

    F0F -> Forge ( parameters ) { statement_list }

    funct_decl -> fun id ( parameters ) { statement_list }

    var_decl -> var id var_value
    var_value -> = expression ; | ;   

    statement -> expression ; | for_statement | while_statement | if_statement | return_statement | print_statement

    for_statement -> for ( var_decl expression ; expression ) { statement_list }

    while_statement -> while ( expression ) { statement_list }

    if_statement -> if ( expression ) { statement_list } else_stmt
    else_stmt -> else { statement_list } | epsilon

    return_statement -> return ret
    ret -> expression ; | ;

    print_statement -> print ( expression ) ;

    parameters -> id parm | epsilon
    parm -> , id parm | epsilon

    arguments -> expression args | epsilon
    args -> , expression args | epsilon

    expression -> call = operation | operation

    operation -> logic_and OR
    OR -> || operation | epsilon

    logic_and -> equality AND
    AND -> && logic_and | epsilon

    equality -> comparison eql
    eql -> == equality | != equality | epsilon

    comparison -> term LGEq
    LGEq -> < comparison | <= comparison | > comparison  | >= comparison | epsilon

    term -> factor FX
    FX -> + term | - term | epsilon

    factor -> pow PowX
    PowX -> * factor | / factor | % factor | epsilon

    pow -> unary UX
    UX -> ^ pow | epsilon

    unary -> ! unary | - unary | call

    call -> primary call_type 

    call_type -> ( arguments ) call_type | epsilon

    primary -> true  | false | null | integer  | decimal | string_chain  | id | ( expression )

It is a context free grammar. It is not LL(1) because the productions of 'expression' have intersections in the firsts, since they both reach 'call'. 
We parse this grammar with a modified LL(1) predictive parser, even though the grammar itself isn't LL(1). We acomplish that doing a branching in the conflictive cases. That allows us to check wich production is the appropriate for the token.

## Compiler architecture:
    lexer = F0FLexer.F0FLexer(code)
    parser = LL1_Parser(G)
    parser.begin(lexer.tokens)
    tree = Parse_Tree()
    tree.parse_tree_from_prod_list(parser.left_parse,lexer.tokens)
    ast = AST.ast_from_parse_tree(tree)
    interpreter = Interpreter()
    # resolver
    resolver = Resolver(interpreter)
    resolver.begin(ast)
    # interpret
    interpreter.interpret(ast.root)
    
The compiler for F0F implements a lexer(scanner) that creates the code tokens in a lineal time according to the source code size. Later the parser checks for errors and return a productions list. From wich is created a Parse Tree. Later it is used to build the Abstract Syntax Tree (AST), discarding semantic information as grouping symbols, and epsilon.
The compiler implements a Visitor pattern, used for resolving scopes and variables values and interpreting. The language have dynamic typing, but the type check could be effectuated using a visitor. 

