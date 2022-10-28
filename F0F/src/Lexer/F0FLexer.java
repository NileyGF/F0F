package Lexer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Tokens.F0FToken.TokenType;
import Tokens.F0FToken;

public class F0FLexer 
{
    private final String source_code;
    private final List<F0FToken> tokens = new ArrayList<>();
    private int start = 0;
    private int current = 0;
    private int line = 1;
    private int column = 0;
    private int tok_length = 0;

    private static final Map<String, TokenType> keywords;

    static {
        keywords = new HashMap<>();
        keywords.put("and",    TokenType.And);
        /*keywords.put("class",  TokenType.Class);*/
        keywords.put("else",   TokenType.Else);
        keywords.put("false",  TokenType.False);
        keywords.put("for",    TokenType.For);
        keywords.put("def",    TokenType.Def);
        keywords.put("if",     TokenType.If);
        keywords.put("null",   TokenType.Null);
        keywords.put("or",     TokenType.Or);
        keywords.put("print",  TokenType.Print);
        keywords.put("return", TokenType.Return);
        /*keywords.put("super",  SUPER);*/
        /*keywords.put("this",   THIS);*/
        keywords.put("true",   TokenType.True);
        /*keywords.put("var",    VAR);*/
        keywords.put("while",  TokenType.While);
        keywords.put("mfun",   TokenType.MFUN);
        keywords.put("Point",  TokenType.POINT);
        keywords.put("void",   TokenType.VOID);
        keywords.put("bool",   TokenType.BOOL);
        keywords.put("string", TokenType.STRING);
        keywords.put("int", TokenType.INT);
        keywords.put("float", TokenType.FLOAT);
        keywords.put("double", TokenType.DOUBLE);
    }
    
    F0FLexer(String source) 
    {
        this.source_code = source;
    }
    List<F0FToken> scanTokens() 
    {
        while (!end_file()) {
            // We are at the beginning of the next lexeme.
            start = current;
            tok_length = 0;
            scanToken();
        }

        tokens.add(new F0FToken(TokenType.EOF, "", null, line, 0 ,0));
        return tokens;
    }
    private boolean end_file() 
    {
        return current >= source_code.length();
    }
    private void scanToken() 
    {
        char c = advance();
        switch (c) {
            case '(': tok_length++; addToken(TokenType.opar); column++; break;
            case ')': tok_length++; addToken(TokenType.cpar); column++; break;
            case '{': tok_length++; addToken(TokenType.obrace); column++; break;
            case '}': tok_length++; addToken(TokenType.cbrace); column++; break;
            case '[': tok_length++; addToken(TokenType.obracket); column++; break;
            case ']': tok_length++; addToken(TokenType.cbracket); column++; break;
            case ',': tok_length++; addToken(TokenType.comma); column++; break;
            case '.': tok_length++; addToken(TokenType.dot); column++; break;
            case '-': tok_length++; addToken(TokenType.minus); column++; break;
            case '+': tok_length++; addToken(TokenType.plus); column++; break;
            case ';': tok_length++; addToken(TokenType.semicolon); column++; break;
            case '*': tok_length++; addToken(TokenType.star); column++; break;
            case '!': 
                    if(match_next('=')) {
                        tok_length+=2; 
                        addToken(TokenType.excl_equal);
                        column +=2;
                    }
                    else{
                        tok_length++; 
                        addToken(TokenType.excl);
                        column++;
                    } break;
            case '=': 
                    if(match_next('=')) {
                        tok_length+=2; 
                        addToken(TokenType.equal_equal);
                        column +=2;
                    }
                    else{
                        tok_length++; 
                        addToken(TokenType.equal);
                        column++;
                    } break;
            case '<': 
                    if(match_next('=')) {
                        tok_length+=2; 
                        addToken(TokenType.less_equal);
                        column +=2;
                    }
                    else{
                        tok_length++; 
                        addToken(TokenType.less);
                        column++;
                    } break;
            case '>': 
                    if(match_next('=')) {
                        tok_length+=2; 
                        addToken(TokenType.greater_equal);
                        column +=2;
                    }
                    else{
                        tok_length++; 
                        addToken(TokenType.greater);
                        column++;
                    } break;
            case '/':
                    if (match_next('/')) {
                    // A comment goes until the end of the line.
                        while (peek() != '\n' && !end_file()) 
                            {advance(); column++;}
                    } 
                    else {
                        tok_length++;
                        addToken(TokenType.slash);
                        column++;
                    } break;
                    // Ignore whitespace. 
            case ' ' : column++; tok_length = 0; break;
            case '\r': column++; tok_length = 0; break;
            case '\t': column++; tok_length = 0; break;                  
            case '\n': line++; column = 0; tok_length = 0; break;
            case '"' : string(); break;
            default:
                    if (Digit(c)) {
                        number();
                    } else if (Alpha(c)) {
                        identifier();
                    } 
                    else {} //Lox.error(line, "Unexpected character."); 
                    break;
        }
    }
    private char advance() {
        current++;
        return source_code.charAt(current - 1);
    }
    private void addToken(TokenType type, Object ...literal) {
        String text = source_code.substring(start, current);
        tokens.add(new F0FToken(type, text, literal, line, column, tok_length));
    }
    private boolean match_next(char expected) 
    {
        if (end_file()) return false;
        if (source_code.charAt(current) != expected) return false;
        current++;
        return true;
    }
    private char peek() { //lookahead 1
        if (end_file()) return '\0';
        return source_code.charAt(current);
    }
/*     private char peekNext() { //lookahead 2
        if (current + 1 >= source_code.length()) return '\0';
        return source_code.charAt(current + 1);
    } */
    private void string() {
        while (peek() != '"' && !end_file()) {
            if (peek() == '\n') {
                line++;
                column = 0;
            }
            column++;
            tok_length++;
            advance();
        }

        // Unterminated string.
        if (end_file()) {
            //Lox.error(line, "Unterminated string.");
            return;
        }

        // The closing ".
        advance();

        // Trim the surrounding quotes.
        String value = source_code.substring(start + 1, current - 1);
        addToken(TokenType.STRING, value);
    }
    private boolean Digit(char c)
    {
        return c >= '0' && c <= '9';
    }
    private boolean Alpha(char c)
    {
        boolean lower_case = (c >= 'a' && c <= 'z');
        boolean capital = (c >= 'A' && c <= 'Z');
        return lower_case || capital || c == '_';
    }
    private void number()
    {
        boolean decimal = false;
        while (Digit(peek())) 
            {
                column ++; tok_length ++;
                advance();
            }
        // Look for a fractional part.
        if (peek() == '.') 
        {
            if (current + 1 < source_code.length()) 
            {
                char peeknext = source_code.charAt(current + 1);
                if(Digit(peeknext))
                {    // Consume the "."
                    advance();
                    decimal = true;
                    tok_length++;
                }
                column ++;
            }
            while (Digit(peek())) 
            {
                column ++; tok_length ++;
                advance();
            }
        }

        if(decimal)
        {
            addToken(TokenType.Decimal, Double.parseDouble(source_code.substring(start, current)));
        } 
        else
        {
            addToken(TokenType.Integer, Integer.parseInt(source_code.substring(start, current)));
        }
        
    }
    private void identifier()
    {
        while (Alpha(peek()) || Digit(peek())) {
            column ++; tok_length++;
            advance();
        }

        // See if the identifier is a reserved word.
        String text = source_code.substring(start, current);

        TokenType type = keywords.get(text);
        if (type == null) type = TokenType.Identifier;
        addToken(type, text);
    }
}
