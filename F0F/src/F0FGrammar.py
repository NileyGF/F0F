from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens

class Symbol(Token):

    def __init__(self, lex: str, token_type:TokenType):
        super().__init__(lex, token_type)

    def __str__(self):
        return self.lex
    def __repr__(self):
        return repr(self.lex)

    @property
    def IsEpsilon(self):
        return False

    def __len__(self):
        return 1

class NonTerminal(Symbol):
    def __init__(self, lex: str, token_type: NonTerminalsTokens):
        super().__init__(lex, token_type)
        self.productions = []

    @property
    def IsTerminal(self):
        return False

    @property
    def IsNonTerminal(self):
        return True

    @property
    def IsEpsilon(self):
        return False

class Terminal(Symbol):
    def __init__(self, lex: str, token_type:TerminalsTokens):
        super().__init__(lex, token_type)

    @property
    def IsTerminal(self):
        return True

    @property
    def IsNonTerminal(self):
        return False

    @property
    def IsEpsilon(self):
        return 

class EOF(Terminal):
    def __init__(self):
        super().__init__('$', TerminalsTokens.EOF)

class Sentential_Form:
    def __init__(self, *args):
        self._symbols = tuple(s for s in args if not s.IsEpsilon)

    def __len__(self):
        return len(self._symbols)

    def __repr__(self):
        return  self.__str__()#str(self._symbols)
    def __str__(self):
        sentString = ''
        for s in self._symbols:
            s:Symbol
            sentString += str(s.lex) + ' '
        return sentString

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    @property
    def IsEpsilon(self):
        return False

class Epsilon(Terminal, Sentential_Form):

    def __init__(self):
        super().__init__('epsilon', TerminalsTokens.epsilon)

    def __str__(self):
        return "e"

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))
    
    def __hash__(self):
        return hash("")

    def __iter__(self):
        yield self

    @property
    def IsEpsilon(self):
        return True

class Production:
    def __init__(self, nonTerminal:NonTerminal, sentential:Sentential_Form):
        self.Head = nonTerminal
        self.Body = sentential
    
    def __str__(self):
        return '%s --> %s' % (self.Head.lex, self.Body)
    def __repr__(self):
        return self.__str__()
    
    @property
    def IsEpsilon(self):
        return self.Body.IsEpsilon

class AttributedProduction(Production):
    def __init__(self, nonTerminal: NonTerminal, sentential: Sentential_Form, attributes):
        super().__init__(nonTerminal, sentential)
        self.attributes = attributes
    def syntetice(self):
        pass

class Grammar():
    
    def __init__(self):

        self.Productions = []
        self.nonTerminals = []
        self.terminals = []
        self.mainSymbol = None
        self.Epsilon = Epsilon()
        self.EOF = EOF()

        self.symbDict = { '$': self.EOF }
    
    def New_NonTerminal(self, lex:str, token_type:NonTerminalsTokens, main_symbol = False):
        
        if not lex: raise Exception("Empty lex")

        nt = NonTerminal(lex, token_type)
        if main_symbol:
            if self.mainSymbol is None:
                self.mainSymbol = nt
            else: raise Exception(" ".join(["This grammar already has a main symbol: ", self.mainSymbol]))
        
        self.nonTerminals.append(nt)
        self.symbDict[nt.lex] = nt
        return nt
    
    def New_Terminal(self, lex:str, token_type:TerminalsTokens):

        if not lex: raise Exception("Empty lex")

        t = Terminal(lex, token_type)
        self.terminals.append(t)
        self.symbDict[t.lex] = t
        return t

    def Add_Production(self, production:Production):
        production.Head.productions.append(production)
        self.Productions.append(production)

    def __str__(self):

        ans = 'Non-Terminals:\n\t'
        for nt in self.nonTerminals:
            ans+= str(nt.lex) + " , "
        ans = ans[:len(ans) - 2]
        ans+='\n\n'

        ans += 'Terminals:\n\t'
        for t in self.terminals:
            ans+= str(t.lex) + " , "
        ans = ans[:len(ans) - 2]
        ans+='\n\n'

        ans += 'Productions:'
        for pr in self.Productions:
            ans += "\n\t" + str(pr) 
        ans = ans[:len(ans) - 1]

        return ans

    def __getitem__(self, lex:str):
        try:
            return self.symbDict[lex]
        except KeyError:
            return None
    
