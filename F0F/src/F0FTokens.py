from enum import Enum
class TokenType(Enum):
    pass
class TerminalsTokens(TokenType):
    """single character tokens"""
    opar = '('
    cpar = ')'
    obracket = '['
    cbracket = ']'
    obrace = '{'
    cbrace = '}'
    comma = ','
    dot = '.'
    semicolon = ';'
    minus = '-'
    plus = '+'
    star = '*'
    slash = '/'
    percent = '%'
    caret = '^'
    quoat = '\''
    double_quoat = '\"'
    """ comparisson """
    equal = '=' 
    equal_equal = '==' 
    excl = '!'
    excl_equal = '!='
    greater = '>' 
    greater_equal = '>=' 
    less = '<' 
    less_equal = '<='
    """ keywords """
    _class = 'class' 
    function = 'fun'
    null = 'null'
    this = 'this'
    And = '&&'
    Or = '||'
    Return = 'return'
    While = 'while'
    For = 'for'
    If = 'if'
    Else = 'else'
    Print = 'print'
    """ literals """
    true = 'true'
    false = 'false'
    integer = 0
    decimal = 1
    string_chain = 2
    identifier = 3
    """ end of file"""
    EOF = 4
    """ types """
    _type = ['int', 'double', 'void', 'bool', 'string', 'mfun', 'point' ]
    # _int = 'int'
    # _double = 'double'
    # _void = 'void'
    # _bool = 'bool' 
    # _string = 'string' 
    # _math_function = 'mfun' 
    # _point = 'point' 
    # Floor, Ceil, Round, Random

    epsilon = 35
    pass

class NonTerminalsTokens(TokenType):
    Program = 0
    Declaration_list = 1
    Declaration = 2
    ClassDecl = 3
    FunctDecl = 4
    FunctList = 'ups'
    VarDecl = 5
    VarValue = 'sub'
    Statement = 6
    Expression = 7
    ForStmt = 8
    ForFirst = 'sub'
    WhileStmt = 9
    IfStmt = 10
    elseStmt = 'sub'
    PrintStmt = 11
    ReturnStmt = 12
    ret = 'sub'
    Block = 13
    block_body = 'sub'
    Assignment = 14
    Call = 15
    Logic_Or = 16
    OR = 17
    Logic_And = 18
    AND = 'ups'
    Equality = 19
    Eq = 20
    Comparison = 21
    LGEq = 22
    Term = 23
    Factor = 24
    FX = 25
    Pow = 26 # Pow -> Unary ^ Unary
    UX = 27
    PowX = 'ups2'
    Unary = 28
    call_type = 29
    call_right = 'add'
    Primary = 30
    Parameters = 31
    Parm = 32
    Arguments = 33
    Arg = 34

# TokenType = Enum('TokenType', '')
class Token:
    """
    Basic token class.

    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    line: int
        Token's line
    length: int
        Token's length
    """

    def __init__(self, lex:str, token_type:TokenType, line:int = -1, length:int = -1):
        self.lex = lex
        self.token_type = token_type
        self.line = line
        self.length = length

    def __str__(self):
        return f'{self.token_type.name}: {self.lex}, line:{self.line}'

    def __repr__(self):
        return str(self)

    # @property
    # def is_valid(self):
    #     return True

symbols_tokens = {
    '+'   : TerminalsTokens.plus,
    '-'   : TerminalsTokens.minus,
    '*'   : TerminalsTokens.star,
    '/'   : TerminalsTokens.slash,
    '('   : TerminalsTokens.opar,
    ')'   : TerminalsTokens.cpar,
    ','   : TerminalsTokens.comma,
    '.'   : TerminalsTokens.dot,
    '$'   : TerminalsTokens.EOF,
    '['   : TerminalsTokens.obracket,
    ']'   : TerminalsTokens.cbracket,
    '{'   : TerminalsTokens.obrace,
    '}'   : TerminalsTokens.cbrace,
    ';'   : TerminalsTokens.semicolon,
    '%'   : TerminalsTokens.percent,
    '^'   : TerminalsTokens.caret,
    '\''  : TerminalsTokens.quoat,
    '\"'  : TerminalsTokens.double_quoat,
    '='   : TerminalsTokens.equal,
    '=='  : TerminalsTokens.equal_equal,
    '!'   : TerminalsTokens.excl,
    '!='  : TerminalsTokens.excl_equal,
    '<'   : TerminalsTokens.less,
    '<='  : TerminalsTokens.less_equal,
    '>'   : TerminalsTokens.greater,
    '>='  : TerminalsTokens.greater_equal,
    '&&'  : TerminalsTokens.And,
    '||'  : TerminalsTokens.Or,
}
keywords_tokens = {
    'class'  : TerminalsTokens._class,
    'fun'    : TerminalsTokens.function,
    'null'   : TerminalsTokens.null,
    'this'   : TerminalsTokens.this,
    'return' : TerminalsTokens.Return,
    'while'  : TerminalsTokens.While,
    'for'    : TerminalsTokens.For,
    'if'     : TerminalsTokens.If,
    'else'   : TerminalsTokens.Else,
    'print'  : TerminalsTokens.Print,
    'true'   : TerminalsTokens.true,
    'false'  : TerminalsTokens.false,
    'type'   : TerminalsTokens._type,
    'void'   : TerminalsTokens._type,
    'int'    : TerminalsTokens._type,
    'double' : TerminalsTokens._type,
    'bool'   : TerminalsTokens._type,
    'string' : TerminalsTokens._type,
    'mfun'   : TerminalsTokens._type,
    'point'  : TerminalsTokens._type
}

