from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens, symbols_tokens, keywords_tokens

class F0FError:
    def __init__(self,line:int, msg:str):
        self.message = msg
        self.line = line
    
    def __str__(self) -> str:        
        rep = "[line " + str(self.line) + "] : " + self.message
        return rep
    def __repr__(self):
        return self.__str__()
class LexerError(F0FError):
    pass
class ParsingError(F0FError):
    """
    Base class for all parsing exceptions.
    """
    def __init__(self, token:Token, msg:str):
        super().__init__(token.line,msg)
        self._token_prblm = token
    def token_with_problem(self):
        return self._token_prblm
    def __str__(self) -> str:        
        rep = "Parsing error at: " + str(self._token_prblm.lex) +" [line " + str(self.line) + "] : " + self.message
        return rep