""" class F0F_LL_1(Grammar):
    def __init__(self):
        nonTerminals = [
            #0
            NonTerminal('program'         , NonTerminalsTokens.Program),
            NonTerminal('declaration_list', NonTerminalsTokens.Declaration_list),
            NonTerminal('declaration'     , NonTerminalsTokens.Declaration),
            NonTerminal('class_decl'      , NonTerminalsTokens.ClassDecl),
            NonTerminal('funct_decl'      , NonTerminalsTokens.FunctDecl),
            #5
            NonTerminal('var_decl'        , NonTerminalsTokens.VarDecl),
            NonTerminal('statement'       , NonTerminalsTokens.Statement),
            NonTerminal('expression'      , NonTerminalsTokens.Expression),
            NonTerminal('for_statement'   , NonTerminalsTokens.ForStmt),
            NonTerminal('while_statement' , NonTerminalsTokens.WhileStmt),
            #10
            NonTerminal('if_statement'    , NonTerminalsTokens.IfStmt),
            NonTerminal('print_statement' , NonTerminalsTokens.PrintStmt),
            NonTerminal('return_statement', NonTerminalsTokens.ReturnStmt),
            NonTerminal('block'           , NonTerminalsTokens.Block),
            NonTerminal('assignment'      , NonTerminalsTokens.Assignment),
            #15
            NonTerminal('call'            , NonTerminalsTokens.Call),
            NonTerminal('logic_or'        , NonTerminalsTokens.Logic_Or),
            NonTerminal('OR'              , NonTerminalsTokens.OR),
            NonTerminal('logic_and'       , NonTerminalsTokens.Logic_And),
            NonTerminal('AND'             , NonTerminalsTokens.AND),
            #20
            NonTerminal('equality'        , NonTerminalsTokens.Equality),
            NonTerminal('eql'             , NonTerminalsTokens.Eq),
            NonTerminal('comparison'      , NonTerminalsTokens.Comparison),
            NonTerminal('LGEq'            , NonTerminalsTokens.LGEq),
            NonTerminal('term'            , NonTerminalsTokens.Term),
            #25
            NonTerminal('factor'          , NonTerminalsTokens.Factor),
            NonTerminal('FX'              , NonTerminalsTokens.FX),
            NonTerminal('pow'             , NonTerminalsTokens.Pow),
            NonTerminal('UX'              , NonTerminalsTokens.UX),
            NonTerminal('unary'           , NonTerminalsTokens.Unary),
            #30
            NonTerminal('PowX'            , NonTerminalsTokens.PowX),
            NonTerminal('call_type'       , NonTerminalsTokens.call_type),
            NonTerminal('primary'         , NonTerminalsTokens.Primary),
            NonTerminal('call_right'      , NonTerminalsTokens.call_right),
            NonTerminal('parameters'      , NonTerminalsTokens.Parameters),
            #35
            NonTerminal('parm'            , NonTerminalsTokens.Parm),
            NonTerminal('arguments'       , NonTerminalsTokens.Arguments),
            NonTerminal('args'            , NonTerminalsTokens.Arg),
            NonTerminal('for_first'       , NonTerminalsTokens.ForFirst),
            NonTerminal('else_stmt'       , NonTerminalsTokens.elseStmt),
            #40
            NonTerminal('ret'             , NonTerminalsTokens.ret),
            NonTerminal('block_body'      , NonTerminalsTokens.block_body),
            NonTerminal('funct_list'      , NonTerminalsTokens.FunctList),
            NonTerminal('var_value'       , NonTerminalsTokens.VarValue)
            #44
        ]
        self.Epsilon = Epsilon()
        self.EOF = EOF()
        terminals = [
            #0
            Terminal('+', TerminalsTokens.plus),
            Terminal('-', TerminalsTokens.minus),
            Terminal('*', TerminalsTokens.star),
            Terminal('/', TerminalsTokens.slash),
            Terminal('(', TerminalsTokens.opar),
            #5
            Terminal(')',TerminalsTokens.cpar),
            Terminal(',', TerminalsTokens.comma),
            Terminal('.', TerminalsTokens.dot),
            Terminal('[', TerminalsTokens.obracket),            
            Terminal(']', TerminalsTokens.cbracket),
            #10
            Terminal('{', TerminalsTokens.obrace),
            Terminal('}', TerminalsTokens.cbrace),
            Terminal(';', TerminalsTokens.semicolon),
            Terminal('%', TerminalsTokens.percent),
            Terminal('^', TerminalsTokens.caret),
            #15
            Terminal('\'', TerminalsTokens.quoat),
            Terminal('\"', TerminalsTokens.double_quoat),
            Terminal('=', TerminalsTokens.equal),
            Terminal('==', TerminalsTokens.equal_equal),
            Terminal('!', TerminalsTokens.excl),
            #20
            Terminal('!=', TerminalsTokens.excl_equal),
            Terminal('<', TerminalsTokens.less),
            Terminal('<=', TerminalsTokens.less_equal),
            Terminal('>', TerminalsTokens.greater),
            Terminal('>=', TerminalsTokens.greater_equal),
            #25
            Terminal('class', TerminalsTokens._class),
            Terminal('fun', TerminalsTokens.function),
            Terminal('null',  TerminalsTokens.null),
            Terminal('this', TerminalsTokens.this),
            Terminal('&&', TerminalsTokens.And),
            #30
            Terminal('||', TerminalsTokens.Or),
            Terminal('return', TerminalsTokens.Return),
            Terminal('while', TerminalsTokens.While),
            Terminal('for', TerminalsTokens.For),
            Terminal('if', TerminalsTokens.If),
            #35
            Terminal('else', TerminalsTokens.Else),
            Terminal('print', TerminalsTokens.Print),
            Terminal('true', TerminalsTokens.true),
            Terminal('false', TerminalsTokens.false),
            Terminal('integer', TerminalsTokens.integer),
            #40
            Terminal('decimal', TerminalsTokens.decimal),
            Terminal('id', TerminalsTokens.identifier),
            Terminal('_type', TerminalsTokens._type),
            Terminal('string_chain', TerminalsTokens.string_chain)
            #44
        ]

        self.mainSymbol = nonTerminals[0]
        symbDict = { '$': self.EOF,
                    'epsilon' : self.Epsilon }
        for nt in nonTerminals:
            symbDict[nt.lex] = nt
        for t in terminals:
            symbDict[t.lex] = t

        Productions = [
            # program -> declaration_list EOF
            Production(nonTerminals[0], Sentential_Form(nonTerminals[1])),  #, self.EOF
            # declaration_list -> declaration declaration_list
            # declaration_list -> epsilon
            Production(nonTerminals[1], Sentential_Form(nonTerminals[2], nonTerminals[1])),
            Production(nonTerminals[1], self.Epsilon),
            # declaration -> class_decl
            # declaration -> funct_decl
            # declaration -> var_decl
            # declaration -> statement
            Production(nonTerminals[2], Sentential_Form(nonTerminals[3])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[4])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[5])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[6])),
            # statement -> expression ;
            # statement -> for_statement
            # statement -> while_statement
            # statement -> if_statement
            # statement -> print_statement
            # statement -> return_statement
            # statement -> block
            Production(nonTerminals[6], Sentential_Form(nonTerminals[7], terminals[12])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[8])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[9])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[10])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[11])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[12])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[13])),
            # expression -> assignment
            Production(nonTerminals[7], Sentential_Form(nonTerminals[14])),
            # assignment -> call id = assignment
            # assignment -> id = assignment
            # assignment -> logic_or
            # Production(nonTerminals[14],Sentential_Form(nonTerminals[15],terminals[41],terminals[17],nonTerminals[14])),
            Production(nonTerminals[14],Sentential_Form(nonTerminals[15],terminals[17],nonTerminals[14])),
            # Production(nonTerminals[14],Sentential_Form(terminals[41],terminals[17],nonTerminals[14])),
            Production(nonTerminals[14],Sentential_Form(nonTerminals[16])),
            # logic_or -> logic_and OR
            # OR -> || logic_and OR
            # OR -> epsilon
            Production(nonTerminals[16],Sentential_Form(nonTerminals[18],nonTerminals[17])),
            Production(nonTerminals[17],Sentential_Form(terminals[30],nonTerminals[18],nonTerminals[17])),
            Production(nonTerminals[17],self.Epsilon),
            # logic_and -> equality AND
            # AND -> && equality AND
            # AND -> epsilon
            Production(nonTerminals[18],Sentential_Form(nonTerminals[20],nonTerminals[19])),
            Production(nonTerminals[19],Sentential_Form(terminals[29],nonTerminals[20],nonTerminals[19])),
            Production(nonTerminals[19],self.Epsilon),
            # equality -> comparison eql
            # eql -> == comparison eql
            # eql -> != comparison eql
            # eql -> epsilon
            Production(nonTerminals[20],Sentential_Form(nonTerminals[22],nonTerminals[21])),
            Production(nonTerminals[21],Sentential_Form(terminals[18],nonTerminals[22],nonTerminals[21])),
            Production(nonTerminals[21],Sentential_Form(terminals[20],nonTerminals[22],nonTerminals[21])),
            Production(nonTerminals[21],self.Epsilon),
            # comparison -> term LGEq
            # LGEq -> < term LGEq
            # LGEq -> <= term LGEq
            # LGEq -> > term LGEq
            # LGEq -> >= term LGEq
            # LGEq -> epsilon
            Production(nonTerminals[22],Sentential_Form(nonTerminals[24],nonTerminals[23])),
            Production(nonTerminals[23],Sentential_Form(terminals[21],nonTerminals[24],nonTerminals[23])),
            Production(nonTerminals[23],Sentential_Form(terminals[22],nonTerminals[24],nonTerminals[23])),
            Production(nonTerminals[23],Sentential_Form(terminals[23],nonTerminals[24],nonTerminals[23])),
            Production(nonTerminals[23],Sentential_Form(terminals[24],nonTerminals[24],nonTerminals[23])),
            Production(nonTerminals[23],self.Epsilon),
            # term -> factor FX
            # FX -> + factor FX
            # FX -> - factor FX
            # FX -> epsilon
            Production(nonTerminals[24],Sentential_Form(nonTerminals[25],nonTerminals[26])),
            Production(nonTerminals[26],Sentential_Form(terminals[0], nonTerminals[25],nonTerminals[26])),
            Production(nonTerminals[26],Sentential_Form(terminals[1], nonTerminals[25],nonTerminals[26])),
            Production(nonTerminals[26],self.Epsilon),
            # factor -> pow UX
            # UX -> * pow UX
            # UX -> / pow UX
            # UX -> % pow UX
            # UX -> epsilon
            Production(nonTerminals[25],Sentential_Form(nonTerminals[27],nonTerminals[28])),
            Production(nonTerminals[28],Sentential_Form(terminals[2], nonTerminals[27],nonTerminals[28])),
            Production(nonTerminals[28],Sentential_Form(terminals[3], nonTerminals[27],nonTerminals[28])),
            Production(nonTerminals[28],Sentential_Form(terminals[13],nonTerminals[27],nonTerminals[28])),
            Production(nonTerminals[28],self.Epsilon),
            # pow -> unary PowX
            # PowX -> ^ unary PowX
            # PowX -> epsilon  
            Production(nonTerminals[27],Sentential_Form(nonTerminals[29],nonTerminals[30])),
            Production(nonTerminals[30],Sentential_Form(terminals[14],nonTerminals[29],nonTerminals[30])),
            Production(nonTerminals[30],self.Epsilon),
            # unary -> ! unary
            # unary -> - unary
            # unary -> call
            Production(nonTerminals[29],Sentential_Form(terminals[19],nonTerminals[29])),
            Production(nonTerminals[29],Sentential_Form(terminals[1], nonTerminals[29])),
            Production(nonTerminals[29],Sentential_Form(nonTerminals[15])),
            # call -> primary call_type
            Production(nonTerminals[15],Sentential_Form(nonTerminals[32],nonTerminals[31])),
            # call_type -> . call_rigth call_type
            # call_type -> [ expression ] call_type
            # call_type -> epsilon
            # call_right -> id call_type
            # call_right -> ( arguments ) call_type
            Production(nonTerminals[31],Sentential_Form(terminals[7], nonTerminals[33],nonTerminals[31])),
            Production(nonTerminals[31],Sentential_Form(terminals[8], nonTerminals[7], terminals[9], nonTerminals[31])),
            Production(nonTerminals[31],self.Epsilon),
            Production(nonTerminals[33],Sentential_Form(terminals[41],nonTerminals[31])),
            Production(nonTerminals[33],Sentential_Form(terminals[4], nonTerminals[36],terminals[5], nonTerminals[31])),
            # primary -> true 
            # primary -> false
            # primary -> null
            # primary -> this 
            # primary -> integer 
            # primary -> decimal
            # primary -> string_chain 
            # primary -> id
            # primary -> ( expression )
            Production(nonTerminals[32],Sentential_Form(terminals[37])),
            Production(nonTerminals[32],Sentential_Form(terminals[38])),
            Production(nonTerminals[32],Sentential_Form(terminals[27])),
            Production(nonTerminals[32],Sentential_Form(terminals[28])),
            Production(nonTerminals[32],Sentential_Form(terminals[39])),
            Production(nonTerminals[32],Sentential_Form(terminals[40])),
            Production(nonTerminals[32],Sentential_Form(terminals[43])),
            Production(nonTerminals[32],Sentential_Form(terminals[41])),
            Production(nonTerminals[32],Sentential_Form(terminals[4], nonTerminals[7], terminals[5])),
            # for_statement -> for ( for_first expression ; expression ) statement
            # for_first -> var_decl 
            # for_first -> expression ; 
            Production(nonTerminals[8], Sentential_Form(terminals[33],terminals[4], nonTerminals[38],nonTerminals[7], terminals[12],nonTerminals[7], terminals[5], nonTerminals[6])),
            Production(nonTerminals[38],Sentential_Form(nonTerminals[5])),
            Production(nonTerminals[38],Sentential_Form(nonTerminals[7], terminals[12])),
            # while_statement -> while ( expression ) statement
            Production(nonTerminals[9], Sentential_Form(terminals[32],terminals[4], nonTerminals[7], terminals[5], nonTerminals[6])),
            # if_statement -> if ( expression ) statement else_stmt
            # else_stmt -> else statement
            # else_stmt -> epsilon
            Production(nonTerminals[10],Sentential_Form(terminals[34],terminals[4], nonTerminals[7], terminals[5], nonTerminals[6], nonTerminals[39])),
            Production(nonTerminals[39],Sentential_Form(terminals[35],nonTerminals[6])),
            Production(nonTerminals[39],self.Epsilon),
            # print_statement -> print expression ;
            Production(nonTerminals[11],Sentential_Form(terminals[36],nonTerminals[7], terminals[12])),
            # return_statement -> return ret
            # ret -> expression ;
            # ret -> ;
            Production(nonTerminals[12],Sentential_Form(terminals[31],nonTerminals[40])),
            # Production(nonTerminals[12],Sentential_Form(terminals[31],nonTerminals[7], terminals[12])),
            Production(nonTerminals[40],Sentential_Form(nonTerminals[7], terminals[12])),
            Production(nonTerminals[40],Sentential_Form(terminals[12])),
            # block -> { block_body }
            # block_body -> declaration_list
            # block_body -> epsilon
            Production(nonTerminals[13],Sentential_Form(terminals[10],nonTerminals[41],terminals[11])),
            Production(nonTerminals[41],Sentential_Form(nonTerminals[1])),
            Production(nonTerminals[41],self.Epsilon),
            # class_decl -> class id { funct_list }
            Production(nonTerminals[3], Sentential_Form(terminals[25],terminals[41],terminals[10],nonTerminals[42],terminals[11])),
            # funct_list -> funct_decl funct_list
            # funct_list -> epsilon
            Production(nonTerminals[42],Sentential_Form(nonTerminals[4], nonTerminals[42])),
            Production(nonTerminals[42],self.Epsilon),            
            # funct_decl -> fun type id ( parameters ) block
            Production(nonTerminals[4], Sentential_Form(terminals[26],terminals[42],terminals[41],terminals[4], nonTerminals[34],terminals[5], nonTerminals[13])),
            # var_decl -> type id var_value
            # var_value -> = expression ;
            # var_value -> ;            
            Production(nonTerminals[5], Sentential_Form(terminals[42],terminals[41],nonTerminals[43])),
            Production(nonTerminals[43],Sentential_Form(terminals[17],nonTerminals[7], terminals[12])),    
            Production(nonTerminals[43],Sentential_Form(terminals[12])), 
            # parameters -> type id parm
            # parameters -> epsilon
            # parm -> , type id parm
            # parm -> epsilon
            Production(nonTerminals[34],Sentential_Form(terminals[42],terminals[41],nonTerminals[35])),
            Production(nonTerminals[34],self.Epsilon),
            Production(nonTerminals[35],Sentential_Form(terminals[6], terminals[42],terminals[41],nonTerminals[35])),
            Production(nonTerminals[35],self.Epsilon),
            # arguments -> expression args
            # arguments -> epsilon
            # args -> , expression args
            # args -> epsilon
            Production(nonTerminals[36],Sentential_Form(nonTerminals[7], nonTerminals[37])),
            Production(nonTerminals[36],self.Epsilon),
            Production(nonTerminals[37],Sentential_Form(terminals[6], nonTerminals[7], nonTerminals[37])),
            Production(nonTerminals[37],self.Epsilon)

        ]
        
        for pr in Productions:
            pr.Head.productions.append(pr)

        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.symbDict = symbDict
        self.Productions = Productions

    pass
 """

