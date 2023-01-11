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

    declaration_list -> declaration declaration_list
    declaration_list -> epsilon

    declaration -> funct_decl
    declaration -> var_decl
    declaration -> statement

    statement_list -> var_decl statement_list
    statement_list -> statement statement_list
    statement_list -> epsilon

    F0F -> Forge ( parameters ) { statement_list }

    funct_decl -> fun id ( parameters ) { statement_list }

    var_decl -> var id var_value
    var_value -> = expression ;
    var_value -> ;   

    statement -> expression ;
    statement -> for_statement
    statement -> while_statement
    statement -> if_statement
    statement -> return_statement
    statement -> print_statement

    for_statement -> for ( var_decl expression ; expression ) { statement_list }

    while_statement -> while ( expression ) { statement_list }

    if_statement -> if ( expression ) { statement_list } else_stmt
    else_stmt -> else { statement_list }
    else_stmt -> epsilon

    return_statement -> return ret
    ret -> expression ;
    ret -> ;

    print_statement -> print ( expression ) ;

    parameters -> id parm
    parameters -> epsilon
    parm -> , id parm
    parm -> epsilon

    arguments -> expression args
    arguments -> epsilon
    args -> , expression args
    args -> epsilon

    expression -> call = operation
    expression -> operation

    operation -> logic_and OR
    OR -> || operation
    OR -> epsilon

    logic_and -> equality AND
    AND -> && logic_and
    AND -> epsilon

    equality -> comparison eql
    eql -> == equality
    eql -> != equality
    eql -> epsilon

    comparison -> term LGEq
    LGEq -> < comparison
    LGEq -> <= comparison
    LGEq -> > comparison
    LGEq -> >= comparison
    LGEq -> epsilon

    term -> factor FX
    FX -> + term
    FX -> - term
    FX -> epsilon

    factor -> pow PowX
    PowX -> * factor
    PowX -> / factor
    PowX -> % factor
    PowX -> epsilon

    pow -> unary UX
    UX -> ^ pow
    UX -> epsilon

    unary -> ! unary
    unary -> - unary
    unary -> call

    call -> primary call_type 

    call_type -> ( arguments ) call_type
    call_type -> epsilon

    primary -> true 
    primary -> false
    primary -> null
    primary -> integer 
    primary -> decimal
    primary -> string_chain 
    primary -> id
    primary -> ( expression )