# fixed_tokens = symbols_tokens + keywords_tokens + {
    # 'integer'   : TerminalsTokens.integer,
    # 'decimal'   : TerminalsTokens.decimal,
    # 'id'        : TerminalsTokens.identifier,
    # '_type'     : TerminalsTokens._type,
    # 'string_chain' : TerminalsTokens.string_chain,
    # '$'         : TerminalsTokens.EOF,

    # 'program'           : NonTerminalsTokens.Program,
    # 'declaration_list'  : NonTerminalsTokens.Declaration_list,
    # 'declaration'       : NonTerminalsTokens.Declaration,
    # 'class_decl'        : NonTerminalsTokens.ClassDecl,
    # 'funct_decl'        : NonTerminalsTokens.FunctDecl,
    # 'funct_list'        : NonTerminalsTokens.FunctList,
    # 'var_decl'          : NonTerminalsTokens.VarDecl,
    # 'var_value'         : NonTerminalsTokens.VarValue,
    # 'statement'         : NonTerminalsTokens.Statement,
    # 'expression'        : NonTerminalsTokens.Expression,
    # 'for_statement'     : NonTerminalsTokens.ForStmt,
    # 'while_statement'   : NonTerminalsTokens.WhileStmt,
    # 'if_statement'      : NonTerminalsTokens.IfStmt,
    # 'print_statement'   : NonTerminalsTokens.PrintStmt,
    # 'return_statement'  : NonTerminalsTokens.ReturnStmt,
    # 'block'             : NonTerminalsTokens.Block,
    # 'assignment'        : NonTerminalsTokens.Assignment,
    # 'call'              : NonTerminalsTokens.Call,
    # 'logic_or'          : NonTerminalsTokens.Logic_Or,
    # 'OR'                : NonTerminalsTokens.OR,
    # 'logic_and'         : NonTerminalsTokens.Logic_And,
    # 'AND'               : NonTerminalsTokens.AND,
    # 'equality'          : NonTerminalsTokens.Equality,
    # 'eql'               : NonTerminalsTokens.Eq,
    # 'comparison'        : NonTerminalsTokens.Comparison,
    # 'LGEq'              : NonTerminalsTokens.LGEq,
    # 'term'              : NonTerminalsTokens.Term,
    # 'factor'            : NonTerminalsTokens.Factor,
    # 'FX'                : NonTerminalsTokens.FX,
    # 'pow'               : NonTerminalsTokens.Pow,
    # 'PowX'              : NonTerminalsTokens.PowX,
    # 'unary'             : NonTerminalsTokens.Unary,
    # 'UX'                : NonTerminalsTokens.UX,
    # 'call_type'         : NonTerminalsTokens.call_type,
    # 'primary'           : NonTerminalsTokens.Primary,
    # 'parameters'        : NonTerminalsTokens.Parameters,
    # 'parm'              : NonTerminalsTokens.Parm,
    # 'arguments'         : NonTerminalsTokens.Arguments,
    # 'args'              : NonTerminalsTokens.Arg,
    # 'for_first'         : NonTerminalsTokens.ForFirst,
    # 'else_stmt'         : NonTerminalsTokens.elseStmt,
    # 'ret'               : NonTerminalsTokens.ret,
    # 'block_body'        : NonTerminalsTokens.block_body

# }