class F0F(Grammar):
    def __init__(self):
        self.Epsilon = Epsilon()
        self.EOF = EOF()
        terminals = [
            # 0
            Terminal('+', TerminalsTokens.plus),
            Terminal('-', TerminalsTokens.minus),
            Terminal('*', TerminalsTokens.star),
            Terminal('/', TerminalsTokens.slash),
            Terminal('(', TerminalsTokens.opar),
            # 5
            Terminal(')',TerminalsTokens.cpar),
            Terminal(',', TerminalsTokens.comma),
            Terminal('.', TerminalsTokens.dot),
            Terminal('[', TerminalsTokens.obracket),            
            Terminal(']', TerminalsTokens.cbracket),
            # 10
            Terminal('{', TerminalsTokens.obrace),
            Terminal('}', TerminalsTokens.cbrace),
            Terminal(';', TerminalsTokens.semicolon),
            Terminal('%', TerminalsTokens.percent),
            Terminal('^', TerminalsTokens.caret),
            # 15
            Terminal('\'', TerminalsTokens.quoat),
            Terminal('\"', TerminalsTokens.double_quoat),
            Terminal('=', TerminalsTokens.equal),
            Terminal('==', TerminalsTokens.equal_equal),
            Terminal('!', TerminalsTokens.excl),
            # 20
            Terminal('!=', TerminalsTokens.excl_equal),
            Terminal('<', TerminalsTokens.less),
            Terminal('<=', TerminalsTokens.less_equal),
            Terminal('>', TerminalsTokens.greater),
            Terminal('>=', TerminalsTokens.greater_equal),
            # 25
            Terminal('&&', TerminalsTokens.And),
            Terminal('||', TerminalsTokens.Or),
            Terminal('if', TerminalsTokens.If),
            Terminal('else', TerminalsTokens.Else),
            Terminal('for', TerminalsTokens.For),
            # 30
            Terminal('while', TerminalsTokens.While),
            Terminal('return', TerminalsTokens.Return),
            Terminal('fun', TerminalsTokens.function),
            Terminal('null',  TerminalsTokens.null),
            Terminal('_type', TerminalsTokens._type),
            # 35
            Terminal('true', TerminalsTokens.true),
            Terminal('false', TerminalsTokens.false),
            Terminal('integer', TerminalsTokens.integer),
            Terminal('decimal', TerminalsTokens.decimal),
            Terminal('string_chain', TerminalsTokens.string_chain),
            #40
            Terminal('id', TerminalsTokens.identifier),
            Terminal('Forge', TerminalsTokens.Forge)
        ]
        nonTerminals = [
            # 0 
            NonTerminal('program'         , NonTerminalsTokens.Program),
            NonTerminal('declaration_list', NonTerminalsTokens.Declaration_list),
            NonTerminal('declaration'     , NonTerminalsTokens.Declaration),
            NonTerminal('funct_decl'      , NonTerminalsTokens.FunctDecl),
            NonTerminal('var_decl'        , NonTerminalsTokens.VarDecl),
            # 5
            NonTerminal('statement'       , NonTerminalsTokens.Statement),
            NonTerminal('statement_list'  , NonTerminalsTokens.Statement_List),
            NonTerminal('F0F'             , NonTerminalsTokens.F0F),
            NonTerminal('for_statement'   , NonTerminalsTokens.ForStmt),
            NonTerminal('while_statement' , NonTerminalsTokens.WhileStmt),
            # 10
            NonTerminal('if_statement'    , NonTerminalsTokens.IfStmt),
            NonTerminal('return_statement', NonTerminalsTokens.ReturnStmt),
            NonTerminal('expression'      , NonTerminalsTokens.Expression),
            NonTerminal('parameters'      , NonTerminalsTokens.Parameters),
            NonTerminal('parm'            , NonTerminalsTokens.Parm),
            # 15
            NonTerminal('arguments'       , NonTerminalsTokens.Arguments),
            NonTerminal('args'            , NonTerminalsTokens.Arg),
            NonTerminal('else_stmt'       , NonTerminalsTokens.elseStmt),
            NonTerminal('ret'             , NonTerminalsTokens.ret),
            NonTerminal('var_value'       , NonTerminalsTokens.VarValue),
            # 20
            NonTerminal('call'            , NonTerminalsTokens.Call),
            NonTerminal('operation'       , NonTerminalsTokens.Operation),
            NonTerminal('OR'              , NonTerminalsTokens.OR),
            NonTerminal('logic_and'       , NonTerminalsTokens.Logic_And),
            NonTerminal('AND'             , NonTerminalsTokens.AND),
            # 25 
            NonTerminal('equality'        , NonTerminalsTokens.Equality),
            NonTerminal('eql'             , NonTerminalsTokens.Eq),
            NonTerminal('comparison'      , NonTerminalsTokens.Comparison),
            NonTerminal('LGEq'            , NonTerminalsTokens.LGEq),
            NonTerminal('term'            , NonTerminalsTokens.Term),
            # 30
            NonTerminal('factor'          , NonTerminalsTokens.Factor),
            NonTerminal('FX'              , NonTerminalsTokens.FX),
            NonTerminal('pow'             , NonTerminalsTokens.Pow),
            NonTerminal('PowX'            , NonTerminalsTokens.PowX),
            NonTerminal('unary'           , NonTerminalsTokens.Unary),
            # 35
            NonTerminal('UX'              , NonTerminalsTokens.UX),
            NonTerminal('primary'         , NonTerminalsTokens.Primary),
            NonTerminal('call_type'       , NonTerminalsTokens.call_type)
            # 38   
        ]

        self.mainSymbol = nonTerminals[0]
        symbDict = { '$': self.EOF,
                    'epsilon' : self.Epsilon }
        for nt in nonTerminals:
            symbDict[nt.lex] = nt
        for t in terminals:
            symbDict[t.lex] = t

        Productions = [
            # program -> declaration_list F0F EOF
            Production(nonTerminals[0], Sentential_Form(nonTerminals[1], nonTerminals[7])),  
            # declaration_list -> declaration declaration_list
            # declaration_list -> epsilon
            Production(nonTerminals[1], Sentential_Form(nonTerminals[2], nonTerminals[1])),
            Production(nonTerminals[1], self.Epsilon),
            # declaration -> funct_decl
            # declaration -> var_decl
            # declaration -> statement
            Production(nonTerminals[2], Sentential_Form(nonTerminals[3])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[4])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[5])),
            # statement_list -> var_decl statement_list
            # statement_list -> statement statement_list
            # statement_list -> epsilon
            Production(nonTerminals[6], Sentential_Form(nonTerminals[4], nonTerminals[6])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[5], nonTerminals[6])),
            Production(nonTerminals[6], self.Epsilon),
            # F0F -> Forge ( parameters ) { statement_list }
            Production(nonTerminals[7], Sentential_Form(terminals[41],terminals[4], nonTerminals[13],terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # funct_decl -> fun type id ( parameters ) { statement_list }
            Production(nonTerminals[3], Sentential_Form(terminals[32],terminals[34],terminals[40],terminals[4], nonTerminals[13],terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # var_decl -> type id var_value
            # var_value -> = expression ;
            # var_value -> ;   
            Production(nonTerminals[4], Sentential_Form(terminals[34],terminals[40],nonTerminals[19])),
            Production(nonTerminals[19],Sentential_Form(terminals[17],nonTerminals[12],terminals[12])),    
            Production(nonTerminals[19],Sentential_Form(terminals[12])), 
            # statement -> expression ;
            # statement -> for_statement
            # statement -> while_statement
            # statement -> if_statement
            # statement -> return_statement
            Production(nonTerminals[5], Sentential_Form(nonTerminals[12],terminals[12])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[8])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[9])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[10])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[11])),
            # for_statement -> for ( var_decl expression ; expression ) { statement_list }
            Production(nonTerminals[8], Sentential_Form(terminals[29],terminals[4], nonTerminals[4], nonTerminals[12],terminals[12],nonTerminals[12],terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # while_statement -> while ( expression ) { statement_list }
            Production(nonTerminals[9], Sentential_Form(terminals[30],terminals[4], nonTerminals[12], terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # if_statement -> if ( expression ) { statement_list } else_stmt
            # else_stmt -> else { statement_list }
            # else_stmt -> epsilon
            Production(nonTerminals[10],Sentential_Form(terminals[27],terminals[4], nonTerminals[12],terminals[10],nonTerminals[6], terminals[11],nonTerminals[17])),
            Production(nonTerminals[17],Sentential_Form(terminals[28],terminals[10],nonTerminals[6], terminals[11])),
            Production(nonTerminals[17],self.Epsilon),
            # return_statement -> return ret
            # ret -> expression ;
            # ret -> ;
            Production(nonTerminals[11],Sentential_Form(terminals[31],nonTerminals[18])),
            Production(nonTerminals[18],Sentential_Form(nonTerminals[12],terminals[12])),
            Production(nonTerminals[18],Sentential_Form(terminals[12])),
            # parameters -> type id parm
            # parameters -> epsilon
            # parm -> , type id parm
            # parm -> epsilon
            Production(nonTerminals[13],Sentential_Form(terminals[34],terminals[40],nonTerminals[14])),
            Production(nonTerminals[13],self.Epsilon),
            Production(nonTerminals[14],Sentential_Form(terminals[6], terminals[34],terminals[40],nonTerminals[14])),
            Production(nonTerminals[14],self.Epsilon),
            # arguments -> expression args
            # arguments -> epsilon
            # args -> , expression args
            # args -> epsilon
            Production(nonTerminals[15],Sentential_Form(nonTerminals[12],nonTerminals[16])),
            Production(nonTerminals[15],self.Epsilon),
            Production(nonTerminals[16],Sentential_Form(terminals[6], nonTerminals[12],nonTerminals[16])),
            Production(nonTerminals[16],self.Epsilon),
            # expression -> call = expression
            # expression -> operation
            Production(nonTerminals[12],Sentential_Form(nonTerminals[20],terminals[17],nonTerminals[21])),
            Production(nonTerminals[12],Sentential_Form(nonTerminals[21])),
            # operation -> logic_and OR
            # OR -> || operation
            # OR -> epsilon
            Production(nonTerminals[21],Sentential_Form(nonTerminals[23],nonTerminals[22])),
            Production(nonTerminals[22],Sentential_Form(terminals[26],nonTerminals[21])),
            Production(nonTerminals[22],self.Epsilon),
            # logic_and -> equality AND
            # AND -> && logic_and
            # AND -> epsilon
            Production(nonTerminals[23],Sentential_Form(nonTerminals[25],nonTerminals[24])),
            Production(nonTerminals[24],Sentential_Form(terminals[25],nonTerminals[23])),
            Production(nonTerminals[24],self.Epsilon),
            # equality -> comparison eql
            # eql -> == equality
            # eql -> != equality
            # eql -> epsilon
            Production(nonTerminals[25],Sentential_Form(nonTerminals[27],nonTerminals[26])),
            Production(nonTerminals[26],Sentential_Form(terminals[18],nonTerminals[25])),
            Production(nonTerminals[26],Sentential_Form(terminals[20],nonTerminals[25])),
            Production(nonTerminals[26],self.Epsilon),
            # comparison -> term LGEq
            # LGEq -> < comparison
            # LGEq -> <= comparison
            # LGEq -> > comparison
            # LGEq -> >= comparison
            # LGEq -> epsilon
            Production(nonTerminals[27],Sentential_Form(nonTerminals[29],nonTerminals[28])),
            Production(nonTerminals[28],Sentential_Form(terminals[21],nonTerminals[27])),
            Production(nonTerminals[28],Sentential_Form(terminals[22],nonTerminals[27])),
            Production(nonTerminals[28],Sentential_Form(terminals[23],nonTerminals[27])),
            Production(nonTerminals[28],Sentential_Form(terminals[24],nonTerminals[27])),
            Production(nonTerminals[28],self.Epsilon),
            # term -> factor FX
            # FX -> + term
            # FX -> - term
            # FX -> epsilon
            Production(nonTerminals[29],Sentential_Form(nonTerminals[30],nonTerminals[31])),
            Production(nonTerminals[31],Sentential_Form(terminals[0], nonTerminals[29])),
            Production(nonTerminals[31],Sentential_Form(terminals[1], nonTerminals[29])),
            Production(nonTerminals[31],self.Epsilon),
            # factor -> pow PowX
            # PowX -> * factor
            # PowX -> / factor
            # PowX -> % factor
            # PowX -> epsilon
            Production(nonTerminals[30],Sentential_Form(nonTerminals[32],nonTerminals[33])),
            Production(nonTerminals[33],Sentential_Form(terminals[2], nonTerminals[30])),
            Production(nonTerminals[33],Sentential_Form(terminals[3], nonTerminals[30])),
            Production(nonTerminals[33],Sentential_Form(terminals[13],nonTerminals[30])),
            Production(nonTerminals[33],self.Epsilon),
            # pow -> unary UX
            # UX -> ^ pow
            # UX -> epsilon
            Production(nonTerminals[32],Sentential_Form(nonTerminals[34],nonTerminals[35])),
            Production(nonTerminals[35],Sentential_Form(terminals[14],nonTerminals[32])),
            Production(nonTerminals[35],self.Epsilon),
            # unary -> ! unary
            # unary -> - unary
            # unary -> call
            Production(nonTerminals[34],Sentential_Form(terminals[19],nonTerminals[34])),
            Production(nonTerminals[34],Sentential_Form(terminals[1], nonTerminals[34])),
            Production(nonTerminals[34],Sentential_Form(nonTerminals[20])),
            # call -> primary call_type 
            Production(nonTerminals[20],Sentential_Form(nonTerminals[36],nonTerminals[37])),
            # call_type -> . id call_type
            # call_type -> [ expression ] call_type
            # call_type -> ( arguments ) call_type
            # call_type -> epsilon
            Production(nonTerminals[37],Sentential_Form(terminals[7], terminals[40],nonTerminals[37])),
            # Production(nonTerminals[37],Sentential_Form(terminals[8], nonTerminals[12],terminals[9], nonTerminals[37])),
            Production(nonTerminals[37],Sentential_Form(terminals[4], nonTerminals[15],terminals[5], nonTerminals[37])),
            Production(nonTerminals[37],self.Epsilon),
            # primary -> true 
            # primary -> false
            # primary -> null
            # primary -> integer 
            # primary -> decimal
            # primary -> string_chain 
            # primary -> id
            # primary -> ( expression )
            Production(nonTerminals[36],Sentential_Form(terminals[35])),
            Production(nonTerminals[36],Sentential_Form(terminals[36])),
            Production(nonTerminals[36],Sentential_Form(terminals[33])),
            Production(nonTerminals[36],Sentential_Form(terminals[37])),
            Production(nonTerminals[36],Sentential_Form(terminals[38])),
            Production(nonTerminals[36],Sentential_Form(terminals[39])),
            Production(nonTerminals[36],Sentential_Form(terminals[40])),
            Production(nonTerminals[36],Sentential_Form(terminals[4], nonTerminals[12],terminals[5]))                        
        ]

        for pr in Productions:
            pr.Head.productions.append(pr)

        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.symbDict = symbDict
        self.Productions = Productions
