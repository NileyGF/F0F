from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens, symbols_tokens, keywords_tokens
from F0FErrors import F0FError, LexerError
class F0FLexer:
    def __init__(self, source_code:str):
        self.start = 0
        self.current = 0
        self.line = 1
        self.token_length = 0
        self.had_error = False
        self.lexer_errors = []

        if not source_code: raise Exception()
        self.source_code = source_code

        self.tokens:list = []
        self.tokenize_text()
    
    def tokenize_text(self):
        """
        Tokenize `self.source_code` and set it to `self.tokens`.
        """
        while not self.end_file():
            self.start = self.current
            self.token_length = 0
            self.scan_Token()
        
        # self.tokens.append(Token('$', TerminalsTokens.EOF, self.line, 0))
        return self.tokens
    
    def scan_Token(self):
        c = self.advance()
        # switch()
        if c == ' ' or c == '\r' or c == '\t':
            #consume empty spaces
            self.token_length = 0        
        elif c == '(' or c == ')' or c == '[' or c == ']' \
            or c == '{' or c == '}' or c == ',' or c == '.'\
            or c == '-' or c == '+' or c == '*' or c == '^'\
            or c == ';' or c =='%':

            self.token_length += 1
            self.add_Token(symbols_tokens[c])
        elif c == '!':
            if self.match_next('='):
                self.token_length += 2
                self.add_Token(symbols_tokens['!='])
            else:
                self.token_length += 1
                self.add_Token(symbols_tokens['!'])
        elif c == '=':
            if self.match_next('='):
                self.token_length += 2
                self.add_Token(symbols_tokens['=='])
            else:
                self.token_length += 1
                self.add_Token(symbols_tokens['='])
        elif c == '<':
            if self.match_next('='):
                self.token_length += 2
                self.add_Token(symbols_tokens['<='])
            else:
                self.token_length += 1
                self.add_Token(symbols_tokens['<'])
        elif c == '>':
            if self.match_next('='):
                self.token_length += 2
                self.add_Token(symbols_tokens['>='])
            else:
                self.token_length += 1
                self.add_Token(symbols_tokens['>'])
        elif c == '/':
            if self.match_next('/'):
                # a comment goes until the end of the line.
                while self.peek() != '\n' and not self.end_file():
                    self.advance()
            else:
                self.token_length += 1
                self.add_Token(symbols_tokens['/'])
        elif c == '\n':
            self.line += 1
            self.token_length = 0
        # elif c == '\'':
        #     pass
        elif c == '\"':
            self.string_chain()
        else:
            if c.isdigit():
                self.token_length +=1
                self.number()
            elif c.isalpha() or c == '_':
                self.token_length +=1
                self.identifier()
            else: 
                self.had_error = True
                self.lexer_errors.append(LexerError(self.line, "Unexpected character."))

    def end_file(self):
        return self.current >= len(self.source_code)
    
    def peek(self):
        """ returns current character """
        if self.end_file():
            return '\0'
        return self.source_code[self.current]
    
    def advance(self):
        """ returns current character and move current to the next one """
        self.current += 1
        return self.source_code[self.current - 1]

    def add_Token(self, token_type:TokenType, lexeme = None):
        if not lexeme:
            lexeme = self.source_code[self.start:self.current]
        self.tokens.append(Token(lexeme, token_type, self.line, self.token_length))
    
    def match_next(self, expected):
        """ returns False if source_code[current] != expected
            else: move current and return True
        """
        if self.end_file(): return False
        if self.source_code[self.current] != expected:
            return False
        self.current += 1
        return True

    def string_chain(self):
        while self.peek() != '\"' and not self.end_file():
            if self.peek() == '\n':
                self.line += 1
            
            self.token_length += 1
            self.advance()
        
        # unterminated string
        if self.end_file():
            self.had_error = True
            self.lexer_errors.append(LexerError(self.line, "Unterminated string"))
            # F0FErrors.error(line, "Unterminated string.");
            pass

        # closing "
        self.advance()

        chain = self.source_code[self.start + 1: self.current - 1]
        self.add_Token(TerminalsTokens.string_chain, chain)

    def alpha(self,c:str):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"
    
    def number(self):
        decimal = False
        while self.peek().isdigit():
            self.advance()
            self.token_length += 1
        if self.peek() == '.':
            if self.current + 1 < len(self.source_code):
                peeknext = self.source_code[self.current+1]
                if peeknext.isdigit():
                    # consume '.'
                    self.advance()
                    decimal = True
                    self.token_length += 1
            while self.peek().isdigit():
                self.advance()
                self.token_length += 1
        
        if decimal:
            self.add_Token(TerminalsTokens.decimal)
        else:
            self.add_Token(TerminalsTokens.integer)

    def identifier(self):
        peek = self.peek()
        while self.alpha(peek) or peek == '_' or peek.isdigit() and not self.end_file():
            self.token_length += 1
            self.advance()
            peek = self.peek()  
        # check if it is a reserved word
        text = self.source_code[self.start:self.current]
        type = keywords_tokens.get(text)

        if not type:
            type = TerminalsTokens.identifier
        self.add_Token(type, text)

